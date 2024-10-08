from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import VideoUploadForm
from .subtitle_generator import generate_srt  # تابعی که از قبل ساخته‌اید

def video_upload_view(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video']

            # ذخیره فایل ویدئو در سیستم فایل
            fs = FileSystemStorage(location='media/videos')  # مسیر ذخیره‌سازی ویدیو
            filename = fs.save(video_file.name, video_file)
            video_path = fs.path(filename)  # مسیر کامل فایل ذخیره‌شده

            # اجرای تابع تولید زیرنویس
            srt_path = generate_srt(video_path)

            # بازگرداندن فایل SRT به کاربر
            if srt_path:
                srt_url = fs.url(srt_path)  # URL فایل SRT
                return render(request, 'upload.html', {'form': form, 'srt_file_url': srt_url})
            else:
                return render(request, 'upload.html', {'form': form, 'error': 'Failed to generate SRT file.'})

    else:
        form = VideoUploadForm()

    return render(request, 'upload.html', {'form': form})
