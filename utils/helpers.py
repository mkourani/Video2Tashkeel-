"""
دوال مساعدة عامة للمشروع - نسخة الكلود
"""

import os
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# Add this at the top of utils/helpers.py, after imports

def load_config():
    """Simple config loader that returns empty dict (no file storage on cloud)"""
    return {}

def save_config(config):
    """Simple config saver that does nothing (no file storage on cloud)"""
    pass
    
# ========================================
# دوال النسخ
# ========================================
def add_copy_button(text_to_copy, button_text="📋 نسخ", key="copy"):
    """إضافة زر نسخ يعمل باستخدام JavaScript"""
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
# حفظ الملفات
# ========================================
def save_text_to_file(text, prefix, source_path=None):
    """حفظ النص في ملف"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # في الكلود، نحفظ في مجلد tmp
    os.makedirs('/tmp/output', exist_ok=True)
    filename = f"{prefix}_{timestamp}.txt"
    filepath = os.path.join('/tmp/output', filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return filepath

# ========================================
# دوال التحقق
# ========================================
def get_file_size_str(file_size):
    """الحصول على حجم الملف بصيغة مقروءة"""
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
