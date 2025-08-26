import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import json
import os
import uuid
from config import *

def setup_slash_commands(bot, logs_system):
    
    @bot.tree.command(name="help", description="عرض قائمة أوامر neral system المحسنة")
    async def help_slash(interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 neral system - نظام الإدارة المتقدم",
            description="**مرحباً بك في neral system** ✨\n`استخدم الأوامر التالية لإدارة سيرفرك بكفاءة عالية`",
            color=0x5865F2,
            timestamp=datetime.utcnow()
        )
        
        # أوامر الإدارة والعقوبات
        moderation_commands = [
            "🔨 `/ban` - حظر عضو من السيرفر نهائياً",
            "🔓 `/unban` - فك حظر عضو من السيرفر",
            "👢 `/kick` - طرد عضو من السيرفر مؤقتاً", 
            "🔇 `/mute` - كتم عضو لفترة زمنية محددة",
            "🔊 `/unmute` - فك كتم العضو المكتوم",
            "⚠️ `/warn` - إعطاء تحذير لعضو مع السبب"
        ]
        
        embed.add_field(
            name="🛡️ **أوامر الإدارة والعقوبات**",
            value="\n".join(moderation_commands),
            inline=False
        )
        
        # أوامر التحذيرات والمعلومات
        info_commands = [
            "📊 `/warnings` - عرض جميع تحذيرات عضو",
            "🗑️ `/clear` - حذف عدد محدد من الرسائل",
            "ℹ️ `/info` - عرض معلومات عضو أو السيرفر",
            "🏓 `/ping` - فحص سرعة استجابة البوت"
        ]
        
        embed.add_field(
            name="ℹ️ **المعلومات والأدوات**",
            value="\n".join(info_commands),
            inline=False
        )
        
        # نظام Reaction Roles
        reaction_commands = [
            "🎭 `/reaction_role_setup` - إنشاء نظام أدوار تفاعلية",
            "➕ `/add_reaction_role` - إضافة دور للرسالة التفاعلية",
            "➖ `/remove_reaction_role` - حذف دور من الرسالة التفاعلية",
            "📋 `/list_reaction_roles` - عرض جميع الأدوار التفاعلية"
        ]
        
        embed.add_field(
            name="🎭 **نظام الأدوار التفاعلية**",
            value="\n".join(reaction_commands),
            inline=False
        )
        
        # إعدادات السيرفر
        embed.add_field(
            name="⚙️ **إعدادات السيرفر**",
            value="🔧 `/settings` - إدارة إعدادات السيرفر والإحصائيات",
            inline=False
        )
        
        # Footer محسن
        embed.set_footer(
            text=f"طُلب بواسطة {interaction.user.display_name} • neral system متاح 24/7",
            icon_url=interaction.user.display_avatar.url
        )
        
        # إضافة thumbnail للسيرفر
        if interaction.guild and interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)
        
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="ban", description="حظر عضو من السيرفر")
    @app_commands.describe(member="العضو المراد حظره", reason="سبب الحظر")
    async def ban_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "لم يتم تحديد سبب"):
        # التحقق من الصلاحيات
        if not interaction.user.guild_permissions.ban_members:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لحظر الأعضاء.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if hasattr(interaction.user, 'top_role') and member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            embed = discord.Embed(
                title="❌ خطأ في الصلاحيات",
                description="لا يمكنك حظر عضو يملك رتبة أعلى منك أو مساوية لك.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # إرسال رسالة خاصة للعضو
            try:
                dm_embed = discord.Embed(
                    title="🔨 تم حظرك من السيرفر",
                    description=f"**السيرفر:** {interaction.guild.name}\n**بواسطة:** {interaction.user.mention}\n**السبب:** {reason}",
                    color=0xFF6B6B
                )
                if interaction.guild.icon:
                    dm_embed.set_thumbnail(url=interaction.guild.icon.url)
                await member.send(embed=dm_embed)
            except:
                pass
            
            await member.ban(reason=f"بواسطة {interaction.user}: {reason}")
            
            embed = discord.Embed(
                title="🔨 تم حظر العضو بنجاح",
                description=f"تم حظر {member.mention} من السيرفر",
                color=0xFF6B6B
            )
            embed.add_field(name="👤 العضو المحظور", value=f"{member} ({member.id})", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{interaction.user.mention}", inline=True)
            embed.add_field(name="📅 التاريخ", value=discord.utils.format_dt(datetime.now(), "F"), inline=True)
            embed.add_field(name="📝 السبب", value=reason, inline=False)
            
            embed.set_thumbnail(url=member.display_avatar.url)
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لحظر هذا العضو.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="unban", description="فك حظر عضو من السيرفر")
    @app_commands.describe(user_id="معرف المستخدم المراد فك حظره", reason="سبب فك الحظر")
    async def unban_slash(interaction: discord.Interaction, user_id: str, reason: str = "لم يتم تحديد سبب"):
        if not interaction.user.guild_permissions.ban_members:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لفك حظر الأعضاء.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            user = await bot.fetch_user(int(user_id))
            await interaction.guild.unban(user, reason=f"بواسطة {interaction.user}: {reason}")
            
            embed = discord.Embed(
                title="🔓 تم فك الحظر بنجاح",
                description=f"تم فك حظر {user.mention}",
                color=0x4ECDC4
            )
            embed.add_field(name="👤 العضو", value=f"{user} ({user.id})", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{interaction.user.mention}", inline=True)
            embed.add_field(name="📝 السبب", value=reason, inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.NotFound:
            embed = discord.Embed(
                title="❌ عضو غير موجود",
                description="المعرف المحدد غير صحيح أو العضو غير محظور.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            embed = discord.Embed(
                title="❌ معرف خاطئ",
                description="يجب أن يكون المعرف رقماً صحيحاً.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="kick", description="طرد عضو من السيرفر")
    @app_commands.describe(member="العضو المراد طرده", reason="سبب الطرد")
    async def kick_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "لم يتم تحديد سبب"):
        if not interaction.user.guild_permissions.kick_members:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لطرد الأعضاء.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # رسالة خاصة للعضو
            try:
                dm_embed = discord.Embed(
                    title="👢 تم طردك من السيرفر",
                    description=f"**السيرفر:** {interaction.guild.name}\n**بواسطة:** {interaction.user.mention}\n**السبب:** {reason}",
                    color=0xFFB74D
                )
                if interaction.guild.icon:
                    dm_embed.set_thumbnail(url=interaction.guild.icon.url)
                await member.send(embed=dm_embed)
            except:
                pass
            
            await member.kick(reason=f"بواسطة {interaction.user}: {reason}")
            
            embed = discord.Embed(
                title="👢 تم طرد العضو بنجاح",
                description=f"تم طرد {member.mention} من السيرفر",
                color=0xFFB74D
            )
            embed.add_field(name="👤 العضو المطرود", value=f"{member} ({member.id})", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{interaction.user.mention}", inline=True)
            embed.add_field(name="📅 التاريخ", value=discord.utils.format_dt(datetime.now(), "F"), inline=True)
            embed.add_field(name="📝 السبب", value=reason, inline=False)
            
            embed.set_thumbnail(url=member.display_avatar.url)
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لطرد هذا العضو.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="mute", description="كتم عضو لفترة محددة")
    @app_commands.describe(member="العضو المراد كتمه", duration="مدة الكتم (مثال: 10د, 2س, 1ي)", reason="سبب الكتم")
    async def mute_slash(interaction: discord.Interaction, member: discord.Member, duration: str = None, reason: str = "لم يتم تحديد سبب"):
        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لكتم الأعضاء.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # تحويل المدة
        mute_seconds = None
        duration_text = "دائم"
        
        if duration:
            try:
                if duration.endswith('د'):
                    mute_seconds = int(duration[:-1]) * 60
                    duration_text = f"{duration[:-1]} دقيقة"
                elif duration.endswith('س'):
                    mute_seconds = int(duration[:-1]) * 3600
                    duration_text = f"{duration[:-1]} ساعة"
                elif duration.endswith('ي'):
                    mute_seconds = int(duration[:-1]) * 86400
                    duration_text = f"{duration[:-1]} يوم"
            except ValueError:
                pass
        
        try:
            # العثور على أو إنشاء رول الكتم
            muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
            if not muted_role:
                muted_role = await interaction.guild.create_role(
                    name="Muted", 
                    color=0x424242,
                    reason="رول الكتم التلقائي - neral system"
                )
                
                for channel in interaction.guild.channels:
                    try:
                        await channel.set_permissions(muted_role, send_messages=False, speak=False, add_reactions=False)
                    except:
                        continue
            
            await member.add_roles(muted_role, reason=f"بواسطة {interaction.user}: {reason}")
            add_muted_user(interaction.guild.id, member.id)
            
            embed = discord.Embed(
                title="🔇 تم كتم العضو بنجاح",
                description=f"تم كتم {member.mention}",
                color=0x8B5CF6
            )
            embed.add_field(name="👤 العضو المكتوم", value=f"{member} ({member.id})", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{interaction.user.mention}", inline=True)
            embed.add_field(name="⏰ المدة", value=duration_text, inline=True)
            embed.add_field(name="📝 السبب", value=reason, inline=False)
            
            embed.set_thumbnail(url=member.display_avatar.url)
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لكتم هذا العضو.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="unmute", description="فك كتم عضو")
    @app_commands.describe(member="العضو المراد فك كتمه")
    async def unmute_slash(interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لفك كتم الأعضاء.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        
        if not muted_role or muted_role not in member.roles:
            embed = discord.Embed(
                title="❌ العضو غير مكتوم",
                description="العضو المحدد ليس مكتوماً حالياً.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            await member.remove_roles(muted_role, reason=f"فك كتم بواسطة {interaction.user}")
            remove_muted_user(interaction.guild.id, member.id)
            
            embed = discord.Embed(
                title="🔊 تم فك الكتم بنجاح",
                description=f"تم فك كتم {member.mention}",
                color=0x4ECDC4
            )
            embed.add_field(name="👤 العضو", value=f"{member} ({member.id})", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{interaction.user.mention}", inline=True)
            embed.add_field(name="📅 التاريخ", value=discord.utils.format_dt(datetime.now(), "F"), inline=True)
            
            embed.set_thumbnail(url=member.display_avatar.url)
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لفك كتم هذا العضو.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="warn", description="إعطاء تحذير لعضو")
    @app_commands.describe(member="العضو المراد تحذيره", reason="سبب التحذير")
    async def warn_slash(interaction: discord.Interaction, member: discord.Member, reason: str):
        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لإعطاء تحذيرات.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        warning_id = str(uuid.uuid4())[:8]
        warning_data = {
            'id': warning_id,
            'reason': reason,
            'moderator': str(interaction.user),
            'moderator_id': interaction.user.id,
            'timestamp': datetime.utcnow().isoformat(),
            'guild_id': interaction.guild.id
        }
        
        add_warning(interaction.guild.id, member.id, warning_data)
        
        warnings = get_user_warnings(interaction.guild.id, member.id)
        warning_count = len(warnings)
        
        embed = discord.Embed(
            title="⚠️ تم إعطاء تحذير",
            description=f"تم إعطاء تحذير لـ {member.mention}",
            color=0xFFB74D
        )
        embed.add_field(name="👤 العضو المحذَّر", value=f"{member} ({member.id})", inline=True)
        embed.add_field(name="👮 بواسطة", value=f"{interaction.user.mention}", inline=True)
        embed.add_field(name="🔢 رقم التحذير", value=f"#{warning_count}", inline=True)
        embed.add_field(name="🆔 معرف التحذير", value=f"`{warning_id}`", inline=True)
        embed.add_field(name="📝 السبب", value=reason, inline=False)
        
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="warnings", description="عرض تحذيرات عضو")
    @app_commands.describe(member="العضو (اختياري)")
    async def warnings_slash(interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        warnings = get_user_warnings(interaction.guild.id, member.id)
        
        if not warnings:
            embed = discord.Embed(
                title="📊 تحذيرات العضو",
                description=f"{member.mention} لا يملك أي تحذيرات.",
                color=0x4ECDC4
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await interaction.response.send_message(embed=embed)
            return
        
        embed = discord.Embed(
            title="📊 قائمة التحذيرات",
            description=f"تحذيرات العضو {member.mention}",
            color=0xFFB74D
        )
        
        for i, warning in enumerate(warnings[:5], 1):  # عرض أول 5 تحذيرات فقط
            timestamp = datetime.fromisoformat(warning['timestamp'])
            embed.add_field(
                name=f"⚠️ التحذير #{i}",
                value=f"**المعرف:** `{warning['id']}`\n**السبب:** {warning['reason'][:50]}{'...' if len(warning['reason']) > 50 else ''}\n**المشرف:** {warning['moderator']}\n**التاريخ:** {discord.utils.format_dt(timestamp, 'd')}",
                inline=False
            )
        
        if len(warnings) > 5:
            embed.add_field(
                name="📈 المزيد",
                value=f"يوجد {len(warnings) - 5} تحذير إضافي لم يتم عرضه",
                inline=False
            )
        
        embed.set_footer(text=f"إجمالي التحذيرات: {len(warnings)} • neral system")
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="clear", description="حذف عدد معين من الرسائل")
    @app_commands.describe(amount="عدد الرسائل المراد حذفها")
    async def purge_slash(interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لحذف الرسائل.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if amount <= 0 or amount > 100:
            embed = discord.Embed(
                title="❌ عدد خاطئ",
                description="يجب أن يكون العدد بين 1 و 100.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        deleted = await interaction.channel.purge(limit=amount)
        
        embed = discord.Embed(
            title="🗑️ تم حذف الرسائل",
            description=f"تم حذف **{len(deleted)}** رسالة بنجاح من {interaction.channel.mention}",
            color=0x4ECDC4
        )
        embed.add_field(name="👮 بواسطة", value=interaction.user.mention, inline=True)
        embed.add_field(name="📅 التاريخ", value=discord.utils.format_dt(datetime.now(), "F"), inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="info", description="عرض معلومات عضو أو السيرفر")
    @app_commands.describe(member="العضو (اختياري)")
    async def info_slash(interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            # معلومات السيرفر
            guild = interaction.guild
            
            embed = discord.Embed(
                title=f"🏠 معلومات السيرفر: {guild.name}",
                description=f"معلومات شاملة عن سيرفر **{guild.name}**",
                color=0x5865F2
            )
            
            # معلومات أساسية
            embed.add_field(
                name="👑 المالك",
                value=f"{guild.owner.mention}" if guild.owner else "غير محدد",
                inline=True
            )
            
            embed.add_field(
                name="👥 الأعضاء",
                value=f"**الإجمالي:** {guild.member_count}\n**البشر:** {len([m for m in guild.members if not m.bot])}\n**البوتات:** {len([m for m in guild.members if m.bot])}",
                inline=True
            )
            
            embed.add_field(
                name="📍 القنوات",
                value=f"**النصية:** {len(guild.text_channels)}\n**الصوتية:** {len(guild.voice_channels)}\n**الفئات:** {len(guild.categories)}",
                inline=True
            )
            
            embed.add_field(
                name="📅 تاريخ الإنشاء",
                value=discord.utils.format_dt(guild.created_at, "F"),
                inline=True
            )
            
            embed.add_field(
                name="🎭 الأدوار",
                value=str(len(guild.roles)),
                inline=True
            )
            
            embed.add_field(
                name="😀 الإيموجيز",
                value=str(len(guild.emojis)),
                inline=True
            )
            
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
                embed.add_field(
                    name="🔗 أيقونة السيرفر",
                    value=f"[رابط الأيقونة]({guild.icon.url})",
                    inline=True
                )
            
            embed.set_footer(text=f"معرف السيرفر: {guild.id} • neral system")
        else:
            # معلومات العضو
            embed = discord.Embed(
                title=f"👤 معلومات العضو: {member.display_name}",
                description=f"معلومات مفصلة عن العضو {member.mention}",
                color=member.color if member.color != discord.Color.default() else 0x5865F2
            )
            
            embed.add_field(
                name="📋 المعلومات الأساسية",
                value=f"**الاسم:** {member}\n**المعرف:** `{member.id}`\n**النك نيم:** {member.display_name}",
                inline=False
            )
            
            embed.add_field(
                name="📅 التواريخ",
                value=f"**إنشاء الحساب:** {discord.utils.format_dt(member.created_at, 'F')}\n**انضمام للسيرفر:** {discord.utils.format_dt(member.joined_at, 'F') if member.joined_at else 'غير محدد'}",
                inline=False
            )
            
            # الأدوار
            roles = [role.mention for role in member.roles if role != interaction.guild.default_role]
            if roles:
                embed.add_field(
                    name="🎭 الأدوار",
                    value=" • ".join(roles[:10]) + (f" • و {len(roles) - 10} دور آخر" if len(roles) > 10 else ""),
                    inline=False
                )
            
            # الحالة
            status_map = {
                discord.Status.online: "🟢 متصل",
                discord.Status.idle: "🟡 خامل",
                discord.Status.dnd: "🔴 مشغول",
                discord.Status.offline: "⚫ غير متصل"
            }
            embed.add_field(
                name="📊 الحالة",
                value=status_map.get(member.status, "❓ غير معروف"),
                inline=True
            )
            
            # التحذيرات
            warnings = get_user_warnings(interaction.guild.id, member.id)
            embed.add_field(
                name="⚠️ التحذيرات",
                value=str(len(warnings)),
                inline=True
            )
            
            # الصورة الشخصية
            if member.avatar:
                embed.set_thumbnail(url=member.avatar.url)
                embed.add_field(
                    name="🖼️ الصورة الشخصية",
                    value=f"[رابط الصورة]({member.avatar.url})",
                    inline=True
                )
            
            embed.set_footer(text=f"معرف العضو: {member.id} • neral system")
        
        await interaction.response.send_message(embed=embed)

    # نظام Reaction Roles - الأوامر الجديدة
    @bot.tree.command(name="reaction_role_setup", description="إعداد رسالة reaction roles جديدة")
    @app_commands.describe(
        channel="القناة التي ستُرسل فيها الرسالة",
        title="عنوان الرسالة",
        description="وصف الرسالة"
    )
    async def setup_reaction_roles(interaction: discord.Interaction, channel: discord.TextChannel, title: str, description: str):
        if not interaction.user.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك صلاحية إدارة الأدوار",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # إنشاء الـ embed
        embed = discord.Embed(
            title=f"🎭 {title}",
            description=description,
            color=0x5865F2
        )
        
        embed.add_field(
            name="📝 كيفية الاستخدام",
            value="تفاعل مع الرموز أدناه للحصول على الأدوار المقابلة",
            inline=False
        )
        
        embed.set_footer(text="neral system - Reaction Roles • سيتم تحديث هذه الرسالة عند إضافة أدوار جديدة")
        
        try:
            # إرسال الرسالة
            message = await channel.send(embed=embed)
            
            # حفظ معلومات الرسالة
            reaction_role_data = load_reaction_roles()
            
            reaction_role_data[str(message.id)] = {
                'guild_id': interaction.guild.id,
                'channel_id': channel.id,
                'message_id': message.id,
                'title': title,
                'description': description,
                'roles': {}
            }
            
            save_reaction_roles(reaction_role_data)
            
            # رسالة تأكيد
            embed = discord.Embed(
                title="✅ تم إنشاء رسالة Reaction Roles بنجاح",
                description=f"تم إنشاء رسالة Reaction Roles في {channel.mention}",
                color=0x4ECDC4
            )
            embed.add_field(name="🆔 معرف الرسالة", value=f"`{message.id}`", inline=True)
            embed.add_field(name="📝 العنوان", value=title, inline=True)
            embed.add_field(name="💡 الخطوة التالية", value="استخدم `/add_reaction_role` لإضافة أدوار للرسالة", inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي صلاحية الإرسال في هذه القناة",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="add_reaction_role", description="إضافة دور لرياكشن معين")
    @app_commands.describe(
        message_id="معرف رسالة Reaction Roles",
        emoji="الرمز التعبيري",
        role="الدور المراد إضافته",
        description="وصف الدور (اختياري)"
    )
    async def add_reaction_role(interaction: discord.Interaction, message_id: str, emoji: str, role: discord.Role, description: str = None):
        if not interaction.user.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك صلاحية إدارة الأدوار",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        reaction_role_data = load_reaction_roles()
        
        if message_id not in reaction_role_data:
            embed = discord.Embed(
                title="❌ رسالة غير موجودة",
                description="لم يتم العثور على رسالة Reaction Roles بهذا المعرف",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        message_data = reaction_role_data[message_id]
        
        if message_data['guild_id'] != interaction.guild.id:
            embed = discord.Embed(
                title="❌ سيرفر مختلف",
                description="هذه الرسالة ليست من نفس السيرفر",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # العثور على الرسالة وإضافة الرياكشن
            channel = bot.get_channel(message_data['channel_id'])
            message = await channel.fetch_message(int(message_id))
            
            await message.add_reaction(emoji)
            
            # إضافة الدور للبيانات
            message_data['roles'][emoji] = {
                'role_id': role.id,
                'role_name': role.name,
                'description': description or f"الحصول على دور {role.name}"
            }
            
            save_reaction_roles(reaction_role_data)
            
            # تحديث الرسالة
            await update_reaction_role_message(bot, message_id, message_data)
            
            embed = discord.Embed(
                title="✅ تم إضافة الدور بنجاح!",
                color=0x4ECDC4
            )
            embed.add_field(name="🎭 الرمز", value=emoji, inline=True)
            embed.add_field(name="🏷️ الدور", value=role.mention, inline=True)
            embed.add_field(name="📝 الوصف", value=description or f"الحصول على دور {role.name}", inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.NotFound:
            embed = discord.Embed(
                title="❌ رسالة غير موجودة",
                description="لم يتم العثور على الرسالة المحددة",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي صلاحية إضافة رياكشن أو تعديل الرسالة",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="remove_reaction_role", description="حذف reaction role معين")
    @app_commands.describe(
        message_id="معرف رسالة Reaction Roles",
        emoji="الرمز التعبيري المراد حذفه"
    )
    async def remove_reaction_role(interaction: discord.Interaction, message_id: str, emoji: str):
        if not interaction.user.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك صلاحية إدارة الأدوار",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        reaction_role_data = load_reaction_roles()
        
        if message_id not in reaction_role_data or emoji not in reaction_role_data[message_id]['roles']:
            embed = discord.Embed(
                title="❌ Reaction Role غير موجود",
                description="لم يتم العثور على الـ reaction role المحدد",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # حذف الرياكشن من الرسالة
            message_data = reaction_role_data[message_id]
            channel = bot.get_channel(message_data['channel_id'])
            message = await channel.fetch_message(int(message_id))
            
            await message.clear_reaction(emoji)
            
            # حذف الدور من البيانات
            role_info = message_data['roles'][emoji]
            del message_data['roles'][emoji]
            
            save_reaction_roles(reaction_role_data)
            
            # تحديث الرسالة
            await update_reaction_role_message(bot, message_id, message_data)
            
            embed = discord.Embed(
                title="✅ تم حذف Reaction Role بنجاح!",
                color=0x4ECDC4
            )
            embed.add_field(name="🎭 الرمز المحذوف", value=emoji, inline=True)
            embed.add_field(name="🏷️ الدور", value=role_info['role_name'], inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ حدث خطأ",
                description=f"حدث خطأ أثناء حذف الـ reaction role: {str(e)[:100]}",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="list_reaction_roles", description="عرض قائمة جميع reaction roles في السيرفر")
    async def list_reaction_roles(interaction: discord.Interaction):
        reaction_role_data = load_reaction_roles()
        
        guild_messages = {
            msg_id: data for msg_id, data in reaction_role_data.items()
            if data['guild_id'] == interaction.guild.id
        }
        
        if not guild_messages:
            embed = discord.Embed(
                title="📋 قائمة Reaction Roles",
                description="لا توجد رسائل reaction roles في هذا السيرفر",
                color=0x5865F2
            )
            embed.add_field(
                name="💡 كيفية البدء",
                value="استخدم `/reaction_role_setup` لإنشاء أول رسالة reaction roles",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="📋 قائمة Reaction Roles",
                description=f"يوجد **{len(guild_messages)}** رسالة reaction roles في هذا السيرفر:",
                color=0x5865F2
            )
            
            for msg_id, data in guild_messages.items():
                channel = bot.get_channel(data['channel_id'])
                channel_mention = channel.mention if channel else "قناة محذوفة"
                
                roles_count = len(data['roles'])
                roles_list = []
                
                for emoji, role_data in list(data['roles'].items())[:5]:  # عرض أول 5 أدوار
                    role = interaction.guild.get_role(role_data['role_id'])
                    if role:
                        roles_list.append(f"{emoji} → {role.mention}")
                    else:
                        roles_list.append(f"{emoji} → دور محذوف")
                
                if roles_count > 5:
                    roles_list.append(f"و {roles_count - 5} دور آخر...")
                
                field_value = f"**المعرف:** `{msg_id}`\n**القناة:** {channel_mention}\n**عدد الأدوار:** {roles_count}"
                if roles_list:
                    field_value += f"\n**الأدوار:**\n" + "\n".join(roles_list)
                else:
                    field_value += "\n**الأدوار:** لا توجد أدوار"
                
                embed.add_field(
                    name=f"📝 {data['title']}",
                    value=field_value,
                    inline=False
                )
        
        embed.set_footer(text="neral system - Reaction Roles")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="settings", description="إدارة إعدادات السيرفر")
    async def settings_slash(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="تحتاج لصلاحيات المدير لإدارة الإعدادات.",
                color=0xFF6B6B
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        config = get_guild_config(interaction.guild.id)
        
        embed = discord.Embed(
            title="⚙️ إعدادات السيرفر",
            description=f"الإعدادات الحالية لسيرفر **{interaction.guild.name}**",
            color=0x5865F2
        )
        
        logs_channel = bot.get_channel(config.get('logs_channel')) if config.get('logs_channel') else None
        
        embed.add_field(
            name="📊 نظام اللوقات",
            value=f"**الحالة:** {'🟢 مفعل' if config.get('logs_enabled') else '🔴 معطل'}\n**القناة:** {logs_channel.mention if logs_channel else 'غير محددة'}",
            inline=False
        )
        
        # إحصائيات السيرفر
        total_warnings = 0
        total_muted = len(config.get('muted_users', []))
        
        # حساب التحذيرات الإجمالية
        for user_warnings in config.get('warnings', {}).values():
            if isinstance(user_warnings, list):
                total_warnings += len(user_warnings)
        
        embed.add_field(
            name="📈 إحصائيات الإدارة",
            value=f"**إجمالي التحذيرات:** {total_warnings}\n**الأعضاء المكتومين:** {total_muted}\n**أوامر البوت:** 13",
            inline=False
        )
        
        # معلومات neral system
        embed.add_field(
            name="🤖 معلومات neral system",
            value=f"**الإصدار:** v2.0 محسن\n**آخر تحديث:** {discord.utils.format_dt(datetime.now(), 'd')}\n**الحالة:** 🟢 متصل",
            inline=False
        )
        
        embed.set_footer(text=f"معرف السيرفر: {interaction.guild.id} • neral system")
        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="ping", description="فحص سرعة البوت")
    async def ping_slash(interaction: discord.Interaction):
        latency = round(bot.latency * 1000)
        
        # تحديد اللون حسب سرعة الاستجابة
        if latency < 100:
            color = 0x4ECDC4  # أخضر
            status_emoji = "🟢"
            status_text = "ممتاز"
        elif latency < 300:
            color = 0xFFB74D  # برتقالي
            status_emoji = "🟡"
            status_text = "جيد"
        else:
            color = 0xFF6B6B  # أحمر
            status_emoji = "🔴"
            status_text = "بطيء"
        
        embed = discord.Embed(
            title="🏓 بونج!",
            description=f"**زمن الاستجابة:** {latency}ms\n**الحالة:** {status_emoji} {status_text}",
            color=color
        )
        
        embed.add_field(
            name="📊 تفاصيل الاتصال",
            value=f"**البوت:** {status_emoji} متصل\n**الخادم:** {status_emoji} يعمل\n**قاعدة البيانات:** {status_emoji} متاحة",
            inline=True
        )
        
        embed.add_field(
            name="🤖 معلومات البوت",
            value=f"**الاسم:** neral system\n**الخوادم:** {len(bot.guilds)}\n**المستخدمين:** {len(set(bot.get_all_members()))}",
            inline=True
        )
        
        embed.set_footer(text=f"طُلب بواسطة {interaction.user.display_name} • neral system")
        await interaction.response.send_message(embed=embed)

# وظائف مساعدة لـ Reaction Roles
def load_reaction_roles():
    """تحميل بيانات reaction roles"""
    try:
        if os.path.exists('data/reaction_roles.json'):
            with open('data/reaction_roles.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_reaction_roles(data):
    """حفظ بيانات reaction roles"""
    try:
        os.makedirs('data', exist_ok=True)
        with open('data/reaction_roles.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"خطأ في حفظ reaction roles: {e}")

async def update_reaction_role_message(bot, message_id, message_data):
    """تحديث رسالة reaction roles"""
    try:
        channel = bot.get_channel(message_data['channel_id'])
        message = await channel.fetch_message(int(message_id))
        
        embed = discord.Embed(
            title=f"🎭 {message_data['title']}",
            description=message_data['description'],
            color=0x5865F2
        )
        
        if message_data['roles']:
            roles_text = []
            for emoji, role_info in message_data['roles'].items():
                roles_text.append(f"{emoji} → **{role_info['role_name']}**")
                if role_info.get('description'):
                    roles_text.append(f"    ↳ {role_info['description']}")
            
            embed.add_field(
                name="🎭 الأدوار المتاحة",
                value="\n".join(roles_text),
                inline=False
            )
        
        embed.add_field(
            name="📝 كيفية الاستخدام",
            value="تفاعل مع الرموز أدناه للحصول على الأدوار المقابلة",
            inline=False
        )
        
        embed.set_footer(text="neral system - Reaction Roles • سيتم تحديث هذه الرسالة عند إضافة أدوار جديدة")
        
        await message.edit(embed=embed)
    except Exception as e:
        print(f"خطأ في تحديث reaction role message: {e}")

# هذه الوظائف يجب أن تكون موجودة في ملف منفصل (database.py مثلاً)
def add_warning(guild_id, user_id, warning_data):
    """إضافة تحذير - يجب تنفيذها حسب نظام قاعدة البيانات المستخدم"""
    pass

def get_user_warnings(guild_id, user_id):
    """الحصول على تحذيرات مستخدم - يجب تنفيذها حسب نظام قاعدة البيانات المستخدم"""
    return []

def add_muted_user(guild_id, user_id):
    """إضافة مستخدم مكتوم - يجب تنفيذها حسب نظام قاعدة البيانات المستخدم"""
    pass

def remove_muted_user(guild_id, user_id):
    """إزالة مستخدم من قائمة المكتومين - يجب تنفيذها حسب نظام قاعدة البيانات المستخدم"""
    pass

def get_guild_config(guild_id):
    """الحصول على إعدادات السيرفر - يجب تنفيذها حسب نظام قاعدة البيانات المستخدم"""
    return {
        'logs_enabled': False,
        'logs_channel': None,
        'warnings': {},
        'muted_users': []
    }