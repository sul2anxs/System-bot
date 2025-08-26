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
            color=0x7289DA,
            timestamp=datetime.utcnow()
        )
        
        # أوامر الإدارة (بدون بريفكس)
        admin_commands = [
            "🔨 `رزق @عضو` - حظر عضو من السيرفر",
            "🔨 `زووط @عضو` - حظر عضو من السيرفر", 
            "🔨 `طع @عضو` - طرد عضو من السيرفر",
            "🔨 `بنعالي @عضو` - حظر عضو من السيرفر",
            "🔇 `اص @عضو [المدة]` - كتم عضو",
            "🔇 `اسكت @عضو [المدة]` - كتم عضو",
            "🔇 `اسكات @عضو [المدة]` - كتم عضو",
            "🔊 `تحدث @عضو` - فك كتم عضو",
            "⚠️ `تحذير @عضو السبب` - إعطاء تحذير لعضو",
            "✅ `تعال معرف_العضو` - فك حظر عضو",
            "🎭 `رول @عضو اسم_الرتبة` - إعطاء رتبة لعضو",
            "🔒 `قفل` - قفل الروم الحالي",
            "🔓 `فتح` - فتح الروم الحالي"
        ]
        
        embed.add_field(
            name="⚡ أوامر الإدارة (بدون بريفكس)",
            value="\n".join(admin_commands),
            inline=False
        )
        
        # أوامر التحكم
        control_commands = [
            "🗑️ `!مسح عدد` - حذف عدد من الرسائل",
            "♻️ `رجع معرف_الرسالة` - استرداد رسالة محذوفة",
            "📊 `!تعيين_لوقات #قناة` - تعيين قناة اللوقات",
            "👤 `inf @عضو` - عرض معلومات عضو",
            "🏰 `!سيرفر` - معلومات السيرفر",
            "📋 `!التحذيرات @عضو` - عرض تحذيرات عضو",
            "🗑️ `!حذف_تحذير @عضو معرف_التحذير` - حذف تحذير معين"
        ]
        
        embed.add_field(
            name="🔧 أوامر التحكم",
            value="\n".join(control_commands),
            inline=False
        )
        
        # أوامر عامة
        general_commands = [
            "🏓 `!بنق` - فحص سرعة البوت",
            "🕐 `!وقت` - عرض الوقت الحالي",
            "ℹ️ `!مساعدة` - عرض هذه القائمة"
        ]
        
        embed.add_field(
            name="📋 أوامر عامة",
            value="\n".join(general_commands),
            inline=False
        )
        
        embed.set_footer(
            text="💡 الأوامر الإدارية تعمل بدون علامة ! • يمكنك أيضاً استخدام أوامر Slash بكتابة /",
            icon_url=bot.user.avatar.url if bot.user and bot.user.avatar else None
        )
        embed.set_thumbnail(url=bot.user.avatar.url if bot.user and bot.user.avatar else None)
        await ctx.send(embed=embed)

    # ═══════════════════════════════════════════════════════════════
    # أوامر الحظر الجديدة (بدون بريفكس وبدون سبب)
    # ═══════════════════════════════════════════════════════════════
    
    @bot.command(name='رزق')
    @commands.has_permissions(ban_members=True)
    async def ban_razq(ctx, member: discord.Member):
        """حظر عضو من السيرفر - أمر رزق"""
        await execute_ban(ctx, member, "تم الحظر")

    @bot.command(name='زووط')
    @commands.has_permissions(ban_members=True)
    async def ban_zoot(ctx, member: discord.Member):
        """حظر عضو من السيرفر - أمر زووط"""
        await execute_ban(ctx, member, "تم الحظر")

    @bot.command(name='بنعالي')
    @commands.has_permissions(ban_members=True)
    async def ban_baneali(ctx, member: discord.Member):
        """حظر عضو من السيرفر - أمر بنعالي"""
        await execute_ban(ctx, member, "تم الحظر")

    async def execute_ban(ctx, member: discord.Member, reason: str):
        """تنفيذ عملية الحظر"""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="❌ خطأ في الصلاحيات",
                description="لا يمكنك حظر عضو يملك رتبة أعلى منك أو مساوية لك.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ خطأ",
                description="لا يمكنك حظر نفسك!",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        try:
            # إرسال رسالة خاصة للعضو المحظور
            try:
                dm_embed = discord.Embed(
                    title="🔨 تم حظرك من السيرفر",
                    description=f"**السيرفر:** {ctx.guild.name}\n**بواسطة:** {ctx.author.display_name}",
                    color=0xFF4444,
                    timestamp=datetime.utcnow()
                )
                dm_embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
                await member.send(embed=dm_embed)
            except:
                pass
            
            await member.ban(reason=f"بواسطة {ctx.author}")
            
            embed = discord.Embed(
                title="🔨 تم حظر العضو بنجاح",
                color=0xFF4444,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 العضو المحظور", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="📅 التاريخ", value=f"<t:{int(datetime.utcnow().timestamp())}:f>", inline=True)
            embed.set_footer(text=f"معرف العضو: {member.id}")
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لحظر هذا العضو.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    # ═══════════════════════════════════════════════════════════════
    # أوامر فك الحظر (بدون بريفكس وبدون سبب)
    # ═══════════════════════════════════════════════════════════════
    
    @bot.command(name='تعال')
    @commands.has_permissions(ban_members=True)
    async def unban_taaal(ctx, user_id: int):
        """فك حظر عضو - أمر تعال"""
        try:
            user = await bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=f"فك حظر بواسطة {ctx.author}")
            
            embed = discord.Embed(
                title="✅ تم فك الحظر بنجاح",
                color=0x00FF7F,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 العضو", value=f"{user.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="📅 التاريخ", value=f"<t:{int(datetime.utcnow().timestamp())}:f>", inline=True)
            embed.set_footer(text=f"معرف العضو: {user.id}")
            embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
            
            await ctx.send(embed=embed)
            
        except discord.NotFound:
            embed = discord.Embed(
                title="❌ لم يتم العثور على العضو",
                description="العضو المحدد غير محظور أو غير موجود.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لفك حظر الأعضاء.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    # ═══════════════════════════════════════════════════════════════
    # أمر الطرد (بدون بريفكس وبدون سبب)
    # ═══════════════════════════════════════════════════════════════
    
    @bot.command(name='طع')
    @commands.has_permissions(kick_members=True)
    async def kick_ta3(ctx, member: discord.Member):
        """طرد عضو من السيرفر - أمر طع"""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="❌ خطأ في الصلاحيات",
                description="لا يمكنك طرد عضو يملك رتبة أعلى منك أو مساوية لك.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ خطأ",
                description="لا يمكنك طرد نفسك!",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        try:
            # إرسال رسالة خاصة للعضو المطرود
            try:
                dm_embed = discord.Embed(
                    title="👢 تم طردك من السيرفر",
                    description=f"**السيرفر:** {ctx.guild.name}\n**بواسطة:** {ctx.author.display_name}",
                    color=0xFFA500,
                    timestamp=datetime.utcnow()
                )
                dm_embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
                await member.send(embed=dm_embed)
            except:
                pass
            
            await member.kick(reason=f"طرد بواسطة {ctx.author}")
            
            embed = discord.Embed(
                title="👢 تم طرد العضو بنجاح",
                color=0xFFA500,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 العضو المطرود", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="📅 التاريخ", value=f"<t:{int(datetime.utcnow().timestamp())}:f>", inline=True)
            embed.set_footer(text=f"معرف العضو: {member.id}")
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لطرد هذا العضو.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    # ═══════════════════════════════════════════════════════════════
    # أوامر الكتم (بدون بريفكس وبدون سبب)
    # ═══════════════════════════════════════════════════════════════
    
    @bot.command(name='اص')
    @commands.has_permissions(manage_messages=True)
    async def mute_as(ctx, member: discord.Member, duration=None):
        """كتم عضو - أمر اص"""
        await execute_mute(ctx, member, duration)

    @bot.command(name='اسكت')
    @commands.has_permissions(manage_messages=True)
    async def mute_asket(ctx, member: discord.Member, duration=None):
        """كتم عضو - أمر اسكت"""
        await execute_mute(ctx, member, duration)

    @bot.command(name='اسكات')
    @commands.has_permissions(manage_messages=True)
    async def mute_askat(ctx, member: discord.Member, duration=None):
        """كتم عضو - أمر اسكات"""
        await execute_mute(ctx, member, duration)

    async def execute_mute(ctx, member: discord.Member, duration=None):
        """تنفيذ عملية الكتم"""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="❌ خطأ في الصلاحيات",
                description="لا يمكنك كتم عضو يملك رتبة أعلى منك أو مساوية لك.",
                color=0xFF0000
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
                muted_role = await ctx.guild.create_role(
                    name="Muted", 
                    color=0x818386,
                    reason="رول الكتم التلقائي"
                )
                
                # إعداد صلاحيات الرول في جميع القنوات
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False, add_reactions=False)
            
            await member.add_roles(muted_role, reason=f"كتم بواسطة {ctx.author}")
            add_muted_user(ctx.guild.id, member.id)
            
            embed = discord.Embed(
                title="🔇 تم كتم العضو بنجاح",
                color=0xFF6B6B,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 العضو المكتوم", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="⏰ المدة", value=duration_text, inline=True)
            embed.add_field(name="📅 التاريخ", value=f"<t:{int(datetime.utcnow().timestamp())}:f>", inline=False)
            embed.set_footer(text=f"معرف العضو: {member.id}")
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            
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
                        color=0x00FF7F,
                        timestamp=datetime.utcnow()
                    )
                    await ctx.send(embed=unmute_embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لكتم هذا العضو.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    # ═══════════════════════════════════════════════════════════════
    # أمر فك الكتم (بدون بريفكس)
    # ═══════════════════════════════════════════════════════════════
    
    @bot.command(name='تحدث')
    @commands.has_permissions(manage_messages=True)
    async def unmute_tahadath(ctx, member: discord.Member):
        """فك كتم عضو - أمر تحدث"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if not muted_role or muted_role not in member.roles:
            embed = discord.Embed(
                title="❌ العضو غير مكتوم",
                description="العضو المحدد ليس مكتوماً حالياً.",
                color=0xFFA500
            )
            await ctx.send(embed=embed)
            return
        
        try:
            await member.remove_roles(muted_role, reason=f"فك كتم بواسطة {ctx.author}")
            remove_muted_user(ctx.guild.id, member.id)
            
            embed = discord.Embed(
                title="🔊 تم فك الكتم بنجاح",
                color=0x00FF7F,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 العضو", value=f"{member.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="📅 التاريخ", value=f"<t:{int(datetime.utcnow().timestamp())}:f>", inline=True)
            embed.set_footer(text=f"معرف العضو: {member.id}")
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لفك كتم هذا العضو.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    # ═══════════════════════════════════════════════════════════════
    # أمر إعطاء الرتب (بدون بريفكس)
    # ═══════════════════════════════════════════════════════════════
    
    @bot.command(name='رول')
    @commands.has_permissions(manage_roles=True)
    async def give_role(ctx, member: discord.Member, *, role_name):
        """إعطاء رتبة لعضو - أمر رول"""
        # البحث عن الرتبة
        role = None
        
        # البحث بالاسم
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        
        # إذا لم يتم العثور بالاسم، جرب بالمعرف
        if not role:
            try:
                role_id = int(role_name)
                role = discord.utils.get(ctx.guild.roles, id=role_id)
            except ValueError:
                pass
        
        # إذا لم يتم العثور على الرتبة
        if not role:
            embed = discord.Embed(
                title="❌ رتبة غير موجودة",
                description=f"لم يتم العثور على رتبة بالاسم أو المعرف: `{role_name}`",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        # التحقق من صلاحيات الرتبة
        if role.position >= ctx.author.top_role.position and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="❌ خطأ في الصلاحيات",
                description="لا يمكنك إعطاء رتبة أعلى من رتبتك أو مساوية لها.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        if role.position >= ctx.guild.me.top_role.position:
            embed = discord.Embed(
                title="❌ خطأ في صلاحيات البوت",
                description="لا يمكنني إعطاء رتبة أعلى من رتبتي.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        # التحقق إذا كان العضو يملك الرتبة بالفعل
        if role in member.roles:
            embed = discord.Embed(
                title="ℹ️ الرتبة موجودة بالفعل",
                description=f"العضو {member.mention} يملك رتبة {role.mention} بالفعل.",
                color=0xFFA500
            )
            await ctx.send(embed=embed)
            return
        
        try:
            await member.add_roles(role, reason=f"إعطاء رتبة بواسطة {ctx.author}")
            
            embed = discord.Embed(
                title="🎭 تم إعطاء الرتبة بنجاح",
                color=0x00FF7F,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 العضو", value=f"{member.mention}", inline=True)
            embed.add_field(name="🎭 الرتبة", value=f"{role.mention}", inline=True)
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="📅 التاريخ", value=f"<t:{int(datetime.utcnow().timestamp())}:f>", inline=False)
            embed.set_footer(text=f"معرف الرتبة: {role.id}")
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لإعطاء هذه الرتبة.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(
                title="❌ خطأ في الشبكة",
                description="حدث خطأ أثناء محاولة إعطاء الرتبة. حاول مرة أخرى.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    # ═══════════════════════════════════════════════════════════════
    # أوامر قفل وفتح الروم (بدون بريفكس)
    # ═══════════════════════════════════════════════════════════════
    
    @bot.command(name='قفل')
    @commands.has_permissions(manage_channels=True)
    async def lock_channel(ctx):
        """قفل الروم الحالي"""
        try:
            await ctx.channel.set_permissions(
                ctx.guild.default_role,
                send_messages=False,
                reason=f"قفل القناة بواسطة {ctx.author}"
            )
            
            embed = discord.Embed(
                title="🔒 تم قفل الروم",
                description=f"تم قفل {ctx.channel.mention} بنجاح.",
                color=0xFF6B6B,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="📅 التاريخ", value=f"<t:{int(datetime.utcnow().timestamp())}:f>", inline=True)
            embed.set_footer(text="يمكن للمشرفين فقط الكتابة الآن")
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لقفل هذه القناة.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    @bot.command(name='فتح')
    @commands.has_permissions(manage_channels=True)
    async def unlock_channel(ctx):
        """فتح الروم الحالي"""
        try:
            await ctx.channel.set_permissions(
                ctx.guild.default_role,
                send_messages=True,
                reason=f"فتح القناة بواسطة {ctx.author}"
            )
            
            embed = discord.Embed(
                title="🔓 تم فتح الروم",
                description=f"تم فتح {ctx.channel.mention} بنجاح.",
                color=0x00FF7F,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👮 بواسطة", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="📅 التاريخ", value=f"<t:{int(datetime.utcnow().timestamp())}:f>", inline=True)
            embed.set_footer(text="يمكن للجميع الكتابة الآن")
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ ليس لدي صلاحية",
                description="ليس لدي الصلاحيات اللازمة لفتح هذه القناة.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    # ═══════════════════════════════════════════════════════════════
    # أمر inf لعرض معلومات العضو
    # ═══════════════════════════════════════════════════════════════

    @bot.command(name='inf')
    async def user_info_inf(ctx, member: discord.Member = None):
        """عرض معلومات عضو - أمر inf"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"👤 معلومات العضو",
            color=member.color if member.color != discord.Color.default() else 0x7289DA,
            timestamp=datetime.utcnow()
        )
        
        embed.set_author(
            name=f"{member.display_name}",
            icon_url=member.avatar.url if member.avatar else None
        )
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        
        # المعلومات الأساسية
        basic_info = f"**الاسم:** {member.name}\n"
        basic_info += f"**العرض:** {member.display_name}\n"
        basic_info += f"**المعرف:** {member.id}\n"
        basic_info += f"**البوت:** {'نعم' if member.bot else 'لا'}"
        
        embed.add_field(
            name="📋 المعلومات الأساسية",
            value=basic_info,
            inline=True
        )
        
        # تواريخ مهمة
        created = f"<t:{int(member.created_at.timestamp())}:f>"
        joined = f"<t:{int(member.joined_at.timestamp())}:f>" if member.joined_at else "غير محدد"
        
        dates_info = f"**إنشاء الحساب:** {created}\n"
        dates_info += f"**انضم للسيرفر:** {joined}"
        
        embed.add_field(
            name="📅 التواريخ",
            value=dates_info,
            inline=True
        )
        
        # الرتب
        roles = [role.mention for role in member.roles[1:]]  # تجاهل @everyone
        if roles:
            roles_text = ", ".join(roles[:5])  # أول 5 رتب
            if len(member.roles) > 6:
                roles_text += f" و {len(member.roles) - 6} رتبة أخرى"
        else:
            roles_text = "لا توجد رتب"
        
        embed.add_field(
            name=f"🎭 الرتب ({len(member.roles) - 1})",
            value=roles_text,
            inline=False
        )
        
        # الصلاحيات المهمة
        perms = member.guild_permissions
        important_perms = []
        
        if perms.administrator:
            important_perms.append("👑 المدير")
        if perms.manage_guild:
            important_perms.append("🏰 إدارة السيرفر")
        if perms.manage_channels:
            important_perms.append("📺 إدارة القنوات")
        if perms.ban_members:
            important_perms.append("🔨 حظر الأعضاء")
        if perms.kick_members:
            important_perms.append("👢 طرد الأعضاء")
        if perms.manage_messages:
            important_perms.append("💬 إدارة الرسائل")
        
        if important_perms:
            embed.add_field(
                name="🔑 الصلاحيات المهمة",
                value=", ".join(important_perms),
                inline=False
            )
        
        # الحالة والنشاط
        status_emoji = {
            "online": "🟢 متصل",
            "idle": "🟡 خامل", 
            "dnd": "🔴 مشغول",
            "offline": "⚫ غير متصل"
        }
        
        status_info = f"**الحالة:** {status_emoji.get(str(member.status), '⚫ غير متصل')}\n"
        status_info += f"**أعلى رتبة:** {member.top_role.mention}"
        
        embed.add_field(
            name="📊 الحالة",
            value=status_info,
            inline=True
        )
        
        embed.set_footer(
            text=f"طُلب بواسطة {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        
        await ctx.send(embed=embed)

    # ═══════════════════════════════════════════════════════════════
    # أمر رجع لاسترداد الرسائل
    # ═══════════════════════════════════════════════════════════════

    @bot.command(name='رجع', aliases=['back'])
    async def recover_message_rejaa(ctx, message_id: int):
        """استرداد رسالة محذوفة - أمر رجع"""
        if message_id not in deleted_messages_cache:
            embed = discord.Embed(
                title="❌ رسالة غير موجودة",
                description="لم يتم العثور على الرسالة المحددة في الكاش.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        message_data = deleted_messages_cache[message_id]
        
        embed = discord.Embed(
            title="📩 رسالة محذوفة مستردة",
            color=0x7289DA,
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
        
        embed.add_field(
            name="🕒 وقت الحذف",
            value=f"<t:{int(datetime.utcnow().timestamp())}:R>",
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
        
        embed.set_footer(
            text=f"معرف الرسالة: {message_id} • طُلب بواسطة {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        
        if hasattr(message_data['author'], 'avatar') and message_data['author'].avatar:
            embed.set_thumbnail(url=message_data['author'].avatar.url)
        
        await ctx.send(embed=embed)

    # باقي الأوامر (التحذير، السيرفر، البنق، إلخ...)
    # يمكن إضافتها حسب الحاجة