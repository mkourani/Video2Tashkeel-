"""
دوال الاتصال بـ Google Gemini API - نسخة المستخدم (للكلود)
"""

import streamlit as st
import google.generativeai as genai
import time

# ========================================
# الحصول على مفتاح المستخدم
# ========================================
def get_gemini_key():
    """Get Gemini API key from session state (user input)"""
    if 'user_gemini' in st.session_state and st.session_state.user_gemini:
        return st.session_state.user_gemini
    return None

# ========================================
# دوال الترجمة
# ========================================
def translate_with_gemini(text, source_lang, target_lang, model="gemini-2.5-flash"):
    """الترجمة باستخدام Google Gemini - مع مفتاح المستخدم"""
    
    api_key = get_gemini_key()
    if not api_key:
        st.error("❌ الرجاء إدخال مفتاح Google Gemini في الشريط الجانبي")
        return None
    
    try:
        genai.configure(api_key=api_key)
        
        # تحويل أسماء اللغات للإنجليزية
        lang_map = {
            "فارسي": "Persian",
            "عربي": "Arabic",
            "إنجليزي": "English"
        }
        
        src = lang_map.get(source_lang, source_lang)
        tgt = lang_map.get(target_lang, target_lang)
        
        prompt = f"""
        Translate the following text from {src} to {tgt}.
        Return only the translation, no explanations.
        
        Text: {text}
        """
        
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        st.error(f"❌ خطأ في الترجمة: {str(e)}")
        return None

# ========================================
# دوال التفريغ النصي
# ========================================
def transcribe_with_gemini(audio_path, language=None, model="gemini-2.5-flash"):
    """تفريغ ملف صوتي إلى نص باستخدام Gemini"""
    
    api_key = get_gemini_key()
    if not api_key:
        st.error("❌ الرجاء إدخال مفتاح Google Gemini في الشريط الجانبي")
        return None
    
    try:
        genai.configure(api_key=api_key)
        
        # رفع الملف الصوتي
        with st.spinner("جاري رفع الملف الصوتي..."):
            audio_file = genai.upload_file(audio_path)
        
        # انتظار معالجة الملف
        with st.spinner("جاري معالجة الملف الصوتي..."):
            while audio_file.state.name == "PROCESSING":
                time.sleep(2)
                audio_file = genai.get_file(audio_file.name)
        
        if audio_file.state.name == "FAILED":
            st.error("❌ فشلت معالجة الملف الصوتي")
            return None
        
        # إعداد prompt حسب اللغة
        if language == "fa":
            prompt = "Transcribe this Persian audio accurately. Return only the transcription."
        elif language == "ar":
            prompt = "فرغ هذا الملف الصوتي العربي بدقة. أعد فقط النص المفرغ."
        elif language == "en":
            prompt = "Transcribe this English audio accurately. Return only the transcription."
        else:
            prompt = "Transcribe this audio accurately. Detect the language automatically. Return only the transcription."
        
        # تفريغ الصوت
        model = genai.GenerativeModel(model)
        response = model.generate_content([prompt, audio_file])
        
        return response.text.strip()
    
    except Exception as e:
        st.error(f"❌ خطأ في التفريغ: {str(e)}")
        return None

# ========================================
# دوال التشكيل
# ========================================
def add_tashkeel_with_gemini(text, level="كامل", model="gemini-2.5-flash"):
    """إضافة التشكيل باستخدام Google Gemini"""
    
    api_key = get_gemini_key()
    if not api_key:
        st.error("❌ الرجاء إدخال مفتاح Google Gemini في الشريط الجانبي")
        return None
    
    try:
        genai.configure(api_key=api_key)
        
        level_desc = {
            "بسيط": "Add only basic diacritics (shadda and tanween)",
            "كامل": "Add all diacritics (fatha, damma, kasra, shadda, tanween)",
            "قرآني": "Add diacritics following Quranic rules with proper tajweed"
        }
        
        prompt = f"""
        You are an expert in Arabic diacritics. Add tashkeel to the following Arabic text.
        
        Level: {level_desc.get(level, level_desc['كامل'])}
        
        Rules:
        - Add fatha (َ), damma (ُ), kasra (ِ) where appropriate
        - Add shadda (ّ) for doubled letters
        - Add tanween (ً, ٌ, ٍ) for nunation
        - Add sukun (ْ) where needed
        - Preserve the original text
        
        Text: {text}
        
        Return ONLY the text with diacritics added.
        """
        
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        st.error(f"❌ خطأ في التشكيل: {str(e)}")
        return None
