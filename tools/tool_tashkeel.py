"""
أداة التشكيل المستقلة - خطوتين
"""

import streamlit as st
import os
from utils.gemini_api import add_tashkeel_with_gemini
from utils.deepseek_api import add_tashkeel_with_deepseek
from utils.diacritics import clean_tashkeel
from utils.helpers import save_text_to_file, is_arabic_text, add_copy_button
from datetime import datetime

def show_tashkeel_tool():
    """عرض أداة التشكيل (خطوتين)"""
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🕌 التشكيل</div>', unsafe_allow_html=True)
    
    # ========================================
    # إدخال النص
    # ========================================
    text_input = st.text_area(
        "📝 النص المدخل",
        height=100,
        placeholder="أدخل النص العربي هنا...",
        key="tashkeel_input"
    )
    
    if text_input and not is_arabic_text(text_input):
        st.warning("⚠️ النص ليس بالعربية. التشكيل يحتاج نصاً عربياً.")
        return
    
    st.markdown("---")
    
    # ========================================
    # الخطوة 1: إضافة التشكيل
    # ========================================
    st.markdown("### ✨ الخطوة 1: إضافة التشكيل")
    
    # اختيار API
    st.markdown("#### 🤖 اختر API")
    api_choice = st.radio(
        " ",
        ["Google Gemini", "DeepSeek"],
        horizontal=True,
        key="api_tashkeel",
        label_visibility="collapsed"
    )
    
    # مستوى التشكيل
    level = st.selectbox(
        "مستوى التشكيل",
        ["كامل", "بسيط", "قرآني"],
        index=0,
        key="tashkeel_level"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        add_button = st.button("✨ إضافة التشكيل", use_container_width=True)
    
    if add_button and text_input:
        with st.spinner(f"جاري إضافة التشكيل باستخدام {api_choice}..."):
            
            if api_choice == "Google Gemini":
                if not st.session_state.api_key_gemini:
                    st.error("❌ مفتاح Google Gemini غير موجود")
                    return
                full_text = add_tashkeel_with_gemini(text_input, level)
            else:
                if not st.session_state.api_key_deepseek:
                    st.error("❌ مفتاح DeepSeek غير موجود")
                    return
                full_text = add_tashkeel_with_deepseek(text_input, level)
            
            if full_text:
                st.session_state.full_tashkeel_text = full_text
                st.success("✅ تمت إضافة التشكيل!")
                
                st.markdown("**النص بعد الإضافة:**")
                st.markdown(f'<div class="output-box">{full_text}</div>', unsafe_allow_html=True)
                
                # زر نسخ للنص بعد الإضافة
                add_copy_button(full_text, "📋 نسخ", key="copy_after_add")
    
    st.markdown("---")
    
    # ========================================
    # الخطوة 2: إزالة الزائد - الجزء الكامل
    # ========================================
    if 'full_tashkeel_text' in st.session_state and st.session_state.full_tashkeel_text:
        st.markdown("### ✂️ الخطوة 2: إزالة التشكيل الزائد")
        st.markdown("اختر ما تريد الاحتفاظ به:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**الشدة والتنوين**")
            keep_shadda = st.checkbox("الشدة العادية (ّ)", value=True, key="keep_shadda")
            keep_tanween_fatha = st.checkbox("تنوين الفتح (ً)", value=True, key="keep_tanween_fatha")
            keep_tanween_damma = st.checkbox("تنوين الضم (ٌ)", value=True, key="keep_tanween_damma")
            keep_tanween_kasra = st.checkbox("تنوين الكسر (ٍ)", value=True, key="keep_tanween_kasra")
        
        with col2:
            st.markdown("**الحركات القصيرة**")
            keep_fatha = st.checkbox("الفتحة (َ)", value=False, key="keep_fatha")
            keep_damma = st.checkbox("الضمة (ُ)", value=False, key="keep_damma")
            keep_kasra = st.checkbox("الكسرة (ِ)", value=False, key="keep_kasra")
            
            st.markdown("**خيارات إضافية**")
            keep_shamsi = st.checkbox("التشديد الشمسي", value=False, key="keep_shamsi",
                                     help="مثل: الرَّحْمَن ← الرحمن")
            keep_majhool = st.checkbox("ضمة المبني للمجهول", value=True, key="keep_majhool",
                                      help="مثل: ضُرب، أُكل، قُتل")
        
        st.markdown("---")
        
        # زر الإزالة
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✂️ إزالة الزائد", use_container_width=True):
                
                # تطبيق منطق Saheh
                cleaned_text = clean_tashkeel(
                    st.session_state.full_tashkeel_text,
                    keep_shadda=keep_shadda,
                    keep_tanween_fatha=keep_tanween_fatha,
                    keep_tanween_damma=keep_tanween_damma,
                    keep_tanween_kasra=keep_tanween_kasra,
                    keep_fatha=keep_fatha,
                    keep_damma=keep_damma,
                    keep_kasra=keep_kasra,
                    keep_shamsi=keep_shamsi,
                    keep_majhool=keep_majhool
                )
                
                st.session_state.final_text = cleaned_text
                st.success("✅ تمت إزالة الزائد!")
        
        # عرض النص النهائي
        if st.session_state.get('final_text'):
            st.markdown("**النص النهائي:**")
            st.markdown(f'<div class="output-box">{st.session_state.final_text}</div>', unsafe_allow_html=True)
            
            # أزرار الحفظ والنسخ
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 حفظ", key="save_final", use_container_width=True):
                    filepath = save_text_to_file(st.session_state.final_text, "tashkeel_final")
                    st.success(f"✅ تم الحفظ في {os.path.basename(filepath)}")
            
            with col2:
                add_copy_button(st.session_state.final_text, "📋 نسخ", key="copy_final")
    
    st.markdown('</div>', unsafe_allow_html=True)