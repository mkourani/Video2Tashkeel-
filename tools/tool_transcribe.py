"""
أداة التفريغ النصي
"""

import streamlit as st
import os
from utils.gemini_api import transcribe_with_gemini
from utils.helpers import save_text_to_file, add_copy_button

def show_transcribe_tool():
    """عرض أداة التفريغ النصي"""
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📝 التفريغ النصي</div>', unsafe_allow_html=True)
    
    # التحقق من وجود مفتاح المستخدم
    if 'user_gemini' not in st.session_state or not st.session_state.user_gemini:
        st.warning("⚠️ الرجاء إدخال مفتاح Google Gemini في الشريط الجانبي أولاً")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # رفع ملف صوتي
    uploaded_file = st.file_uploader(
        "رفع ملف صوتي",
        type=['mp3', 'wav', 'ogg', 'm4a'],
        key="audio_upload"
    )
    
    if uploaded_file:
        # حفظ الملف مؤقتاً
        os.makedirs('temp', exist_ok=True)
        audio_path = os.path.join('temp', uploaded_file.name)
        with open(audio_path, 'wb') as f:
            f.write(uploaded_file.getvalue())
        
        st.info(f"📁 تم رفع: {uploaded_file.name}")
        
        # اختيار اللغة
        language = st.selectbox(
            "اللغة المصدر",
            ["فارسي", "عربي", "إنجليزي", "تلقائي"],
            index=0
        )
        
        # تحويل اسم اللغة
        lang_map = {
            "فارسي": "fa",
            "عربي": "ar",
            "إنجليزي": "en",
            "تلقائي": None
        }
        
        # زر التفريغ
        if st.button("🎤 بدء التفريغ", use_container_width=True):
            with st.spinner("جاري تفريغ الصوت..."):
                
                # التحقق مرة أخرى (احتياطاً)
                if 'user_gemini' not in st.session_state or not st.session_state.user_gemini:
                    st.error("❌ مفتاح Google Gemini غير موجود. الرجاء إدخاله في الشريط الجانبي")
                else:
                    transcript = transcribe_with_gemini(
                        audio_path,
                        lang_map.get(language)
                    )
                    
                    if transcript:
                        st.success("✅ تم التفريغ بنجاح!")
                        
                        # عرض النص
                        st.markdown("### 📝 النص المفرغ:")
                        st.markdown(f'<div class="output-box">{transcript}</div>', unsafe_allow_html=True)
                        
                        # أزرار الحفظ والنسخ
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("💾 حفظ", use_container_width=True):
                                filepath = save_text_to_file(transcript, "transcript")
                                st.success(f"✅ تم الحفظ")
                        with col2:
                            add_copy_button(transcript, "📋 نسخ", key="copy_transcript")
    
    st.markdown('</div>', unsafe_allow_html=True)
