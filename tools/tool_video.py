"""
أداة تحويل الفيديو إلى صوت - نسخة محسنة
"""
import streamlit as st
import os
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
import shutil  # مهم للـ FFmpeg path

# ========================================
# دالة الحصول على مسار FFmpeg (للكلود والمحلي)
# ========================================
def get_ffmpeg_path():
    """Get FFmpeg path that works in both local and cloud environments"""
    # Check if ffmpeg is in system PATH (for cloud)
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        return ffmpeg_path
    # Fallback to local ffmpeg folder (for local development)
    local_path = os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg.exe')
    if os.path.exists(local_path):
        return local_path
    return 'ffmpeg'  # Hope it's in PATH

# ========================================
# دوال مساعدة
# ========================================
def get_file_size_str(file_size):
    """دالة مساعدة للحجم"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if file_size < 1024:
            return f"{file_size:.1f} {unit}"
        file_size /= 1024
    return f"{file_size:.1f} TB"

def get_audio_codec(format):
    """الحصول على برنامج الترميز المناسب للصيغة"""
    codecs = {
        'mp3': 'libmp3lame',
        'wav': 'pcm_s16le',
        'ogg': 'libvorbis',
        'm4a': 'aac'
    }
    return codecs.get(format, 'libmp3lame')

# ========================================
# الدالة الرئيسية
# ========================================
def show_video_tool():
    """عرض أداة تحويل الفيديو إلى صوت"""
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🎬 تحويل فيديو إلى صوت</div>', unsafe_allow_html=True)
    
    # الحصول على مسار FFmpeg
    ffmpeg_path = get_ffmpeg_path()
    
    # التحقق من وجود FFmpeg
    if ffmpeg_path == 'ffmpeg':
        # Try to find it with 'where' command on Windows
        try:
            result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
            if result.returncode == 0:
                ffmpeg_path = result.stdout.strip().split('\n')[0]
            else:
                st.error("❌ FFmpeg غير موجود. الرجاء التأكد من تثبيته")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        except:
            st.error("❌ FFmpeg غير موجود. الرجاء التأكد من تثبيته")
            st.markdown('</div>', unsafe_allow_html=True)
            return
    
    # رفع الملف
    uploaded_file = st.file_uploader(
        "رفع ملف فيديو",
        type=['mp4', 'avi', 'mov', 'mkv', 'webm'],
        key="video_upload"
    )
    
    if uploaded_file is not None:
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
                index=0,
                key="audio_format"
            )
        with col2:
            audio_quality = st.select_slider(
                "الجودة",
                options=[64, 96, 128, 192, 256, 320],
                value=192,
                key="audio_quality"
            )
        
        # زر التحويل
        if st.button("🎬 بدء التحويل", use_container_width=True):
            with st.spinner("جاري تحويل الفيديو إلى صوت..."):
                try:
                    # إنشاء مجلد temp إذا لم يكن موجوداً
                    os.makedirs('temp', exist_ok=True)
                    
                    # حفظ الملف المؤقت
                    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix, dir='temp')
                    temp_video.write(uploaded_file.getvalue())
                    temp_video.close()
                    video_path = temp_video.name
                    
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
                        st.success("✅ تم التحويل بنجاح!")
                        
                        # عرض مشغل الصوت
                        with open(audio_path, 'rb') as f:
                            audio_bytes = f.read()
                        st.audio(audio_bytes)
                        
                        # زر تحميل الملف
                        with open(audio_path, 'rb') as f:
                            st.download_button(
                                label="📥 تحميل الملف الصوتي",
                                data=f,
                                file_name=audio_filename,
                                mime=f"audio/{audio_format}"
                            )
                        
                        # تنظيف الملفات المؤقتة (اختياري)
                        try:
                            os.unlink(video_path)
                        except:
                            pass
                    else:
                        st.error(f"❌ خطأ في التحويل: {result.stderr[:200]}")
                    
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)