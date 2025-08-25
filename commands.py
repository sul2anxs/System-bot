import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
import uuid
from config import *

def setup_commands(bot, logs_system, deleted_messages_cache):
    
    @bot.command(name='مساعدة', aliases=['help'])
    async def help_command(ctx):
        """عرض قائمة الأوامر المتاحة"""
        embed = discord.Embed(
            title="🤖 أوامر البوت العربي المتقدم",
            description="قائمة شاملة بجميع أوامر البوت المتاحة",
            color=discord.Color.blue()
        )
        
        # أوامر الإدارة
        admin_commands = [
            "`!حظر @عضو [السبب]` - حظر عضو من السيرفر",
            "`!فك_حظر معرف_العضو [السبب]` - فك حظر عضو",
            "`!طرد @عضو [السبب]` - طرد عضو من السيرفر",
            "`!كتم @عضو [المدة] [السبب]` - كتم عضو",
            "`!فك_كتم @عضو` - فك كتم عضو",
            "`!تحذير @عضو السبب` - إعطاء تحذير لعضو",
            "`!التحذيرات @عضو` - عرض تحذيرات عضو",
            "`!حذف_تحذير @عضو معرف_التحذير` - حذف تحذير معين"
        ]
        
        embed.add_field(
            name="⚡ أوامر الإدارة",
            value="\n".join(admin_commands),
            inline=False
        )
        
        # أوامر التحكم
        control_commands = [
            "`!مسح عدد` - حذف عدد من الرسائل",
            "`!استرداد معرف_الرسالة` - استرداد رسالة محذوفة",
            "`!تعيين_لوقات #قناة` - تعيين قناة اللوقات",
            "`!معلومات [@عضو]` - عرض معلومات عضو",
            "`!سيرفر` - معلومات السيرفر"
        ]
        
        embed.add_field(
            name="🔧 أوامر التحكم",
            value="\n".join(control_commands),
            inline=False
        )
        
        # أوامر عامة
        general_commands = [
            "`!بنق` - فحص سرعة البوت",
            "`!وقت` - عرض الوقت الحالي",
            "`!مساعدة` - عرض هذه القائمة"
        ]
        
        embed.add_field(
            name="📋 أوامر عامة",
            value="\n".join(general_commands),
            inline=False
        )
        
        embed.set_footer(text="💡 يمكنك أيضاً استخدام أوامر Slash بكتابة /")
        await ctx.send(embed=embed)

    @bot.command(name='حظر', aliases=['ban'])
    @commands.has_permissions(ban_members=True)
    async def ban_member(ctx, member: discord.Member, *, reason="لم يتم تحديد سبب"):
        """حظر عضو من السيرفر"""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="❌ خطأ في الصلاحيات",
                description="لا يمكنك حظر عضو يملك رتبة أعلى منك أو مساوية لك.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ خطأ",
                description="لا يمكنك حظر نفسك!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        try:
            # إرسال رسالة خاصة للعضو المحظور
            try:
                dm_embed = discord.Embed(
                    title="🔨 تم حظرك من السيرفر",
                    description=f"**السيرفر:** {ctx.guild.name}\n**السبب:** {reason}",
                    color=discord.Color.red()
                )
                await member.send(embed=dm_embed)
            except:
                pass  # تجاهل إذا كانت الرسائل الخاصة مغلقة
            
            await member.ban(reason=f"بواسطة {ctx.author}: {reason}")
            
            embed = discord.Embed(
                title="🔨 تم حظر العضو بنجاح",
                color=discord.Color.red()
            )
            embed.add_field(name="👤 العضو المحظور", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="📝 السبب", value=reason, inline=False)
            embed.set_footer(text=f"معرف العضو: {member.id}")
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لحظر هذا العضو.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @bot.command(name='فك_حظر', aliases=['unban'])
    @commands.has_permissions(ban_members=True)
    async def unban_member(ctx, user_id: int, *, reason="لم يتم تحديد سبب"):
        """فك حظر عضو"""
        try:
            user = await bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=f"بواسطة {ctx.author}: {reason}")
            
            embed = discord.Embed(
                title="✅ تم فك الحظر بنجاح",
                color=discord.Color.green()
            )
            embed.add_field(name="👤 العضو", value=f"{user.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="📝 السبب", value=reason, inline=False)
            
            await ctx.send(embed=embed)
            
        except discord.NotFound:
            embed = discord.Embed(
                title="❌ لم يتم العثور على العضو",
                description="العضو المحدد غير محظور أو غير موجود.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لفك حظر الأعضاء.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @bot.command(name='طرد', aliases=['kick'])
    @commands.has_permissions(kick_members=True)
    async def kick_member(ctx, member: discord.Member, *, reason="لم يتم تحديد سبب"):
        """طرد عضو من السيرفر"""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="❌ خطأ في الصلاحيات",
                description="لا يمكنك طرد عضو يملك رتبة أعلى منك أو مساوية لك.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ خطأ",
                description="لا يمكنك طرد نفسك!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        try:
            # إرسال رسالة خاصة للعضو المطرود
            try:
                dm_embed = discord.Embed(
                    title="👢 تم طردك من السيرفر",
                    description=f"**السيرفر:** {ctx.guild.name}\n**السبب:** {reason}",
                    color=discord.Color.orange()
                )
                await member.send(embed=dm_embed)
            except:
                pass
            
            await member.kick(reason=f"بواسطة {ctx.author}: {reason}")
            
            embed = discord.Embed(
                title="👢 تم طرد العضو بنجاح",
                color=discord.Color.orange()
            )
            embed.add_field(name="👤 العضو المطرود", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="📝 السبب", value=reason, inline=False)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لطرد هذا العضو.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @bot.command(name='كتم', aliases=['mute'])
    @commands.has_permissions(manage_messages=True)
    async def mute_member(ctx, member: discord.Member, duration=None, *, reason="لم يتم تحديد سبب"):
        """كتم عضو لفترة معينة"""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="❌ خطأ في الصلاحيات",
                description="لا يمكنك كتم عضو يملك رتبة أعلى منك أو مساوية لك.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # تحويل المدة إلى ثوان
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
                else:
                    mute_seconds = int(duration) * 60  # افتراضي دقائق
                    duration_text = f"{duration} دقيقة"
            except ValueError:
                mute_seconds = None
        
        try:
            # إنشاء أو العثور على رول الكتم
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not muted_role:
                muted_role = await ctx.guild.create_role(name="Muted", reason="رول الكتم التلقائي")
                
                # إعداد صلاحيات الرول في جميع القنوات
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False)
            
            await member.add_roles(muted_role, reason=f"بواسطة {ctx.author}: {reason}")
            add_muted_user(ctx.guild.id, member.id)
            
            embed = discord.Embed(
                title="🔇 تم كتم العضو بنجاح",
                color=discord.Color.red()
            )
            embed.add_field(name="👤 العضو المكتوم", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="⏰ المدة", value=duration_text, inline=True)
            embed.add_field(name="📝 السبب", value=reason, inline=False)
            
            await ctx.send(embed=embed)
            
            # إزالة الكتم تلقائياً بعد المدة المحددة
            if mute_seconds:
                await asyncio.sleep(mute_seconds)
                if muted_role in member.roles:
                    await member.remove_roles(muted_role, reason="انتهاء مدة الكتم")
                    remove_muted_user(ctx.guild.id, member.id)
                    
                    unmute_embed = discord.Embed(
                        title="🔊 تم فك الكتم تلقائياً",
                        description=f"تم فك كتم {member.mention} بعد انتهاء المدة المحددة.",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=unmute_embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لكتم هذا العضو.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @bot.command(name='فك_كتم', aliases=['unmute'])
    @commands.has_permissions(manage_messages=True)
    async def unmute_member(ctx, member: discord.Member):
        """فك كتم عضو"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if not muted_role or muted_role not in member.roles:
            embed = discord.Embed(
                title="❌ العضو غير مكتوم",
                description="العضو المحدد ليس مكتوماً حالياً.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        try:
            await member.remove_roles(muted_role, reason=f"فك كتم بواسطة {ctx.author}")
            remove_muted_user(ctx.guild.id, member.id)
            
            embed = discord.Embed(
                title="🔊 تم فك الكتم بنجاح",
                color=discord.Color.green()
            )
            embed.add_field(name="👤 العضو", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لفك كتم هذا العضو.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @bot.command(name='تحذير', aliases=['warn'])
    @commands.has_permissions(manage_messages=True)
    async def warn_member(ctx, member: discord.Member, *, reason):
        """إعطاء تحذير لعضو"""
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ خطأ",
                description="لا يمكنك تحذير نفسك!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        warning_id = str(uuid.uuid4())[:8]
        warning_data = {
            'id': warning_id,
            'reason': reason,
            'moderator': str(ctx.author),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        add_warning(ctx.guild.id, member.id, warning_data)
        
        # الحصول على عدد التحذيرات الكلي
        warnings = get_user_warnings(ctx.guild.id, member.id)
        warning_count = len(warnings)
        
        embed = discord.Embed(
            title="⚠️ تم إعطاء تحذير",
            color=discord.Color.yellow()
        )
        embed.add_field(name="👤 العضو", value=f"{member.mention}", inline=True)
        embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
        embed.add_field(name="🔢 رقم التحذير", value=f"#{warning_count}", inline=True)
        embed.add_field(name="📝 السبب", value=reason, inline=False)
        embed.add_field(name="🆔 معرف التحذير", value=warning_id, inline=True)
        
        await ctx.send(embed=embed)
        
        # إرسال رسالة خاصة للعضو
        try:
            dm_embed = discord.Embed(
                title="⚠️ تلقيت تحذيراً",
                description=f"**السيرفر:** {ctx.guild.name}\n**السبب:** {reason}",
                color=discord.Color.yellow()
            )
            dm_embed.add_field(name="📊 عدد التحذيرات", value=f"{warning_count}", inline=True)
            await member.send(embed=dm_embed)
        except:
            pass

    @bot.command(name='التحذيرات', aliases=['warnings'])
    async def show_warnings(ctx, member: discord.Member = None):
        """عرض تحذيرات عضو"""
        if member is None:
            member = ctx.author
        
        warnings = get_user_warnings(ctx.guild.id, member.id)
        
        if not warnings:
            embed = discord.Embed(
                title="📊 تحذيرات العضو",
                description=f"{member.mention} لا يملك أي تحذيرات.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="📊 قائمة التحذيرات",
            description=f"تحذيرات العضو {member.mention}",
            color=discord.Color.orange()
        )
        
        for i, warning in enumerate(warnings, 1):
            timestamp = datetime.fromisoformat(warning['timestamp'])
            embed.add_field(
                name=f"⚠️ التحذير #{i}",
                value=f"**السبب:** {warning['reason']}\n**المشرف:** {warning['moderator']}\n**التاريخ:** {timestamp.strftime('%Y-%m-%d %H:%M')}\n**المعرف:** {warning['id']}",
                inline=False
            )
        
        embed.set_footer(text=f"إجمالي التحذيرات: {len(warnings)}")
        await ctx.send(embed=embed)

    @bot.command(name='حذف_تحذير', aliases=['remove_warning'])
    @commands.has_permissions(manage_messages=True)
    async def remove_warning_command(ctx, member: discord.Member, warning_id: str):
        """حذف تحذير معين لعضو"""
        removed = remove_warning(ctx.guild.id, member.id, warning_id)
        
        if not removed:
            embed = discord.Embed(
                title="❌ تحذير غير موجود",
                description="لم يتم العثور على التحذير المحدد.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="✅ تم حذف التحذير",
            color=discord.Color.green()
        )
        embed.add_field(name="👤 العضو", value=f"{member.mention}", inline=True)
        embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
        embed.add_field(name="📝 سبب التحذير المحذوف", value=removed['reason'], inline=False)
        
        await ctx.send(embed=embed)

    @bot.command(name='مسح', aliases=['purge', 'clear'])
    @commands.has_permissions(manage_messages=True)
    async def purge_messages(ctx, amount: int):
        """حذف عدد معين من الرسائل"""
        if amount <= 0 or amount > 100:
            embed = discord.Embed(
                title="❌ عدد خاطئ",
                description="يجب أن يكون العدد بين 1 و 100.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 لحذف أمر المسح نفسه
        
        embed = discord.Embed(
            title="🗑️ تم حذف الرسائل",
            description=f"تم حذف {len(deleted) - 1} رسالة بنجاح.",
            color=discord.Color.green()
        )
        
        confirmation = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await confirmation.delete()

    @bot.command(name='استرداد', aliases=['recover'])
    @commands.has_permissions(manage_messages=True)
    async def recover_message(ctx, message_id: int):
        """استرداد رسالة محذوفة"""
        if message_id not in deleted_messages_cache:
            embed = discord.Embed(
                title="❌ رسالة غير موجودة",
                description="لم يتم العثور على الرسالة المحددة في الكاش.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        message_data = deleted_messages_cache[message_id]
        
        embed = discord.Embed(
            title="📩 رسالة محذوفة مستردة",
            color=discord.Color.blue(),
            timestamp=message_data['created_at']
        )
        
        embed.add_field(
            name="👤 المؤلف",
            value=f"{message_data['author'].mention} ({message_data['author']})",
            inline=True
        )
        
        embed.add_field(
            name="📍 القناة",
            value=f"{message_data['channel'].mention}",
            inline=True
        )
        
        if message_data['content']:
            embed.add_field(
                name="📝 المحتوى",
                value=message_data['content'][:1024],
                inline=False
            )
        
        if message_data['attachments']:
            embed.add_field(
                name="📎 المرفقات",
                value="\n".join(message_data['attachments']),
                inline=False
            )
        
        embed.set_footer(text=f"معرف الرسالة: {message_id}")
        await ctx.send(embed=embed)

    @bot.command(name='تعيين_لوقات', aliases=['set_logs'])
    @commands.has_permissions(administrator=True)
    async def set_logs_channel(ctx, channel: discord.TextChannel):
        """تعيين قناة اللوقات"""
        from config import set_logs_channel as config_set_logs_channel
        config_set_logs_channel(ctx.guild.id, channel.id)
        
        embed = discord.Embed(
            title="✅ تم تعيين قناة اللوقات",
            description=f"تم تعيين {channel.mention} كقناة اللوقات للسيرفر.",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)

    @bot.command(name='معلومات', aliases=['info', 'userinfo'])
    async def user_info(ctx, member: discord.Member = None):
        """عرض معلومات عضو"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"👤 معلومات العضو: {member.display_name}",
            color=member.color if member.color != discord.Color.default() else discord.Color.blue()
        )
        
        embed.add_field(
            name="📋 المعلومات الأساسية",
            value=f"**الاسم:** {member}\n**الاسم المستعار:** {member.display_name}\n**المعرف:** {member.id}",
            inline=False
        )
        
        embed.add_field(
            name="📅 التواريخ",
            value=f"**إنشاء الحساب:** {member.created_at.strftime('%Y-%m-%d')}\n**انضمام للسيرفر:** {member.joined_at.strftime('%Y-%m-%d') if member.joined_at else 'غير محدد'}",
            inline=False
        )
        
        embed.add_field(
            name="🎭 الأدوار",
            value=" ".join([role.mention for role in member.roles[1:]]) if len(member.roles) > 1 else "لا توجد أدوار",
            inline=False
        )
        
        # عرض التحذيرات
        warnings = get_user_warnings(ctx.guild.id, member.id)
        embed.add_field(
            name="⚠️ التحذيرات",
            value=str(len(warnings)),
            inline=True
        )
        
        # حالة الكتم
        embed.add_field(
            name="🔇 حالة الكتم",
            value="مكتوم" if is_user_muted(ctx.guild.id, member.id) else "غير مكتوم",
            inline=True
        )
        
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        
        await ctx.send(embed=embed)

    @bot.command(name='سيرفر', aliases=['server', 'serverinfo'])
    async def server_info(ctx):
        """عرض معلومات السيرفر"""
        guild = ctx.guild
        
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
            value=f"**الكل:** {guild.member_count}\n**البشر:** {len([m for m in guild.members if not m.bot])}\n**البوتات:** {len([m for m in guild.members if m.bot])}",
            inline=True
        )
        
        embed.add_field(
            name="📍 القنوات",
            value=f"**النصية:** {len(guild.text_channels)}\n**الصوتية:** {len(guild.voice_channels)}\n**الفئات:** {len(guild.categories)}",
            inline=True
        )
        
        embed.add_field(
            name="🎭 الأدوار",
            value=str(len(guild.roles)),
            inline=True
        )
        
        embed.add_field(
            name="📅 تاريخ الإنشاء",
            value=guild.created_at.strftime('%Y-%m-%d'),
            inline=True
        )
        
        embed.add_field(
            name="🆔 معرف السيرفر",
            value=str(guild.id),
            inline=True
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await ctx.send(embed=embed)

    @bot.command(name='بنق', aliases=['ping'])
    async def ping(ctx):
        """فحص سرعة البوت"""
        latency = round(bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 بونج!",
            description=f"زمن الاستجابة: **{latency}ms**",
            color=discord.Color.green() if latency < 100 else discord.Color.orange() if latency < 300 else discord.Color.red()
        )
        
        await ctx.send(embed=embed)

    @bot.command(name='وقت', aliases=['time'])
    async def current_time(ctx):
        """عرض الوقت الحالي"""
        now = datetime.utcnow()
        
        embed = discord.Embed(
            title="🕐 الوقت الحالي",
            description=f"**UTC:** {now.strftime('%Y-%m-%d %H:%M:%S')}",
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)
