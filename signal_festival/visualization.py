from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip, AudioFileClip
from moviepy.video.io.bindings import mplfig_to_npimage
from matplotlib.patches import Circle



# Загрузка аудио файла
audio = AudioSegment.from_file("voice/audio_2024-07-22_10-36-02.ogg")

# Преобразование в массив
audio_array = np.array(audio.get_array_of_samples())

# Нормализация аудио данных
audio_array = audio_array / np.max(np.abs(audio_array))

def make_frame(t):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Установка фона
    ax.set_facecolor('black')
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.axis('off')

    # Добавление звезд на задний фон
    num_stars = 100
    star_x = np.random.uniform(-1, 1, num_stars)
    star_y = np.random.uniform(-1, 1, num_stars)
    star_sizes = np.random.uniform(0.5, 3, num_stars)
    ax.scatter(star_x, star_y, s=star_sizes, c='white', alpha=0.8)

    # Добавление волн на задний фон
    wave_amplitude = 0.1
    wave_frequency = 2 * np.pi * (t % 1)
    wave_x = np.linspace(-1, 1, 500)
    wave_y = wave_amplitude * np.sin(5 * wave_x + wave_frequency)
    ax.plot(wave_x, wave_y, color='cyan', alpha=0.6, linewidth=2)

    # Получение амплитуды на текущем временном промежутке
    idx = int(t * audio.frame_rate)
    amp = audio_array[idx] if idx < len(audio_array) else 0

    # Генерация частиц
    num_particles = 100
    angles = np.linspace(0, 2 * np.pi, num_particles)
    radii = np.random.rand(num_particles) * amp
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)

    # Отрисовка частиц
    ax.scatter(x, y, c='cyan', s=5)

    # Преобразование текущего фрейма в изображение
    return mplfig_to_npimage(fig)




# Длительность аудио
duration = audio.duration_seconds

# Создание видео
video = VideoClip(make_frame, duration=duration)

# Загрузка аудио
audio_clip = AudioFileClip("path/to/your/audio/file.mp3")

# Добавление аудио к видео
video = video.set_audio(audio_clip)

# Сохранение видео в файл
video.write_videofile("output_video_with_audio.mp4", fps=24, codec='libx264', audio_codec='aac')



