import aiohttp
import asyncio
import time
import os
import random

async def fetch(session, url, file_path, user_id):
    start_time = time.time()
    with open(file_path, 'rb') as f:
        # Отправляем POST-запрос с файлом и параметром userID
        # userID=int(time.time())
        data = aiohttp.FormData()
        data.add_field('file', f, filename=os.path.basename(file_path))
        data.add_field('userID', str(user_id))

        

        async with session.post(url, data=data) as response:
            response_content = await response.read()  # Чтение содержимого ответа
            
            # Сохраняем ответ в файл
            output_file_path = f"response_{user_id}.mp3"  # Имя файла для сохранения
            with open(output_file_path, 'wb') as output_file:
                output_file.write(response_content)
            
            end_time = time.time()
            return end_time - start_time  # Возвращаем время ответа

# async def main(url, file_path, user_id, count):
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch(session, url, file_path, user_id) for _ in range(count)]
#         response_times = await asyncio.gather(*tasks)
#         return response_times
async def main(url, file_path, count):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(count):
            user_id = random.randint(1000, 9999)  # Генерация случайного userID
            tasks.append(fetch(session, url, file_path, user_id))
            delay = random.uniform(1, 3)  # Генерация случайной задержки от 1 до 3 секунд
            await asyncio.sleep(delay)  # Задержка перед следующим запросом

        response_times = await asyncio.gather(*tasks)
        return response_times
    
def calculate_statistics(response_times):
    max_time = max(response_times)
    min_time = min(response_times)
    avg_time = sum(response_times) / len(response_times)
    return max_time, min_time, avg_time

if __name__ == "__main__":
    import os 
    #remove responce files
    for file in os.listdir():
        if file.startswith("response_"):
            os.remove(file)
    url = "https://generate.ai-akedemi-project.ru/api/recognition-audio/"
    file_path = "audio.mp3"  # Путь к вашему аудиофайлу
    user_id = 1234  # Ваш userID
    count = 5 # Количество запросов

    response_times = asyncio.run(main(url, file_path, count))

    for i, time_taken in enumerate(response_times):
        print(f"Запрос {i + 1}: {time_taken:.4f} секунд")

    max_time, min_time, avg_time = calculate_statistics(response_times)
    print(f"\nМаксимальное время: {max_time:.4f} секунд")
    print(f"Минимальное время: {min_time:.4f} секунд")
    print(f"Среднее время: {avg_time:.4f} секунд")