# Add this at the VERY TOP of your app.py file
import sys, streamlit.web.cli, streamlit.runtime.runtime
if '__file__' not in globals(): 
    raise Exception("Save the file first!")
if not streamlit.runtime.runtime.Runtime.exists():
    sys.argv[:] = ['streamlit', 'run', __file__]
    sys.exit(streamlit.web.cli.main())
# End shim

# app.py - Video2Tashkeel (نسخة الكلود - المستخدم يدخل المفاتيح)
import streamlit as st
import os

# استيراد الأدوات
from tools.tool_video import show_video_tool
from tools.tool_transcribe import show_transcribe_tool
from tools.tool_translate import show_translate_tool
from tools.tool_tashkeel import show_tashkeel_tool

# استيراد الدوال المساعدة
from utils.helpers import load_config, save_config

# ========================================
# إعدادات الصفحة
# ========================================
st.set_page_config(
    page_title="Video2Tashkeel - تشكيل",
    page_icon="🕌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========================================
# تحميل التنسيقات
# ========================================
try:
    with open('assets/style.css', 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except:
    pass

# ========================================
# تهيئة الجلسة
# ========================================
if 'current_tool' not in st.session_state:
    st.session_state.current_tool = 'video'  # نبدأ بالفيديو مباشرة
# ❌ NO LONGER loading API keys from config.json
# Users will enter them manually in the sidebar

# ========================================
# العنوان الرئيسي
# ========================================
st.markdown('<div class="main-title">🕌 تشكيل</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">منظومة التفريغ والترجمة والتشكيل الآلي</div>', unsafe_allow_html=True)

# ========================================
# شريط الأدوات العلوي
# ========================================
tools = {
    "🎬 فيديو←صوت": "video",
    "📝 تفريغ": "transcribe",
    "🌐 ترجمة": "translate",
    "🕌 تشكيل": "tashkeel"
}

st.markdown('<div class="toolbar">', unsafe_allow_html=True)
cols = st.columns(len(tools))
for i, (name, tool_id) in enumerate(tools.items()):
    with cols[i]:
        if st.button(name, key=f"tool_{tool_id}", use_container_width=True):
            st.session_state.current_tool = tool_id
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ========================================
# عرض الأداة الحالية
# ========================================
if st.session_state.current_tool == 'video':
    show_video_tool()
elif st.session_state.current_tool == 'transcribe':
    show_transcribe_tool()
elif st.session_state.current_tool == 'translate':
    show_translate_tool()
elif st.session_state.current_tool == 'tashkeel':
    show_tashkeel_tool()

# ========================================
# إعدادات API في الشريط الجانبي (للمستخدم)
# ========================================
with st.sidebar:
    st.markdown("### 🔑 مفاتيح API")
    st.markdown("*أدخل مفاتيحك الخاصة لاستخدام التطبيق*")
    
    # Google Gemini - User enters their own key
    user_gemini = st.text_input(
        "🔵 Google Gemini",
        type="password",
        placeholder="أدخل مفتاح Google Gemini",
        key="user_gemini_input",
        help="لن يتم حفظ هذا المفتاح - أدخله كل مرة تستخدم فيها التطبيق"
    )
    
    # DeepSeek - User enters their own key
    user_deepseek = st.text_input(
        "⚪ DeepSeek",
        type="password",
        placeholder="أدخل مفتاح DeepSeek",
        key="user_deepseek_input",
        help="لن يتم حفظ هذا المفتاح - أدخله كل مرة تستخدم فيها التطبيق"
    )
    
    # Store in session state for the app to use
    if user_gemini:
        st.session_state.user_gemini = user_gemini
        st.success("✅ تم إدخال مفتاح Google Gemini")
    
    if user_deepseek:
        st.session_state.user_deepseek = user_deepseek
        st.success("✅ تم إدخال مفتاح DeepSeek")
    
    st.markdown("---")
    
    # FFmpeg check (optional)
    with st.expander("🎬 معلومات FFmpeg"):
        st.markdown("في النسخة السحابية، FFmpeg مثبت تلقائياً")