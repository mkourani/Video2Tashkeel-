"""
المرحلة 1: تحويل الفيديو إلى صوت
"""

import streamlit as st
import os
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from utils.helpers import save_text_to_file, get_file_size_str

def show_stage1():
    """عرض واجهة المرحلة 1"""
    
    st.markdown("### 🎬 المرحلة 1: تحويل الفيديو إلى صوت")
    
    # التحقق من وجود FFmpeg
    ffmpeg_path = st.session_state.get('ffmpeg_path', os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg.exe'))
    
    if not os.path.exists(ffmpeg_path):
        st.error("❌ FFmpeg غير موجود. الرجاء التأكد من مجلد ffmpeg")
        return
    
    # رفع الملف
    uploaded_file = st.file_uploader(
        "رفع ملف فيديو",
        type=['mp4', 'avi', 'mov', 'mkv', 'webm'],
        key="video_uploader"
    )
    
    if uploaded_file:
        # عرض معلومات الملف
        file_size = len(uploaded_file.getvalue())
        st.info(f"📁 اسم الملف: {uploaded_file.name}")
        st.info(f"📊 الحجم: {get_file_size_str(file_size)}")
        
        # خيارات التحويل
        col1, col2 = st.columns(2)
        with col1:
            audio_format = st.selectbox(
                "صيغة الصوت",
                ["mp3", "wav", "ogg", "m4a"],
                index=0
            )
        with col2:
            audio_quality = st.select_slider(
                "الجودة",
                options=[64, 96, 128, 192, 256, 320],
                value=192
            )
        
        # زر التحويل
        if st.button("🎬 بدء التحويل", use_container_width=True):
            with st.spinner("جاري تحويل الفيديو إلى صوت..."):
                try:
                    # حفظ الملف المؤقت
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        video_path = tmp_file.name
                    
                    # مسار الصوت الناتج
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    audio_filename = f"audio_{timestamp}.{audio_format}"
                    audio_path = os.path.join('temp', audio_filename)
                    
                    # أمر FFmpeg
                    cmd = [
                        ffmpeg_path,
                        '-i', video_path,
                        '-vn',
                        '-acodec', get_audio_codec(audio_format),
                        '-ab', f'{audio_quality}k',
                        '-y',
                        audio_path
                    ]
                    
                    # تشغيل FFmpeg
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        # حفظ المسار في الجلسة
                        st.session_state.audio_path = audio_path
                        st.session_state.source_path = video_path
                        st.session_state.source_filename = uploaded_file.name
                        st.session_state.source_dir = os.path.dirname(video_path)
                        st.session_state.conversion_done = True
                        
                        # عرض النجاح
                        st.success("✅ تم التحويل بنجاح!")
                        st.audio(audio_path)
                        
                        # زر متابعة
                        if st.button("متابعة ←", key="stage1_next"):
                            st.session_state.current_stage = 2
                            st.rerun()
                    else:
                        st.error(f"❌ خطأ في التحويل: {result.stderr[:200]}")
                    
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

def get_audio_codec(format):
    """الحصول على برنامج الترميز المناسب للصيغة"""
    codecs = {
        'mp3': 'libmp3lame',
        'wav': 'pcm_s16le',
        'ogg': 'libvorbis',
        'm4a': 'aac'
    }
    return codecs.get(format, 'libmp3lame')