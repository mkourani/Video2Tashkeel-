"""
دوال الاتصال بـ DeepSeek API - نسخة المستخدم (للكلود)
"""

import streamlit as st
import requests
import json

# ========================================
# الحصول على مفتاح المستخدم
# ========================================
def get_deepseek_key():
    """Get DeepSeek API key from session state (user input)"""
    if 'user_deepseek' in st.session_state and st.session_state.user_deepseek:
        return st.session_state.user_deepseek
    return None

# ========================================
# دوال الترجمة
# ========================================
def translate_with_deepseek(text, source_lang, target_lang, model="deepseek-chat"):
    """الترجمة باستخدام DeepSeek - مع مفتاح المستخدم"""
    
    api_key = get_deepseek_key()
    if not api_key:
        st.error("❌ الرجاء إدخال مفتاح DeepSeek في الشريط الجانبي")
        return None
    
    url = "https://api.deepseek.com/v1/chat/completions"
    
    # تحويل أسماء اللغات للإنجليزية
    lang_map = {
        "فارسي": "Persian",
        "عربي": "Arabic",
        "إنجليزي": "English"
    }
    
    src = lang_map.get(source_lang, source_lang)
    tgt = lang_map.get(target_lang, target_lang)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    prompt = f"""
    Translate the following text from {src} to {tgt}.
    Return only the translation, no explanations.
    
    Text: {text}
    """
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            st.error(f"❌ خطأ DeepSeek: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال: {str(e)}")
        return None

# ========================================
# دوال التشكيل
# ========================================
def add_tashkeel_with_deepseek(text, level="كامل", model="deepseek-chat"):
    """إضافة التشكيل باستخدام DeepSeek"""
    
    api_key = get_deepseek_key()
    if not api_key:
        st.error("❌ الرجاء إدخال مفتاح DeepSeek في الشريط الجانبي")
        return None
    
    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    level_desc = {
        "بسيط": "Add only basic diacritics (shadda and tanween)",
        "كامل": "Add all diacritics (fatha, damma, kasra, shadda, tanween)",
        "قرآني": "Add diacritics following Quranic rules"
    }
    
    prompt = f"""
    Add Arabic diacritics (tashkeel) to the following text.
    Level: {level_desc.get(level, level_desc['كامل'])}
    
    Text: {text}
    
    Return only the text with diacritics.
    """
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert in Arabic diacritics."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            st.error(f"❌ خطأ DeepSeek: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال: {str(e)}")
        return None
