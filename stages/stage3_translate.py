"""
المرحلة 3: الترجمة
"""

import streamlit as st
import os
from utils.gemini_api import translate_text
from utils.helpers import save_text_to_file, is_arabic_text

def show_stage3():
    """عرض واجهة المرحلة 3"""
    
    st.markdown("### 🌐 المرحلة 3: الترجمة")
    
    # التحقق من وجود نص
    original_text = st.session_state.get('original_text')
    
    if not original_text:
        st.warning("⚠️ لا يوجد نص للترجمة. الرجاء إكمال المرحلة 2 أولاً.")
        return
    
    # عرض النص الأصلي
    with st.expander("النص الأصلي", expanded=False):
        st.text_area("", original_text[:500] + "..." if len(original_text) > 500 else original_text, height=100)
    
    # خيارات الترجمة
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox(
            "من",
            ["فارسي", "عربي", "إنجليزي"],
            index=["فارسي", "عربي", "إنجليزي"].index(st.session_state.get('source_lang', 'فارسي'))
        )
    with col2:
        target_lang = st.selectbox(
            "إلى",
            ["عربي", "إنجليزي", "فارسي", "بدون ترجمة"],
            index=0
        )
    
    # زر الترجمة
    if st.button("🔄 ترجمة", use_container_width=True):
        
        if target_lang == "بدون ترجمة":
            st.session_state.translated_text = original_text
            st.session_state.stage3_done = True
            st.info("✅ تم تخطي الترجمة")
            
            if st.button("متابعة ←", key="stage3_skip_next"):
                st.session_state.current_stage = 4
                st.rerun()
        
        else:
            with st.spinner("جاري الترجمة..."):
                
                translated = translate_text(
                    original_text,
                    source_lang,
                    target_lang
                )
                
                if translated:
                    # حفظ النص
                    source_path = st.session_state.get('source_path')
                    filepath = save_text_to_file(translated, 'translated', source_path)
                    
                    st.session_state.translated_text = translated
                    st.session_state.stage3_done = True
                    st.session_state.target_lang = target_lang
                    
                    st.success(f"✅ تمت الترجمة بنجاح!")
                    st.info(f"📁 تم الحفظ في: {os.path.basename(filepath)}")
                    
                    # عرض النص المترجم
                    with st.expander("عرض النص المترجم", expanded=True):
                        st.text_area("", translated[:500] + "..." if len(translated) > 500 else translated, height=150)
                    
                    # التحقق إذا كان النص عربياً للتشكيل
                    if target_lang == "عربي" and is_arabic_text(translated):
                        st.info("✅ النص عربي - يمكن تشكيله في المرحلة القادمة")
                    
                    # زر متابعة
                    if st.button("متابعة ←", key="stage3_next"):
                        st.session_state.current_stage = 4
                        st.rerun()