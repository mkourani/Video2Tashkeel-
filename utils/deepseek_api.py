"""
دوال الاتصال بـ DeepSeek API
"""

import requests
import json
import streamlit as st

# ========================================
# دوال الترجمة
# ========================================
def translate_with_deepseek(text, source_lang, target_lang, model="deepseek-chat"):
    """الترجمة باستخدام DeepSeek"""
    
    if not st.session_state.api_key_deepseek:
        st.error("❌ مفتاح DeepSeek غير موجود")
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
        "Authorization": f"Bearer {st.session_state.api_key_deepseek}"
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
            st.error(f"DeepSeek error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# ========================================
# دوال التشكيل
# ========================================
def add_tashkeel_with_deepseek(text, level="كامل", model="deepseek-chat"):
    """إضافة التشكيل باستخدام DeepSeek"""
    
    if not st.session_state.api_key_deepseek:
        st.error("❌ مفتاح DeepSeek غير موجود")
        return None
    
    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.session_state.api_key_deepseek}"
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
            st.error(f"DeepSeek error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None