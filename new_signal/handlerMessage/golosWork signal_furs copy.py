from pydub import AudioSegment
from pydub.playback import play
import numpy as np

# Функция для изменения высоты тона
def change_pitch(sound, semitones):
    new_sample_rate = int(sound.frame_rate * (3 ** (semitones / 12.0)))
    pitched_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    return pitched_sound.set_frame_rate(sound.frame_rate)

# Функция для добавления реверберации
def add_reverb(sound, decay=0.5):
    samples = np.array(sound.get_array_of_samples())
    reverb_samples = np.zeros(len(samples) + int(0.1 * sound.frame_rate))
    
    for i in range(len(samples)):
        reverb_samples[i] += samples[i]
        if i + 1 < len(reverb_samples):
            reverb_samples[i + 1] += samples[i] * decay
            
    reverb_sound = AudioSegment(
        reverb_samples.astype(np.int16).tobytes(),
        frame_rate=sound.frame_rate,
        sample_width=sound.sample_width,
        channels=sound.channels
    )
    
    return reverb_sound[:len(sound)]  # Обрезаем до оригинальной длины

# Функция для добавления эффекта "робота"
def add_robot_effect(sound, modulation_frequency=5):
    samples = np.array(sound.get_array_of_samples())
    t = np.arange(len(samples)) / sound.frame_rate
    modulation = 0.05 * (1 + np.sin(2 * np.pi * modulation_frequency * t))  # Синусоидальная модуляция
    robot_samples = samples * modulation
    robot_audio = AudioSegment(
        robot_samples.astype(np.int16).tobytes(),
        frame_rate=sound.frame_rate,
        sample_width=sound.sample_width,
        channels=sound.channels
    )
    return robot_audio

# Функция для сглаживания звука
def smooth_sound(sound, gain=0.9):
    samples = np.array(sound.get_array_of_samples())
    smoothed_samples = np.clip(samples * gain, -32768, 32767)  # Ограничиваем значения
    smoothed_audio = AudioSegment(
        smoothed_samples.astype(np.int16).tobytes(),
        frame_rate=sound.frame_rate,
        sample_width=sound.sample_width,
        channels=sound.channels
    )
    return smoothed_audio

# Функция для увеличения скорости воспроизведения
def increase_speed(sound, speed_factor=1.1):
    return sound.speedup(playback_speed=speed_factor)
# Загрузка аудиофайла
audio = AudioSegment.from_file("audio.mp3")

# Изменение высоты тона (увеличиваем на 2 полутонов для более приятного голоса)
pitched_audio = change_pitch(audio, semitones=-1)

aud= increase_speed(pitched_audio)
# Добавление эффекта "робота"
# robot_audio = add_robot_effect(pitched_audio, modulation_frequency=1)

# Добавление реверберации
# reverb_audio = add_reverb(robot_audio, decay=0.1)
# reverb_audio = add_reverb(pitched_audio, decay=0.1)

# Сглаживание звука
# final_audio = smooth_sound(reverb_audio, gain=0.95)
# final_audio = smooth_sound(reverb_audio, gain=0.35)

# Повышение громкости в 2 раза (6 дБ)
# final_audio = final_audio + 12 # Или final_audio.apply_gain(6)

# Сохранение результата
aud.export("signal_furs.mp3", format="mp3")

# Воспроизведение результата (опционально)
play(aud)