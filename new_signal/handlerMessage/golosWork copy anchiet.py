from pydub import AudioSegment
from pydub.playback import play
import numpy as np

# Функция для изменения высоты тона
def change_pitch(sound, semitones):
    new_sample_rate = int(sound.frame_rate * (2 ** (semitones / 12.0)))
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

# Функция для добавления эха
def add_echo(sound, delay=200, decay=0.5):
    echo_sound = sound
    delay_samples = int(delay * sound.frame_rate / 1000)  # Преобразуем задержку в сэмплы
    
    # Создаем массив для эха
    echo_samples = np.zeros(len(sound.get_array_of_samples()) + delay_samples)
    
    # Добавляем оригинальный звук
    echo_samples[:len(sound.get_array_of_samples())] += np.array(sound.get_array_of_samples())
    
    # Добавляем эхо
    echo_samples[delay_samples:delay_samples + len(sound.get_array_of_samples())] += np.array(sound.get_array_of_samples()) * decay
    
    echo_audio = AudioSegment(
        echo_samples.astype(np.int16).tobytes(),
        frame_rate=sound.frame_rate,
        sample_width=sound.sample_width,
        channels=sound.channels
    )
    
    return echo_audio[:len(sound) + delay_samples]  # Обрезаем до нужной длины

# Функция для добавления легкого искажения
def add_distortion(sound, gain=1.5):
    samples = np.array(sound.get_array_of_samples())
    distorted_samples = np.clip(samples * gain, -32768, 32767)  # Ограничиваем значения
    distorted_audio = AudioSegment(
        distorted_samples.astype(np.int16).tobytes(),
        frame_rate=sound.frame_rate,
        sample_width=sound.sample_width,
        channels=sound.channels
    )
    return distorted_audio

# Загрузка аудиофайла
audio = AudioSegment.from_file("audio.mp3")

# Изменение высоты тона (понижаем на 5 полутонов для глубокого голоса)
pitched_audio = change_pitch(audio, semitones=-5)

# Добавление реверберации
reverb_audio = add_reverb(pitched_audio, decay=0.6)

# Добавление эха
alien_voice_with_echo = add_echo(reverb_audio, delay=300, decay=0.4)

# Добавление искажения
final_audio = add_distortion(alien_voice_with_echo, gain=1.2)

# Сохранение результата
final_audio.export("ancient_alien_voice.mp3", format="mp3")

# Воспроизведение результата (опционально)
play(final_audio)