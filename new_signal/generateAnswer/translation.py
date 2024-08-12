from openai import OpenAI
import os
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()
key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=key,)

def transcript_audio(pathFile:str):
    print(pathFile)
    print('transcript_audio')
    audio_file = open(pathFile, "rb")
    
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text",
        prompt="разбери этот аудиофайл и напиши по строчкам"
        # prompt='напши в ответе только то что было сказанно на русском языке и начинай каждое продложение с новой строки'
        # prompt="disassemble this audio file and write in the format Client: Operator:"

    )
    print('endtrasncript')
    return transcript

# audio_file = open("f_187667f2dd2a3886.mp3", "rb")

# #save to file
# text=transcript_audio("f_187667f2dd2a3886.mp3")
# print(text)
# with open("f_187667f2dd2a3886.txt", "wb") as f:
#     f.write(text.encode())
#     f.close()

import re
def insert_newline_before_uppercase(s):
    return ''.join(['\n' + char if char.isupper() else char for char in s])
def split_before_uppercase(s):
    result = []
    current_word = ''

    for char in s:
        if char==' ': 
            current_word += char 
            continue

        if char.isupper() and current_word:
            result.append(current_word)
            current_word = char
        else:
            current_word += char

    if current_word:
        result.append(current_word)

    return result


def razdel_na_abzacy(filename, output_filename):
    """
    Разделяет текст из файла на абзацы, начинающиеся с заглавной буквы, и записывает 
    результат в новый файл. Дополнительно демонстрирует работу функции на примере текста.

    Args:
        filename: Строка, содержащая имя файла с исходным текстом.
        output_filename: Строка, содержащая имя файла для записи разделенного текста.
        text_example: Строка, содержащая пример текста для демонстрации работы функции.

    Returns:
    None
    """

    # Разделение текста из файла
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    # paragraphs = re.split(r'[A-Z]', text)
    # pprint(paragraphs)
    # Запись разделенного текста в файл
    with open(output_filename, 'w', encoding='utf-8') as f_out:
        lines=split_before_uppercase(text)
        lines2=insert_newline_before_uppercase(text)
        f_out.write(lines2) 
        # pprint(lines)
        # for s in lines:
        #     f_out.write(s)
        # for paragraph in paragraphs:
        #     f_out.write(paragraph + '\n')

    # Демонстрация работы функции на примере текста
    print("**Пример разделения текста:**")
    # example_paragraphs = re.split(r'\A[A-Z]\s+', text_example)
    # for paragraph in example_paragraphs:
        # print(paragraph)

    # Печать сообщения о результатах
    print(f'\nРазделенный текст записан в файл: {output_filename}')

if __name__ == '__main__':
    # Введите имена файлов и пример текста.
    filename = 'f_187667f2dd2a3886.txt'
    output_filename = 'abzacy.txt'
    
    # split_before_uppercase(text_example)
    # print(split_before_uppercase(text_example))
    # Вызов функции.
    razdel_na_abzacy(filename, output_filename,)

# transcript = client.audio.transcriptions.create(
#   model="whisper-1", 
#   file=audio_file, 
#   response_format="text"
# )
# pprint(transcript)