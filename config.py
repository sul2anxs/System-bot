import json
import os
from typing import Dict, Any

DATABASE_FILE = "database.json"

def load_config() -> Dict[str, Any]:
    """تحميل الإعدادات من ملف JSON"""
    if not os.path.exists(DATABASE_FILE):
        return {}
    
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("⚠️ خطأ في قراءة ملف قاعدة البيانات، سيتم إنشاء ملف جديد.")
        return {}

def save_config(config: Dict[str, Any]) -> None:
    """حفظ الإعدادات في ملف JSON"""
    try:
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ خطأ في حفظ قاعدة البيانات: {e}")

def get_guild_config(guild_id: int) -> Dict[str, Any]:
    """الحصول على إعدادات سيرفر معين"""
    config = load_config()
    guild_id_str = str(guild_id)
    
    if guild_id_str not in config:
        # إنشاء إعدادات افتراضية للسيرفر الجديد
        default_config = {
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
        config[guild_id_str] = default_config
        save_config(config)
        return default_config
    
    return config[guild_id_str]

def update_guild_config(guild_id: int, updates: Dict[str, Any]) -> None:
    """تحديث إعدادات سيرفر معين"""
    config = load_config()
    guild_id_str = str(guild_id)
    
    if guild_id_str not in config:
        config[guild_id_str] = get_guild_config(guild_id)
    
    config[guild_id_str].update(updates)
    save_config(config)

def add_warning(guild_id: int, user_id: int, warning_data: Dict[str, Any]) -> None:
    """إضافة تحذير لعضو"""
    config = load_config()
    guild_id_str = str(guild_id)
    user_id_str = str(user_id)
    
    if guild_id_str not in config:
        config[guild_id_str] = get_guild_config(guild_id)
    
    if 'warnings' not in config[guild_id_str]:
        config[guild_id_str]['warnings'] = {}
    
    if user_id_str not in config[guild_id_str]['warnings']:
        config[guild_id_str]['warnings'][user_id_str] = []
    
    config[guild_id_str]['warnings'][user_id_str].append(warning_data)
    save_config(config)

def remove_warning(guild_id: int, user_id: int, warning_id: str) -> Dict[str, Any] | None:
    """إزالة تحذير معين لعضو"""
    config = load_config()
    guild_id_str = str(guild_id)
    user_id_str = str(user_id)
    
    if (guild_id_str not in config or 
        'warnings' not in config[guild_id_str] or 
        user_id_str not in config[guild_id_str]['warnings']):
        return None
    
    warnings = config[guild_id_str]['warnings'][user_id_str]
    
    for i, warning in enumerate(warnings):
        if warning['id'] == warning_id:
            removed_warning = warnings.pop(i)
            save_config(config)
            return removed_warning
    
    return None

def get_user_warnings(guild_id: int, user_id: int) -> list:
    """الحصول على قائمة تحذيرات عضو"""
    config = load_config()
    guild_id_str = str(guild_id)
    user_id_str = str(user_id)
    
    if (guild_id_str not in config or 
        'warnings' not in config[guild_id_str] or 
        user_id_str not in config[guild_id_str]['warnings']):
        return []
    
    return config[guild_id_str]['warnings'][user_id_str]

def add_muted_user(guild_id: int, user_id: int) -> None:
    """إضافة عضو لقائمة المكتومين"""
    config = load_config()
    guild_id_str = str(guild_id)
    
    if guild_id_str not in config:
        config[guild_id_str] = get_guild_config(guild_id)
    
    if 'muted_users' not in config[guild_id_str]:
        config[guild_id_str]['muted_users'] = []
    
    if user_id not in config[guild_id_str]['muted_users']:
        config[guild_id_str]['muted_users'].append(user_id)
        save_config(config)

def remove_muted_user(guild_id: int, user_id: int) -> None:
    """إزالة عضو من قائمة المكتومين"""
    config = load_config()
    guild_id_str = str(guild_id)
    
    if (guild_id_str in config and 
        'muted_users' in config[guild_id_str] and 
        user_id in config[guild_id_str]['muted_users']):
        
        config[guild_id_str]['muted_users'].remove(user_id)
        save_config(config)

def is_user_muted(guild_id: int, user_id: int) -> bool:
    """التحقق من كون العضو مكتوماً"""
    config = load_config()
    guild_id_str = str(guild_id)
    
    if (guild_id_str in config and 
        'muted_users' in config[guild_id_str]):
        return user_id in config[guild_id_str]['muted_users']
    
    return False

def get_logs_channel(guild_id: int) -> int | None:
    """الحصول على ID قناة اللوقات"""
    config = load_config()
    guild_id_str = str(guild_id)
    
    if guild_id_str in config:
        return config[guild_id_str].get('logs_channel')
    
    return None

def set_logs_channel(guild_id: int, channel_id: int) -> None:
    """تعيين قناة اللوقات"""
    config = load_config()
    guild_id_str = str(guild_id)
    
    if guild_id_str not in config:
        config[guild_id_str] = get_guild_config(guild_id)
    
    config[guild_id_str]['logs_channel'] = channel_id
    save_config(config)

def toggle_logs(guild_id: int, enabled: bool) -> None:
    """تفعيل أو إيقاف نظام اللوقات"""
    config = load_config()
    guild_id_str = str(guild_id)
    
    if guild_id_str not in config:
        config[guild_id_str] = get_guild_config(guild_id)
    
    config[guild_id_str]['logs_enabled'] = enabled
    save_config(config)

def is_logs_enabled(guild_id: int) -> bool:
    """التحقق من تفعيل نظام اللوقات"""
    config = load_config()
    guild_id_str = str(guild_id)
    
    if guild_id_str in config:
        return config[guild_id_str].get('logs_enabled', True)
    
    return True

def update_log_setting(guild_id: int, setting_name: str, enabled: bool) -> None:
    """تحديث إعداد معين في نظام اللوقات"""
    config = load_config()
    guild_id_str = str(guild_id)
    
    if guild_id_str not in config:
        config[guild_id_str] = get_guild_config(guild_id)
    
    if 'logs_settings' not in config[guild_id_str]:
        config[guild_id_str]['logs_settings'] = {}
    
    config[guild_id_str]['logs_settings'][setting_name] = enabled
    save_config(config)

def get_log_setting(guild_id: int, setting_name: str) -> bool:
    """الحصول على إعداد معين في نظام اللوقات"""
    config = load_config()
    guild_id_str = str(guild_id)
    
    if (guild_id_str in config and 
        'logs_settings' in config[guild_id_str]):
        return config[guild_id_str]['logs_settings'].get(setting_name, True)
    
    return True