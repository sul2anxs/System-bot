import discord
from discord.ext import commands
import asyncio
import json
import os
from datetime import datetime
from config import load_config, save_config
from logs_system import LogsSystem
from commands import setup_commands
from slash_commands import setup_slash_commands

# إعداد التشغيل
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_messages = True
intents.dm_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# إزالة الأمر المساعدة الافتراضي
bot.remove_command('help')

# نظام اللوقات
logs_system = LogsSystem(bot)

# تخزين الرسائل المحذوفة مؤقتاً
deleted_messages_cache = {}

@bot.event
async def on_ready():
    print(f'🤖 البوت {bot.user} جاهز للعمل!')
    print(f'📊 متصل بـ {len(bot.guilds)} سيرفر')
    
    # مزامنة أوامر Slash
    try:
        synced = await bot.tree.sync()
        print(f'✅ تم مزامنة {len(synced)} أمر Slash')
    except Exception as e:
        print(f'❌ فشل في مزامنة أوامر Slash: {e}')
    
    # تعيين حالة البوت
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="نيرال العم"
        )
    )

@bot.event
async def on_guild_join(guild):
    """عند انضمام البوت لسيرفر جديد"""
    print(f'✅ انضم البوت للسيرفر: {guild.name} (ID: {guild.id})')
    
    # إنشاء إعدادات افتراضية للسيرفر
    config = load_config()
    if str(guild.id) not in config:
        config[str(guild.id)] = {
            'logs_enabled': True,
            'logs_channel': None,
            'warnings': {},
            'muted_users': [],
            'logs_settings': {
                'message_delete': True,
                'message_edit': True,
                'member_join': True,
                'member_leave': True,
                'member_ban': True,
                'member_unban': True,
                'member_kick': True,
                'member_update': True,
                'channel_create': True,
                'channel_delete': True,
                'guild_update': True,
                'voice_state_update': True
            }
        }
        save_config(config)

@bot.event
async def on_message_delete(message):
    """عند حذف رسالة"""
    if message.author.bot:
        return
    
    # حفظ الرسالة في الكاش
    deleted_messages_cache[message.id] = {
        'content': message.content,
        'author': message.author,
        'channel': message.channel,
        'created_at': message.created_at,
        'attachments': [att.url for att in message.attachments] if message.attachments else []
    }
    
    # تسجيل في اللوقات
    await logs_system.log_message_delete(message)

@bot.event
async def on_message_edit(before, after):
    """عند تعديل رسالة"""
    if before.author.bot:
        return
    
    await logs_system.log_message_edit(before, after)

@bot.event
async def on_member_join(member):
    """عند انضمام عضو جديد"""
    await logs_system.log_member_join(member)

@bot.event
async def on_member_remove(member):
    """عند مغادرة عضو"""
    await logs_system.log_member_leave(member)

@bot.event
async def on_member_ban(guild, user):
    """عند حظر عضو"""
    await logs_system.log_member_ban(guild, user)

@bot.event
async def on_member_unban(guild, user):
    """عند فك حظر عضو"""
    await logs_system.log_member_unban(guild, user)

@bot.event
async def on_member_update(before, after):
    """عند تحديث بيانات عضو"""
    await logs_system.log_member_update(before, after)

@bot.event
async def on_guild_channel_create(channel):
    """عند إنشاء قناة جديدة"""
    await logs_system.log_channel_create(channel)

@bot.event
async def on_guild_channel_delete(channel):
    """عند حذف قناة"""
    await logs_system.log_channel_delete(channel)

@bot.event
async def on_guild_update(before, after):
    """عند تحديث إعدادات السيرفر"""
    await logs_system.log_guild_update(before, after)

@bot.event
async def on_voice_state_update(member, before, after):
    """عند تغيير حالة الصوت"""
    await logs_system.log_voice_state_update(member, before, after)

@bot.event
async def on_command_error(ctx, error):
    """معالجة أخطاء الأوامر"""
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ ليس لديك صلاحية",
            description="ليس لديك الصلاحيات المطلوبة لتنفيذ هذا الأمر.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ معطى مفقود",
            description="يرجى تقديم جميع المعطيات المطلوبة للأمر.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="❌ معطى خاطئ",
            description="تأكد من صحة المعطيات المرسلة.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        return  # تجاهل الأوامر غير الموجودة
    else:
        print(f'خطأ غير متوقع: {error}')

async def main():
    """الوظيفة الرئيسية لتشغيل البوت"""
    # إعداد الأوامر
    setup_commands(bot, logs_system, deleted_messages_cache)
    setup_slash_commands(bot, logs_system)
    
    # التوكن الخاص بالبوت
    token = 'MTQwOTYwMDkzNTExNzcxNzUyOA.GJwoFu.eQoZej7Ia1kOtqor1uXPcNwBURU2I74GsFrwr0'
    
    try:
        await bot.start(token)
    except discord.LoginFailure:
        print("❌ فشل في تسجيل الدخول! تأكد من صحة التوكن.")
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")

if __name__ == "__main__":
    asyncio.run(main())