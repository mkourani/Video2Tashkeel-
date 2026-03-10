"""
المرحلة 2: التفريغ النصي
"""

import streamlit as st
import os
from utils.gemini_api import transcribe_audio
from utils.helpers import save_text_to_file, get_text_stats

def show_stage2():
    """عرض واجهة المرحلة 2"""
    
    st.markdown("### 📝 المرحلة 2: التفريغ النصي")
    
    # التحقق من وجود ملف صوتي
    audio_path = st.session_state.get('audio_path')
    
    if not audio_path or not os.path.exists(audio_path):
        st.warning("⚠️ لا يوجد ملف صوتي. الرجاء إكمال المرحلة 1 أولاً.")
        return
    
    # عرض معلومات الملف
    st.info(f"🎵 الملف الصوتي: {os.path.basename(audio_path)}")
    
    # خيارات التفريغ
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox(
            "اللغة المصدر",
            ["فارسي", "عربي", "إنجليزي", "auto"],
            index=["فارسي", "عربي", "إنجليزي", "auto"].index(st.session_state.get('source_lang', 'فارسي'))
        )
    
    # زر التفريغ
    if st.button("🎤 بدء التفريغ", use_container_width=True):
        with st.spinner("جاري تفريغ الصوت... (قد يستغرق دقيقة)"):
            
            # تحويل اسم اللغة للإنجليزية
            lang_map = {
                "فارسي": "fa",
                "عربي": "ar", 
                "إنجليزي": "en",
                "auto": None
            }
            
            transcript = transcribe_audio(
                audio_path,
                language=lang_map.get(source_lang, "ar")
            )
            
            if transcript:
                # حفظ النص
                filepath = save_text_to_file(transcript, 'transcript', audio_path)
                st.session_state.original_text = transcript
                st.session_state.stage2_done = True
                st.session_state.source_lang = source_lang
                
                # عرض النتيجة
                st.success(f"✅ تم التفريغ بنجاح!")
                st.info(f"📁 تم الحفظ في: {os.path.basename(filepath)}")
                
                # إحصائيات
                stats = get_text_stats(transcript)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("عدد الكلمات", stats['words'])
                with col2:
                    st.metric("عدد الجمل", stats['sentences'])
                with col3:
                    st.metric("عدد الحروف", stats['chars'])
                
                # عرض النص
                with st.expander("عرض النص الكامل"):
                    st.text_area("النص المفرغ", transcript, height=200)
                
                # زر متابعة
                if st.button("متابعة ←", key="stage2_next"):
                    st.session_state.current_stage = 3
                    st.rerun()

    # إذا كان هناك نص سابق
    elif st.session_state.get('original_text'):
        st.info("✅ لديك نص مفرغ بالفعل")
        if st.button("متابعة ←", key="stage2_skip"):
            st.session_state.current_stage = 3
            st.rerun()