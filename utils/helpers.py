"""
دوال مساعدة عامة للمشروع
"""

import os
import json
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# ========================================
# دوال النسخ (الجديدة!)
# ========================================

def add_copy_button(text_to_copy, button_text="📋 نسخ", key="copy"):
    """
    إضافة زر نسخ يعمل باستخدام JavaScript
    
    Args:
        text_to_copy: النص المراد نسخه
        button_text: النص الذي يظهر على الزر
        key: مفتاح فريد للزر
    """
    # تنظيف النص للاستخدام في JavaScript
    clean_text = text_to_copy.replace('`', '\\`').replace('${', '\\${')
    
    copy_script = f"""
    <script>
    function copyText_{key}() {{
        const text = `{clean_text}`;
        navigator.clipboard.writeText(text).then(function() {{
            alert('✅ تم النسخ!');
        }}, function(err) {{
            alert('❌ فشل النسخ: ' + err);
        }});
    }}
    </script>
    <button onclick="copyText_{key}()" style="
        background-color: #5380C2;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1.5rem;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        width: 100%;
        font-family: 'Tajawal', sans-serif;
        transition: all 0.3s;
        margin-top: 0.5rem;
    " onmouseover="this.style.backgroundColor='#3A5A8C'" 
       onmouseout="this.style.backgroundColor='#5380C2'"
    >{button_text}</button>
    """
    
    components.html(copy_script, height=50)

# ========================================
# إدارة الملفات والتخزين
# ========================================

def save_text_to_file(text, prefix, source_path=None):
    """
    حفظ النص في ملف
    
    Args:
        text: النص المراد حفظه
        prefix: بادئة اسم الملف (transcript, translated, tashkeel...)
        source_path: مسار الملف الأصلي (اختياري)
    
    Returns:
        مسار الملف المحفوظ
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if source_path and os.path.exists(source_path):
        # حفظ بجانب الملف الأصلي
        source_dir = os.path.dirname(source_path)
        source_name = os.path.splitext(os.path.basename(source_path))[0]
        filename = f"{source_name}_{prefix}_{timestamp}.txt"
        filepath = os.path.join(source_dir, filename)
    else:
        # حفظ في مجلد output
        os.makedirs('output', exist_ok=True)
        filename = f"{prefix}_{timestamp}.txt"
        filepath = os.path.join('output', filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return filepath

def save_srt_file(text, prefix, source_path=None):
    """
    حفظ النص كملف SRT (ترجمة)
    كل 5 ثوانٍ مقطع
    """
    import re
    
    # تقسيم النص إلى جمل
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if source_path and os.path.exists(source_path):
        source_dir = os.path.dirname(source_path)
        source_name = os.path.splitext(os.path.basename(source_path))[0]
        filename = f"{source_name}_{prefix}_{timestamp}.srt"
        filepath = os.path.join(source_dir, filename)
    else:
        os.makedirs('output', exist_ok=True)
        filename = f"{prefix}_{timestamp}.srt"
        filepath = os.path.join('output', filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for i, sentence in enumerate(sentences, 1):
            start_time = (i-1) * 5
            end_time = i * 5
            
            start_str = f"{start_time//3600:02d}:{(start_time%3600)//60:02d}:{start_time%60:02d},000"
            end_str = f"{end_time//3600:02d}:{(end_time%3600)//60:02d}:{end_time%60:02d},000"
            
            f.write(f"{i}\n")
            f.write(f"{start_str} --> {end_str}\n")
            f.write(f"{sentence}\n\n")
    
    return filepath

def load_config():
    """تحميل الإعدادات من ملف config.json"""
    config_file = "config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    """حفظ الإعدادات في ملف config.json"""
    with open("config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# ========================================
# دوال التحقق من الملفات
# ========================================

def check_ffmpeg(ffmpeg_path):
    """التحقق من وجود FFmpeg"""
    return os.path.exists(ffmpeg_path)

def get_file_size_str(file_size):
    """
    الحصول على حجم الملف بصيغة مقروءة
    file_size: حجم الملف بالبايت (int)
    """
    try:
        size = float(file_size)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    except:
        return "0 B"

def is_arabic_text(text):
    """التحقق مما إذا كان النص يحتوي على أحرف عربية"""
    import re
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    return bool(arabic_pattern.search(text))

# ========================================
# دوال النصوص والتنسيق
# ========================================

def truncate_text(text, max_length=100):
    """اقتطاع النص إذا كان طويلاً"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def get_location_text(page, stage=None):
    """
    الحصول على نص المؤشر حسب الصفحة الحالية
    """
    if page == 'settings':
        return "الإعدادات"
    elif page == 'source':
        return "الإعدادات ← المصدر"
    elif page == 'workflow':
        stage_names = {
            1: 'المرحلة 1: تحويل فيديو إلى صوت',
            2: 'المرحلة 2: تفريغ نصي',
            3: 'المرحلة 3: ترجمة',
            4: 'المرحلة 4: تشكيل'
        }
        return f"الإعدادات ← المصدر ← {stage_names.get(stage, '')}"
    return ""

# ========================================
# دوال إحصائيات
# ========================================

def get_text_stats(text):
    """
    إحصائيات عن النص
    """
    if not text:
        return {'chars': 0, 'words': 0, 'sentences': 0}
    
    chars = len(text)
    words = len(text.split())
    import re
    sentences = len(re.split(r'[.!?]+', text)) - 1
    
    return {
        'chars': chars,
        'words': words,
        'sentences': max(sentences, 1)
    }