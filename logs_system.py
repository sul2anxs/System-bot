import discord
from datetime import datetime
from config import get_guild_config, get_logs_channel

class LogsSystem:
    def __init__(self, bot):
        self.bot = bot

    async def get_logs_channel(self, guild_id: int):
        """الحصول على قناة اللوقات للسيرفر"""
        channel_id = get_logs_channel(guild_id)
        if not channel_id:
            return None
        
        channel = self.bot.get_channel(channel_id)
        return channel

    async def should_log_event(self, guild_id: int, event_type: str) -> bool:
        """التحقق من ضرورة تسجيل الحدث"""
        config = get_guild_config(guild_id)
        
        if not config.get('logs_enabled', True):
            return False
        
        logs_settings = config.get('logs_settings', {})
        return logs_settings.get(event_type, True)

    async def log_message_delete(self, message):
        """تسجيل حذف رسالة"""
        if not await self.should_log_event(message.guild.id, 'message_delete'):
            return
        
        logs_channel = await self.get_logs_channel(message.guild.id)
        if not logs_channel:
            return

        embed = discord.Embed(
            title="🗑️ تم حذف رسالة",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="👤 العضو",
            value=f"{message.author.mention} ({message.author})",
            inline=True
        )
        
        embed.add_field(
            name="📍 القناة",
            value=f"{message.channel.mention}",
            inline=True
        )
        
        embed.add_field(
            name="🆔 معرف الرسالة",
            value=str(message.id),
            inline=True
        )
        
        if message.content:
            content = message.content[:1024] if len(message.content) > 1024 else message.content
            embed.add_field(
                name="📝 محتوى الرسالة",
                value=content,
                inline=False
            )
        
        if message.attachments:
            attachments_info = "\n".join([f"• {att.filename}" for att in message.attachments])
            embed.add_field(
                name="📎 المرفقات",
                value=attachments_info,
                inline=False
            )
        
        embed.set_footer(
            text=f"وقت الإنشاء: {message.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        await logs_channel.send(embed=embed)

    async def log_message_edit(self, before, after):
        """تسجيل تعديل رسالة"""
        if not await self.should_log_event(before.guild.id, 'message_edit'):
            return
        
        if before.content == after.content:
            return
        
        logs_channel = await self.get_logs_channel(before.guild.id)
        if not logs_channel:
            return

        embed = discord.Embed(
            title="📝 تم تعديل رسالة",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="👤 العضو",
            value=f"{before.author.mention} ({before.author})",
            inline=True
        )
        
        embed.add_field(
            name="📍 القناة",
            value=f"{before.channel.mention}",
            inline=True
        )
        
        embed.add_field(
            name="🔗 رابط الرسالة",
            value=f"[اذهب للرسالة]({after.jump_url})",
            inline=True
        )
        
        if before.content:
            old_content = before.content[:1024] if len(before.content) > 1024 else before.content
            embed.add_field(
                name="📝 المحتوى القديم",
                value=old_content,
                inline=False
            )
        
        if after.content:
            new_content = after.content[:1024] if len(after.content) > 1024 else after.content
            embed.add_field(
                name="📝 المحتوى الجديد",
                value=new_content,
                inline=False
            )
        
        await logs_channel.send(embed=embed)

    async def log_member_join(self, member):
        """تسجيل انضمام عضو"""
        if not await self.should_log_event(member.guild.id, 'member_join'):
            return
        
        logs_channel = await self.get_logs_channel(member.guild.id)
        if not logs_channel:
            return

        embed = discord.Embed(
            title="👋 انضم عضو جديد",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="👤 العضو",
            value=f"{member.mention} ({member})",
            inline=True
        )
        
        embed.add_field(
            name="🆔 معرف العضو",
            value=str(member.id),
            inline=True
        )
        
        embed.add_field(
            name="📅 تاريخ إنشاء الحساب",
            value=member.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            inline=True
        )
        
        embed.add_field(
            name="📊 إجمالي الأعضاء",
            value=str(member.guild.member_count),
            inline=True
        )
        
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        
        await logs_channel.send(embed=embed)

    async def log_member_leave(self, member):
        """تسجيل مغادرة عضو"""
        if not await self.should_log_event(member.guild.id, 'member_leave'):
            return
        
        logs_channel = await self.get_logs_channel(member.guild.id)
        if not logs_channel:
            return

        embed = discord.Embed(
            title="👋 غادر عضو",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="👤 العضو",
            value=f"{member} ({member.id})",
            inline=True
        )
        
        embed.add_field(
            name="📅 تاريخ الانضمام",
            value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S') if member.joined_at else "غير محدد",
            inline=True
        )
        
        embed.add_field(
            name="📊 إجمالي الأعضاء",
            value=str(member.guild.member_count),
            inline=True
        )
        
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        
        await logs_channel.send(embed=embed)

    async def log_member_ban(self, guild, user):
        """تسجيل حظر عضو"""
        if not await self.should_log_event(guild.id, 'member_ban'):
            return
        
        logs_channel = await self.get_logs_channel(guild.id)
        if not logs_channel:
            return

        embed = discord.Embed(
            title="🔨 تم حظر عضو",
            color=discord.Color.dark_red(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="👤 العضو المحظور",
            value=f"{user} ({user.id})",
            inline=False
        )
        
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        
        await logs_channel.send(embed=embed)

    async def log_member_unban(self, guild, user):
        """تسجيل فك حظر عضو"""
        if not await self.should_log_event(guild.id, 'member_unban'):
            return
        
        logs_channel = await self.get_logs_channel(guild.id)
        if not logs_channel:
            return

        embed = discord.Embed(
            title="✅ تم فك حظر عضو",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="👤 العضو",
            value=f"{user} ({user.id})",
            inline=False
        )
        
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        
        await logs_channel.send(embed=embed)

    async def log_member_update(self, before, after):
        """تسجيل تحديث بيانات عضو"""
        if not await self.should_log_event(before.guild.id, 'member_update'):
            return
        
        logs_channel = await self.get_logs_channel(before.guild.id)
        if not logs_channel:
            return

        changes = []
        
        # تحقق من تغيير الاسم المستعار
        if before.nick != after.nick:
            changes.append(f"**الاسم المستعار:** {before.nick or 'بدون'} → {after.nick or 'بدون'}")
        
        # تحقق من تغيير الأدوار
        if before.roles != after.roles:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]
            
            if added_roles:
                changes.append(f"**أدوار مضافة:** {', '.join([role.mention for role in added_roles])}")
            if removed_roles:
                changes.append(f"**أدوار محذوفة:** {', '.join([role.mention for role in removed_roles])}")
        
        if not changes:
            return
        
        embed = discord.Embed(
            title="👤 تم تحديث بيانات عضو",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="👤 العضو",
            value=f"{after.mention} ({after})",
            inline=False
        )
        
        embed.add_field(
            name="📝 التغييرات",
            value="\n".join(changes),
            inline=False
        )
        
        await logs_channel.send(embed=embed)

    async def log_channel_create(self, channel):
        """تسجيل إنشاء قناة"""
        if not await self.should_log_event(channel.guild.id, 'channel_create'):
            return
        
        logs_channel = await self.get_logs_channel(channel.guild.id)
        if not logs_channel:
            return

        embed = discord.Embed(
            title="📂 تم إنشاء قناة جديدة",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="📍 اسم القناة",
            value=f"{channel.mention} ({channel.name})",
            inline=True
        )
        
        embed.add_field(
            name="🆔 معرف القناة",
            value=str(channel.id),
            inline=True
        )
        
        channel_type = {
            discord.ChannelType.text: "نصية",
            discord.ChannelType.voice: "صوتية",
            discord.ChannelType.category: "فئة",
            discord.ChannelType.forum: "منتدى"
        }.get(channel.type, str(channel.type))
        
        embed.add_field(
            name="🔧 نوع القناة",
            value=channel_type,
            inline=True
        )
        
        await logs_channel.send(embed=embed)

    async def log_channel_delete(self, channel):
        """تسجيل حذف قناة"""
        if not await self.should_log_event(channel.guild.id, 'channel_delete'):
            return
        
        logs_channel = await self.get_logs_channel(channel.guild.id)
        if not logs_channel or channel.id == logs_channel.id:
            return

        embed = discord.Embed(
            title="🗑️ تم حذف قناة",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="📍 اسم القناة",
            value=channel.name,
            inline=True
        )
        
        embed.add_field(
            name="🆔 معرف القناة",
            value=str(channel.id),
            inline=True
        )
        
        channel_type = {
            discord.ChannelType.text: "نصية",
            discord.ChannelType.voice: "صوتية",
            discord.ChannelType.category: "فئة",
            discord.ChannelType.forum: "منتدى"
        }.get(channel.type, str(channel.type))
        
        embed.add_field(
            name="🔧 نوع القناة",
            value=channel_type,
            inline=True
        )
        
        await logs_channel.send(embed=embed)

    async def log_guild_update(self, before, after):
        """تسجيل تحديث إعدادات السيرفر"""
        if not await self.should_log_event(before.id, 'guild_update'):
            return
        
        logs_channel = await self.get_logs_channel(before.id)
        if not logs_channel:
            return

        changes = []
        
        if before.name != after.name:
            changes.append(f"**اسم السيرفر:** {before.name} → {after.name}")
        
        if before.description != after.description:
            changes.append(f"**وصف السيرفر:** {before.description or 'بدون'} → {after.description or 'بدون'}")
        
        if before.verification_level != after.verification_level:
            changes.append(f"**مستوى التحقق:** {before.verification_level} → {after.verification_level}")
        
        if not changes:
            return
        
        embed = discord.Embed(
            title="🏠 تم تحديث إعدادات السيرفر",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="📝 التغييرات",
            value="\n".join(changes),
            inline=False
        )
        
        await logs_channel.send(embed=embed)

    async def log_voice_state_update(self, member, before, after):
        """تسجيل تحديث حالة الصوت"""
        if not await self.should_log_event(member.guild.id, 'voice_state_update'):
            return
        
        logs_channel = await self.get_logs_channel(member.guild.id)
        if not logs_channel:
            return

        # انضمام لقناة صوتية
        if before.channel is None and after.channel is not None:
            embed = discord.Embed(
                title="🔊 انضم عضو لقناة صوتية",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 العضو", value=f"{member.mention}", inline=True)
            embed.add_field(name="📍 القناة", value=after.channel.name, inline=True)
            await logs_channel.send(embed=embed)
        
        # مغادرة قناة صوتية
        elif before.channel is not None and after.channel is None:
            embed = discord.Embed(
                title="🔇 غادر عضو قناة صوتية",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 العضو", value=f"{member.mention}", inline=True)
            embed.add_field(name="📍 القناة", value=before.channel.name, inline=True)
            await logs_channel.send(embed=embed)
        
        # انتقال بين قنوات صوتية
        elif before.channel != after.channel and before.channel is not None and after.channel is not None:
            embed = discord.Embed(
                title="🔀 انتقل عضو بين قنوات صوتية",
                color=discord.Color.orange(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 العضو", value=f"{member.mention}", inline=False)
            embed.add_field(name="📍 من القناة", value=before.channel.name, inline=True)
            embed.add_field(name="📍 إلى القناة", value=after.channel.name, inline=True)
            await logs_channel.send(embed=embed)
