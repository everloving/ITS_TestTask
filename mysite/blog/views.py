import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import Query
from .forms import QueryForm
import io
import av

def create_video(request):

    def generate_video(text: str): #передаётся текст из запроса, возвращается видео
            textlen = len(text)
            width, height, fps = 100, 100, textlen * 2 # Параметы кадра
            output_memory_file = io.BytesIO()
            output = av.open(output_memory_file, 'w', format='mp4')
            stream = output.add_stream('h264', str(fps))
            frame = np.zeros((height, width, 3), dtype=np.uint8) # Создаем кадр с черным фоном
            x, y = width, height // 2 # Начальные координаты для бегущей строки

            # Установим параметры шрифта
            font = cv2.FONT_HERSHEY_COMPLEX
            font_scale = 1
            font_thickness = 2
            font_color = (255, 255, 255)  # Белый цвет текста

            # Пройдемся по каждому кадру
            for t in range(int(2.8 * fps)):  # 3 секунды с частотой (2*длину текста) кадра/сек 
                frame.fill(0)# Очистка кадра
                x -= 4  # Скорость бегущей строки
                cv2.putText(frame, text, (x, y), font, font_scale, font_color, font_thickness) # Вот тут добавим текст
                frame_text = av.VideoFrame.from_ndarray(frame, format='bgr24')
                packet = stream.encode(frame_text)
                output.mux(packet) # Тут запишем кадр
                #out.write(frame)
            packet = stream.encode(None)
            output.mux(packet)
            output.close()

            mp4 = output_memory_file.getbuffer()
            return mp4 #возвращаем объект memoryview


    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            query = Query(text=text, timestamp=timezone.now())
            query.save()
            video_memoryview = generate_video(text)
            video_buffer = io.BytesIO(video_memoryview.tobytes())
            response = HttpResponse(video_buffer, content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="downloaded_video.mp4"'
 
            return response
    else:
        form = QueryForm()
    return render(request, 'blog/create_video.html', {'form': form})

