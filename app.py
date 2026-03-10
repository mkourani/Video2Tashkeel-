# Add this at the VERY TOP of your app.py file
import sys, streamlit.web.cli, streamlit.runtime.runtime
if '__file__' not in globals(): 
    raise Exception("Save the file first!")
if not streamlit.runtime.runtime.Runtime.exists():
    sys.argv[:] = ['streamlit', 'run', __file__]
    sys.exit(streamlit.web.cli.main())
# End shim

# app.py - Video2Tashkeel (بدون زر الرئيسية)
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
if 'api_key_gemini' not in st.session_state:
    config = load_config()
    st.session_state.api_key_gemini = config.get('api_key_gemini', '')
if 'api_key_deepseek' not in st.session_state:
    st.session_state.api_key_deepseek = config.get('api_key_deepseek', '')

# ========================================
# العنوان الرئيسي
# ========================================
st.markdown('<div class="main-title">🕌 تشكيل</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">منظومة التفريغ والترجمة والتشكيل الآلي</div>', unsafe_allow_html=True)

# ========================================
# شريط الأدوات العلوي (بدون زر الرئيسية)
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
# إعدادات API في الشريط الجانبي (بدلاً من صفحة منفصلة)
# ========================================
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    
    with st.expander("🔑 Google Gemini"):
        gemini_key = st.text_input(
            "مفتاح API",
            value=st.session_state.api_key_gemini,
            type="password",
            key="gemini_sidebar"
        )
        if gemini_key != st.session_state.api_key_gemini:
            st.session_state.api_key_gemini = gemini_key
            save_config({'api_key_gemini': gemini_key, 'api_key_deepseek': st.session_state.api_key_deepseek})
            st.success("✅ تم الحفظ")
    
    with st.expander("🔑 DeepSeek"):
        deepseek_key = st.text_input(
            "مفتاح API",
            value=st.session_state.api_key_deepseek,
            type="password",
            key="deepseek_sidebar"
        )
        if deepseek_key != st.session_state.api_key_deepseek:
            st.session_state.api_key_deepseek = deepseek_key
            save_config({'api_key_gemini': st.session_state.api_key_gemini, 'api_key_deepseek': deepseek_key})
            st.success("✅ تم الحفظ")
    
    with st.expander("🎬 FFmpeg"):
        ffmpeg_path = os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            st.success("✅ FFmpeg موجود")
        else:
            st.error("❌ FFmpeg غير موجود")