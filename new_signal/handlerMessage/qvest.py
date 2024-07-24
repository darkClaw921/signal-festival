import json

class Quest:
    def __init__(self, json_file):
        self.json_file = json_file
        self.questions = []
        self.current_question_index = 0
        self.total_score = 0
        self.load_questions()

    def load_questions(self):
        """Загрузка вопросов из JSON файла."""
        # with open(self.json_file, 'r', encoding='utf-8') as file:
        #     self.questions = json.load(file)
        self.questions = self.json_file

    def get_current_question(self):
        """Получение текущего вопроса."""
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def answer_question(self, answer_index):
        """Обработка ответа на текущий вопрос."""
        current_question = self.get_current_question()
        if current_question:
            correct_answer_index = current_question['correct_answer_index']
            if answer_index == correct_answer_index:
                self.total_score += current_question['options'][answer_index]['points']
            self.current_question_index += 1

    def is_finished(self):
        """Проверка, закончился ли квест."""
        return self.current_question_index >= len(self.questions)

    def get_total_score(self):
        """Получение общего количества баллов."""
        return self.total_score

    def reset(self):
        """Сброс квеста для нового прохождения."""
        self.current_question_index = 0
        self.total_score = 0


class QuestManager:
    def __init__(self, json_file):
        self.json_file = json_file
        self.user_quests = {}

    def start_quest(self, user_id):
        """Начать квест для пользователя."""
        quest = Quest(self.json_file)
        self.user_quests[user_id] = quest

    def get_user_quest(self, user_id):
        """Получить квест пользователя."""
        return self.user_quests.get(user_id)

    def answer_question(self, user_id, answer_index):
        """Обработать ответ пользователя на текущий вопрос."""
        quest = self.get_user_quest(user_id)
        if quest:
            quest.answer_question(answer_index)

    def is_user_finished(self, user_id):
        """Проверить, закончил ли пользователь квест."""
        quest = self.get_user_quest(user_id)
        return quest.is_finished() if quest else True

    def get_user_score(self, user_id):
        """Получить общее количество баллов пользователя."""
        quest = self.get_user_quest(user_id)
        return quest.get_total_score() if quest else 0

    def reset_user_quest(self, user_id):
        """Сбросить квест пользователя для нового прохождения."""
        quest = self.get_user_quest(user_id)
        if quest:
            quest.reset()


# Пример JSON файла (quest.json):
# [
#     {
#         "text": "Какой цвет у неба?",
#         "media": "sky.jpg",
#         "options": [
#             {"text": "Синий", "points": 10},
#             {"text": "Зеленый", "points": 0},
#             {"text": "Красный", "points": 0}
#         ],
#         "correct_answer_index": 0
#     },
#     {
#         "text": "Сколько планет в Солнечной системе?",
#         "media": "planets.jpg",
#         "options": [
#             {"text": "8", "points": 10},
#             {"text": "9", "points": 0},
#             {"text": "7", "points": 0}
#         ],
#         "correct_answer_index": 0
#     }
# ]

# Пример использования класса:
if __name__ == "__main__":
    from googleSheet import parse_google_sheet
    parsed_data = parse_google_sheet("Квест 1")
    quest_manager = QuestManager(parsed_data)

    # Пример работы с несколькими пользователями
    user_ids = [1, 2]  # Идентификаторы пользователей

    for user_id in user_ids:
        quest_manager.start_quest(user_id)

    # Пример прохождения квеста для пользователя 1
    user_id = 1
    while not quest_manager.is_user_finished(user_id):
        question = quest_manager.get_user_quest(user_id).get_current_question()
        print(f"Пользователь {user_id}: {question['text']}")
        print("Варианты ответов:")
        for index, option in enumerate(question['options']):
            print(f"{index + 1}. {option['text']} (баллы: {option['points']})")

        answer = int(input("Введите номер ответа: ")) - 1
        quest_manager.answer_question(user_id, answer)

    print(f"Пользователь {user_id} завершил квест! Набрано {quest_manager.get_user_score(user_id)} баллов.")

    # # Пример прохождения квеста для пользователя 2
    # user_id = 2
    # while not quest_manager.is_user_finished(user_id):
    #     question = quest_manager.get_user_quest(user_id).get_current_question()
    #     print(f"Пользователь {user_id}: {question['text']}")
    #     print("Варианты ответов:")
    #     for index, option in enumerate(question['options']):
    #         print(f"{index + 1}. {option['text']} (баллы: {option['points']})")

    #     answer = int(input("Введите номер ответа: ")) - 1
    #     quest_manager.answer_question(user_id, answer)

    # print(f"Пользователь {user_id} завершил квест! Набрано {quest_manager.get_user_score(user_id)} баллов.")