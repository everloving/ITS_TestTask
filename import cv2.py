import cv2
import numpy as np
import av



# Функция для создания видео с бегущей строкой
def create_birthday_video_opencv():
    # Текст поздравления
    birthday_message = "Happy Birthday To You!!1"

    # Размеры видео (ширина x высота)
    width, height = 100, 100

    # Задаём параметры - видеопоток с частотой 24 кадра в секунду
    out = cv2.VideoWriter("birthday_video_opencv.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 24, (width, height))

    # Создаем кадр с черным фоном
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Начальные координаты для бегущей строки
    x, y = width, height // 2

    # Установим параметры шрифта
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (255, 255, 255)  # Белый цвет текста

    # Пройдемся по каждому кадру
    for t in range(72):  # 10 секунд с частотой 24 кадра/сек
        # Очистка кадра
        frame.fill(0)

        # Новые координаты для бегущей строки
        x -= 10  # Скорость бегущей строки

        # Вот тут добавим текст
        cv2.putText(frame, birthday_message, (x, y), font, font_scale, font_color, font_thickness)

        # Тут запишем кадр
        out.write(frame)

    # Закроем тут видеопоток
    out.release()

# Создаём видео 
create_birthday_video_opencv()