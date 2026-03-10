"""
المرحلة 4: التشكيل
خطوتان: إضافة كل التشكيل، ثم إزالة الزائد
"""

import streamlit as st
from utils.gemini_api import add_full_tashkeel, add_tashkeel_with_options
from utils.diacritics import clean_tashkeel, ARABIC_DIACRITICS
from utils.helpers import save_text_to_file, save_srt_file, is_arabic_text, get_text_stats

def show_stage4():
    """عرض واجهة المرحلة 4 (خطوتان)"""
    
    st.markdown("### 🕌 المرحلة 4: التشكيل")
    
    # تحديد النص المدخل
    input_text = st.session_state.get('translated_text') or st.session_state.get('original_text')
    
    if not input_text:
        st.warning("⚠️ لا يوجد نص للتشكيل. الرجاء إكمال المرحلة 3 أولاً.")
        return
    
    # التحقق من أن النص عربي
    if not is_arabic_text(input_text):
        st.warning("⚠️ النص ليس بالعربية. التشكيل يحتاج نصاً عربياً.")
        st.info("💡 الرجاء العودة للمرحلة 3 وترجمة النص إلى العربية.")
        return
    
    # ========================================
    # الخطوة 1: إضافة التشكيل
    # ========================================
    st.markdown("#### ✨ الخطوة 1: إضافة التشكيل الأساسي")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**النص المدخل:**")
        st.text_area("", input_text[:200] + "..." if len(input_text) > 200 else input_text, height=80, key="input_preview")
    
    with col2:
        tashkeel_level = st.selectbox(
            "مستوى التشكيل",
            ["كامل", "بسيط", "قرآني"],
            index=0
        )
    
    # نص بعد الإضافة
    if 'full_tashkeel_text' not in st.session_state:
        st.session_state.full_tashkeel_text = None
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ إضافة التشكيل", use_container_width=True):
            with st.spinner("جاري إضافة التشكيل..."):
                if tashkeel_level == "كامل":
                    full_text = add_full_tashkeel(input_text)
                else:
                    full_text = add_tashkeel_with_options(input_text, tashkeel_level)
                
                if full_text:
                    st.session_state.full_tashkeel_text = full_text
                    st.success("✅ تمت إضافة التشكيل!")
    
    # عرض النص بعد الإضافة
    if st.session_state.full_tashkeel_text:
        st.markdown("**النص بعد الإضافة:**")
        st.markdown(f'<div class="output-box">{st.session_state.full_tashkeel_text[:300]}...</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ========================================
        # الخطوة 2: إزالة الزائد (منطق Saheh)
        # ========================================
        st.markdown("#### ✂️ الخطوة 2: إزالة التشكيل الزائد")
        st.markdown("اختر ما تريد الاحتفاظ به:")
        
        # خيارات الإزالة
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**الشدة والتنوين**")
            keep_shadda = st.checkbox("الشدة العادية (ّ)", value=True, key="keep_shadda")
            keep_tanween_fatha = st.checkbox("تنوين الفتح (ً)", value=True, key="keep_t_fatha")
            keep_tanween_damma = st.checkbox("تنوين الضم (ٌ)", value=True, key="keep_t_damma")
            keep_tanween_kasra = st.checkbox("تنوين الكسر (ٍ)", value=True, key="keep_t_kasra")
        
        with col2:
            st.markdown("**الحركات القصيرة**")
            keep_fatha = st.checkbox("الفتحة (َ)", value=False, key="keep_fatha")
            keep_damma = st.checkbox("الضمة (ُ)", value=False, key="keep_damma")
            keep_kasra = st.checkbox("الكسرة (ِ)", value=False, key="keep_kasra")
            
            st.markdown("**خيارات إضافية**")
            keep_shamsi = st.checkbox("التشديد الشمسي", value=False, key="keep_shamsi")
            keep_majhool = st.checkbox("ضمة المبني للمجهول", value=True, key="keep_majhool")
        
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
                st.session_state.stage4_done = True
                
                st.success("✅ تمت إزالة التشكيل الزائد!")
        
        # عرض النص النهائي
        if st.session_state.get('final_text'):
            st.markdown("**النص النهائي:**")
            st.markdown(f'<div class="output-box">{st.session_state.final_text}</div>', unsafe_allow_html=True)
            
            # إحصائيات
            stats_before = get_text_stats(st.session_state.full_tashkeel_text)
            stats_after = get_text_stats(st.session_state.final_text)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("عدد الكلمات", stats_after['words'])
            with col2:
                diff = stats_before['chars'] - stats_after['chars']
                st.metric("الحركات المحذوفة", diff)
            
            # أزرار الحفظ
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("💾 حفظ", use_container_width=True):
                    source_path = st.session_state.get('source_path')
                    filepath = save_text_to_file(st.session_state.final_text, 'tashkeel_final', source_path)
                    st.success(f"✅ تم الحفظ في {os.path.basename(filepath)}")
            
            with col2:
                if st.button("📋 نسخ", use_container_width=True):
                    st.write("تم النسخ! (اضغط Ctrl+C)")
            
            with col3:
                if st.button("📑 SRT", use_container_width=True):
                    source_path = st.session_state.get('source_path')
                    srt_path = save_srt_file(st.session_state.final_text, 'subtitles', source_path)
                    st.success(f"✅ تم حفظ SRT في {os.path.basename(srt_path)}")
            
            with col4:
                if st.button("🔄 جديد", use_container_width=True):
                    # إعادة تعيين للتشكيل فقط
                    st.session_state.full_tashkeel_text = None
                    st.session_state.final_text = None
                    st.rerun()