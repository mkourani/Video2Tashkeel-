"""
دوال الاتصال بـ Google Gemini API
"""

import google.generativeai as genai
import time
import streamlit as st

def configure_gemini():
    """Configure Gemini API using Streamlit secrets or session state"""
    # First try Streamlit secrets (for cloud deployment)
    if 'api_key_gemini' in st.secrets:
        import google.generativeai as genai
        genai.configure(api_key=st.secrets['api_key_gemini'])
        return True
    # Then try session state (for local development)
    elif 'api_key_gemini' in st.session_state and st.session_state.api_key_gemini:
        import google.generativeai as genai
        genai.configure(api_key=st.session_state.api_key_gemini)
        return True
    return False

# ========================================
# تهيئة API
# ========================================
def configure_gemini(api_key=None):
    """تهيئة مفتاح Google Gemini"""
    if api_key:
        genai.configure(api_key=api_key)
        return True
    elif 'api_key_gemini' in st.session_state and st.session_state.api_key_gemini:
        genai.configure(api_key=st.session_state.api_key_gemini)
        return True
    return False

# ========================================
# دوال الترجمة
# ========================================
def translate_with_gemini(text, source_lang, target_lang, model="gemini-2.5-flash"):
    """الترجمة باستخدام Google Gemini"""
    
    if not configure_gemini():
        st.error("❌ مفتاح Google Gemini غير موجود")
        return None
    
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
    
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"❌ خطأ في الترجمة: {str(e)}")
        return None

# ========================================
# دوال التفريغ النصي (المهمة!)
# ========================================
def transcribe_with_gemini(audio_path, language=None, model="gemini-2.5-flash"):
    """
    تفريغ ملف صوتي إلى نص باستخدام Gemini
    
    Args:
        audio_path: مسار الملف الصوتي
        language: اللغة (fa, ar, en, أو None للتلقائي)
        model: اسم النموذج
    """
    if not configure_gemini():
        st.error("❌ مفتاح Google Gemini غير موجود")
        return None
    
    try:
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
    
    if not configure_gemini():
        st.error("❌ مفتاح Google Gemini غير موجود")
        return None
    
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
    
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"❌ خطأ في التشكيل: {str(e)}")
        return None

# ========================================
# دوال اختبار
# ========================================
def test_gemini_connection(api_key):
    """اختبار الاتصال بـ Gemini"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'OK' in Arabic")
        return True, response.text
    except Exception as e:
        return False, str(e)