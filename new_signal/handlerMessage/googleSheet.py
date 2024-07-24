import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
def parse_google_sheet(sheet_name):
    # Настройка доступа к Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('steam-outlet-368911-cde7193347ad.json', scope)
    client = gspread.authorize(creds)

    # Открытие таблицы и листа
    sheet = client.open("Signal_Quests").worksheet(sheet_name)
    
    # Получение всех данных из листа
    data = sheet.get_all_values()
    
    # Словарь для хранения вопросов
    questions = {}
    
    for row in data[1:]:  # Пропускаем заголовок
        question_number = row[0]
        question_text = row[1].strip()
        answer_text = row[2].strip()
        points = int(row[3].strip())
        
        if question_number not in questions:
            questions[question_number] = {
                "text": question_text,
                "media": "planets.jpg",  # Замените на нужное имя файла
                "options": [],
                "correct_answer_index": None
            }
        
        questions[question_number]["options"].append({"text": answer_text, "points": points})
        
        # Устанавливаем правильный ответ (первый с ненулевыми баллами)
        if questions[question_number]["correct_answer_index"] is None and points > 0:
            questions[question_number]["correct_answer_index"] = len(questions[question_number]["options"]) - 1

    # Преобразуем словарь в список
    result = list(questions.values())
    
    return result

# Пример использования
if __name__ == "__main__":
    parsed_data = parse_google_sheet("Квест 1")
    pprint(parsed_data)