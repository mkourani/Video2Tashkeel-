"""
أداة الترجمة المستقلة
"""

import streamlit as st
import os
from utils.gemini_api import translate_with_gemini
from utils.deepseek_api import translate_with_deepseek
from utils.helpers import save_text_to_file, add_copy_button
from datetime import datetime

def show_translate_tool():
    """عرض أداة الترجمة"""
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🌐 الترجمة</div>', unsafe_allow_html=True)
    
    # التحقق من وجود مفاتيح API في الشريط الجانبي
    has_gemini = 'user_gemini' in st.session_state and st.session_state.user_gemini
    has_deepseek = 'user_deepseek' in st.session_state and st.session_state.user_deepseek
    
    if not has_gemini and not has_deepseek:
        st.warning("⚠️ الرجاء إدخال مفتاح API واحد على الأقل في الشريط الجانبي")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # إدخال النص
    text_input = st.text_area(
        "📝 النص المراد ترجمته",
        height=150,
        placeholder="أدخل النص هنا...",
        key="translate_input"
    )
    
    st.markdown("---")
    
    # اختيار API (راديو بوتون)
    st.markdown("### 🤖 اختر API")
    
    # تحديد الخيارات المتاحة بناءً على المفاتيح المدخلة
    api_options = []
    if has_gemini:
        api_options.append("Google Gemini")
    if has_deepseek:
        api_options.append("DeepSeek")
    
    if len(api_options) == 1:
        # إذا كان هناك خيار واحد فقط، استخدمه تلقائياً
        api_choice = api_options[0]
        st.info(f"سيتم استخدام {api_choice}")
    else:
        # إذا كان هناك خياران، دع المستخدم يختار
        api_choice = st.radio(
            " ",
            api_options,
            horizontal=True,
            label_visibility="collapsed",
            key="api_choice"
        )
    
    st.markdown("---")
    
    # اختيار اللغات (check boxes)
    st.markdown("### 🌍 اللغة المصدر")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        src_fa = st.checkbox("فارسي", key="src_fa")
    with col2:
        src_ar = st.checkbox("عربي", key="src_ar")
    with col3:
        src_en = st.checkbox("إنجليزي", key="src_en")
    with col4:
        src_other = st.checkbox("أخرى", key="src_other")
    
    st.markdown("### 🎯 اللغة الهدف")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        tgt_fa = st.checkbox("فارسي", key="tgt_fa")
    with col2:
        tgt_ar = st.checkbox("عربي", key="tgt_ar")
    with col3:
        tgt_en = st.checkbox("إنجليزي", key="tgt_en")
    with col4:
        tgt_other = st.checkbox("أخرى", key="tgt_other")
    
    # تحويل الاختيارات إلى نص
    source_langs = []
    if src_fa: source_langs.append("فارسي")
    if src_ar: source_langs.append("عربي")
    if src_en: source_langs.append("إنجليزي")
    if src_other: source_langs.append("أخرى")
    
    target_langs = []
    if tgt_fa: target_langs.append("فارسي")
    if tgt_ar: target_langs.append("عربي")
    if tgt_en: target_langs.append("إنجليزي")
    if tgt_other: target_langs.append("أخرى")
    
    st.markdown("---")
    
    # زر الترجمة
    if st.button("🔄 ترجمة", use_container_width=True):
        if not text_input:
            st.warning("⚠️ الرجاء إدخال نص للترجمة")
            return
        
        if not source_langs:
            st.warning("⚠️ الرجاء اختيار اللغة المصدر")
            return
        
        if not target_langs:
            st.warning("⚠️ الرجاء اختيار اللغة الهدف")
            return
        
        # نأخذ أول لغة فقط
        source_lang = source_langs[0]
        target_lang = target_langs[0]
        
        # التحقق من وجود المفتاح المناسب
        if api_choice == "Google Gemini":
            if 'user_gemini' not in st.session_state or not st.session_state.user_gemini:
                st.error("❌ مفتاح Google Gemini غير موجود. الرجاء إدخاله في الشريط الجانبي")
                return
        else:  # DeepSeek
            if 'user_deepseek' not in st.session_state or not st.session_state.user_deepseek:
                st.error("❌ مفتاح DeepSeek غير موجود. الرجاء إدخاله في الشريط الجانبي")
                return
        
        with st.spinner(f"جاري الترجمة باستخدام {api_choice}..."):
            
            if api_choice == "Google Gemini":
                result = translate_with_gemini(
                    text_input,
                    source_lang,
                    target_lang
                )
            else:  # DeepSeek
                result = translate_with_deepseek(
                    text_input,
                    source_lang,
                    target_lang
                )
            
            if result:
                st.success("✅ تمت الترجمة بنجاح!")
                
                # عرض النتيجة
                st.markdown("### 📝 النتيجة:")
                st.markdown(f'<div class="output-box">{result}</div>', unsafe_allow_html=True)
                
                # أزرار الحفظ والنسخ
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 حفظ", key="save_translate", use_container_width=True):
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filepath = save_text_to_file(result, f"translated_{api_choice.lower().replace(' ', '_')}")
                        st.success(f"✅ تم الحفظ في {os.path.basename(filepath)}")
                
                with col2:
                    add_copy_button(result, "📋 نسخ", key=f"copy_translate_{datetime.now().timestamp()}")
    
    st.markdown('</div>', unsafe_allow_html=True)
