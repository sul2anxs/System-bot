import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from config import *

def setup_slash_commands(bot, logs_system):
    
    @bot.tree.command(name="مساعدة", description="عرض قائمة أوامر البوت")
    async def help_slash(interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖أوامر البوت انيرال",
            description="قائمة شاملة بجميع الأوامر المتاحة",
            color=discord.Color.blue()
        )
        
        commands_list = [
            "**🔨 /حظر** - حظر عضو من السيرفر",
            "**🔓 /فك_حظر** - فك حظر عضو",
            "**👢 /طرد** - طرد عضو من السيرفر",
            "**🔇 /كتم** - كتم عضو لفترة محددة",
            "**🔊 /فك_كتم** - فك كتم عضو",
            "**⚠️ /تحذير** - إعطاء تحذير لعضو",
            "**📊 /التحذيرات** - عرض تحذيرات عضو",
            "**🗑️ /مسح** - حذف عدد من الرسائل",
            "**ℹ️ /معلومات** - عرض معلومات عضو أو السيرفر",
            "**⚙️ /إعدادات** - إدارة إعدادات السيرفر",
            "**🏓 /بنق** - فحص سرعة البوت"
        ]
        
        embed.add_field(
            name="📋 الأوامر المتاحة",
            value="\n".join(commands_list),
            inline=False
        )
        
        embed.set_footer(text="💡 يمكنك أيضاً استخدام الأوامر العادية بـ !")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="حظر", description="حظر عضو من السيرفر")
    @app_commands.describe(member="العضو المراد حظره", reason="سبب الحظر")
    async def ban_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "لم يتم تحديد سبب"):
        # التحقق من الصلاحيات
        if not interaction.user.guild_permissions.ban_members:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لحظر الأعضاء.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if hasattr(interaction.user, 'top_role') and member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            embed = discord.Embed(
                title="❌ خطأ في الصلاحيات",
                description="لا يمكنك حظر عضو يملك رتبة أعلى منك أو مساوية لك.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # إرسال رسالة خاصة للعضو
            try:
                dm_embed = discord.Embed(
                    title="🔨 تم حظرك من السيرفر",
                    description=f"**السيرفر:** {interaction.guild.name}\n**السبب:** {reason}",
                    color=discord.Color.red()
                )
                await member.send(embed=dm_embed)
            except:
                pass
            
            await member.ban(reason=f"بواسطة {interaction.user}: {reason}")
            
            embed = discord.Embed(
                title="🔨 تم حظر العضو بنجاح",
                color=discord.Color.red()
            )
            embed.add_field(name="👤 العضو المحظور", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{interaction.user.mention}", inline=True)
            embed.add_field(name="📝 السبب", value=reason, inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لحظر هذا العضو.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="طرد", description="طرد عضو من السيرفر")
    @app_commands.describe(member="العضو المراد طرده", reason="سبب الطرد")
    async def kick_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "لم يتم تحديد سبب"):
        if not interaction.user.guild_permissions.kick_members:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لطرد الأعضاء.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            await member.kick(reason=f"بواسطة {interaction.user}: {reason}")
            
            embed = discord.Embed(
                title="👢 تم طرد العضو بنجاح",
                color=discord.Color.orange()
            )
            embed.add_field(name="👤 العضو المطرود", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{interaction.user.mention}", inline=True)
            embed.add_field(name="📝 السبب", value=reason, inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لطرد هذا العضو.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="كتم", description="كتم عضو لفترة محددة")
    @app_commands.describe(member="العضو المراد كتمه", duration="مدة الكتم (مثال: 10د, 2س, 1ي)", reason="سبب الكتم")
    async def mute_slash(interaction: discord.Interaction, member: discord.Member, duration: str = None, reason: str = "لم يتم تحديد سبب"):
        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لكتم الأعضاء.",
                color=discord.Color.red()
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
                muted_role = await interaction.guild.create_role(name="Muted", reason="رول الكتم التلقائي")
                
                for channel in interaction.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False)
            
            await member.add_roles(muted_role, reason=f"بواسطة {interaction.user}: {reason}")
            add_muted_user(interaction.guild.id, member.id)
            
            embed = discord.Embed(
                title="🔇 تم كتم العضو بنجاح",
                color=discord.Color.red()
            )
            embed.add_field(name="👤 العضو المكتوم", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{interaction.user.mention}", inline=True)
            embed.add_field(name="⏰ المدة", value=duration_text, inline=True)
            embed.add_field(name="📝 السبب", value=reason, inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لكتم هذا العضو.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="فك_كتم", description="فك كتم عضو")
    @app_commands.describe(member="العضو المراد فك كتمه")
    async def unmute_slash(interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لفك كتم الأعضاء.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        
        if not muted_role or muted_role not in member.roles:
            embed = discord.Embed(
                title="❌ العضو غير مكتوم",
                description="العضو المحدد ليس مكتوماً حالياً.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            await member.remove_roles(muted_role, reason=f"فك كتم بواسطة {interaction.user}")
            remove_muted_user(interaction.guild.id, member.id)
            
            embed = discord.Embed(
                title="🔊 تم فك الكتم بنجاح",
                color=discord.Color.green()
            )
            embed.add_field(name="👤 العضو", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{interaction.user.mention}", inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لفك كتم هذا العضو.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="تحذير", description="إعطاء تحذير لعضو")
    @app_commands.describe(member="العضو المراد تحذيره", reason="سبب التحذير")
    async def warn_slash(interaction: discord.Interaction, member: discord.Member, reason: str):
        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لإعطاء تحذيرات.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        import uuid
        warning_id = str(uuid.uuid4())[:8]
        warning_data = {
            'id': warning_id,
            'reason': reason,
            'moderator': str(interaction.user),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        add_warning(interaction.guild.id, member.id, warning_data)
        
        warnings = get_user_warnings(interaction.guild.id, member.id)
        warning_count = len(warnings)
        
        embed = discord.Embed(
            title="⚠️ تم إعطاء تحذير",
            color=discord.Color.yellow()
        )
        embed.add_field(name="👤 العضو", value=f"{member.mention}", inline=True)
        embed.add_field(name="👮 بواسطة", value=f"{interaction.user.mention}", inline=True)
        embed.add_field(name="🔢 رقم التحذير", value=f"#{warning_count}", inline=True)
        embed.add_field(name="📝 السبب", value=reason, inline=False)
        
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="التحذيرات", description="عرض تحذيرات عضو")
    @app_commands.describe(member="العضو (اختياري)")
    async def warnings_slash(interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        warnings = get_user_warnings(interaction.guild.id, member.id)
        
        if not warnings:
            embed = discord.Embed(
                title="📊 تحذيرات العضو",
                description=f"{member.mention} لا يملك أي تحذيرات.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        embed = discord.Embed(
            title="📊 قائمة التحذيرات",
            description=f"تحذيرات العضو {member.mention}",
            color=discord.Color.orange()
        )
        
        for i, warning in enumerate(warnings[:5], 1):  # عرض أول 5 تحذيرات فقط
            timestamp = datetime.fromisoformat(warning['timestamp'])
            embed.add_field(
                name=f"⚠️ التحذير #{i}",
                value=f"**السبب:** {warning['reason'][:50]}{'...' if len(warning['reason']) > 50 else ''}\n**المشرف:** {warning['moderator']}\n**التاريخ:** {timestamp.strftime('%Y-%m-%d')}",
                inline=False
            )
        
        embed.set_footer(text=f"إجمالي التحذيرات: {len(warnings)}")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="مسح", description="حذف عدد معين من الرسائل")
    @app_commands.describe(amount="عدد الرسائل المراد حذفها")
    async def purge_slash(interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="ليس لديك الصلاحيات المطلوبة لحذف الرسائل.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if amount <= 0 or amount > 100:
            embed = discord.Embed(
                title="❌ عدد خاطئ",
                description="يجب أن يكون العدد بين 1 و 100.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        deleted = await interaction.channel.purge(limit=amount)
        
        embed = discord.Embed(
            title="🗑️ تم حذف الرسائل",
            description=f"تم حذف {len(deleted)} رسالة بنجاح.",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="معلومات", description="عرض معلومات عضو أو السيرفر")
    @app_commands.describe(member="العضو (اختياري)")
    async def info_slash(interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            # معلومات السيرفر
            guild = interaction.guild
            
            embed = discord.Embed(
                title=f"🏠 معلومات السيرفر: {guild.name}",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="👑 المالك",
                value=f"{guild.owner.mention}" if guild.owner else "غير محدد",
                inline=True
            )
            
            embed.add_field(
                name="👥 الأعضاء",
                value=str(guild.member_count),
                inline=True
            )
            
            embed.add_field(
                name="📍 القنوات",
                value=f"{len(guild.text_channels + guild.voice_channels)}",
                inline=True
            )
            
            embed.add_field(
                name="📅 تاريخ الإنشاء",
                value=guild.created_at.strftime('%Y-%m-%d'),
                inline=True
            )
            
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
        else:
            # معلومات العضو
            embed = discord.Embed(
                title=f"👤 معلومات العضو: {member.display_name}",
                color=member.color if member.color != discord.Color.default() else discord.Color.blue()
            )
            
            embed.add_field(
                name="📋 المعلومات الأساسية",
                value=f"**الاسم:** {member}\n**المعرف:** {member.id}",
                inline=False
            )
            
            embed.add_field(
                name="📅 التواريخ",
                value=f"**إنشاء الحساب:** {member.created_at.strftime('%Y-%m-%d')}\n**انضمام للسيرفر:** {member.joined_at.strftime('%Y-%m-%d') if member.joined_at else 'غير محدد'}",
                inline=False
            )
            
            warnings = get_user_warnings(interaction.guild.id, member.id)
            embed.add_field(
                name="⚠️ التحذيرات",
                value=str(len(warnings)),
                inline=True
            )
            
            if member.avatar:
                embed.set_thumbnail(url=member.avatar.url)
        
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="إعدادات", description="إدارة إعدادات السيرفر")
    async def settings_slash(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ ليس لديك صلاحية",
                description="تحتاج لصلاحيات المدير لإدارة الإعدادات.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        config = get_guild_config(interaction.guild.id)
        
        embed = discord.Embed(
            title="⚙️ إعدادات السيرفر",
            description="الإعدادات الحالية للسيرفر",
            color=discord.Color.blue()
        )
        
        logs_channel = bot.get_channel(config.get('logs_channel')) if config.get('logs_channel') else None
        
        embed.add_field(
            name="📊 نظام اللوقات",
            value=f"**الحالة:** {'مفعل' if config.get('logs_enabled') else 'معطل'}\n**القناة:** {logs_channel.mention if logs_channel else 'غير محددة'}",
            inline=False
        )
        
        embed.add_field(
            name="📈 الإحصائيات",
            value=f"**التحذيرات:** {len(config.get('warnings', {}))}\n**المكتومين:** {len(config.get('muted_users', []))}",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="بنق", description="فحص سرعة البوت")
    async def ping_slash(interaction: discord.Interaction):
        latency = round(bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 بونج!",
            description=f"زمن الاستجابة: **{latency}ms**",
            color=discord.Color.green() if latency < 100 else discord.Color.orange() if latency < 300 else discord.Color.red()
        )
        
        await interaction.response.send_message(embed=embed)
