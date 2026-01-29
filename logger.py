import json
import os
from datetime import datetime
from typing import Dict, Any, List

class InterviewLogger:
    """
    Логгер для записи сессии интервью в формате JSON.
    Сохраняет видимые сообщения, ответы пользователя и внутренние мысли агентов.
    """
    def __init__(self, team_name: str = "InterviewCoachAI"):
        self.team_name = team_name
        self.session_data = {
            "team_name": team_name,
            "session_start": datetime.now().isoformat(),
            "turns": [],
            "final_feedback": None
        }
        self.current_turn_id = 1

    def log_turn(
        self,
        agent_visible_message: str,
        user_message: str,
        internal_thoughts: str
    ) -> None:
        """
        Записывает один ход (вопрос-ответ) интервью.

        :param agent_visible_message: Видимый пользователю вопрос/реплика агента.
        :param user_message: Ответ кандидата.
        :param internal_thoughts: Внутренние рассуждения агентов (скрытые от пользователя).
        """
        turn_entry = {
            "turn_id": self.current_turn_id,
            "agent_visible_message": agent_visible_message,
            "user_message": user_message,
            "internal_thoughts": internal_thoughts,
            "timestamp": datetime.now().isoformat()
        }
        self.session_data["turns"].append(turn_entry)
        self.current_turn_id += 1

        # Опционально: можно добавить вывод в консоль для отладки
        print(f"\n[Turn {turn_entry['turn_id'] - 1}]")
        print(f"Agent: {agent_visible_message}")
        print(f"User: {user_message}")
        print(f"Thoughts: {internal_thoughts}")

    def log_final_feedback(self, feedback: Dict[str, Any]) -> None:
        """Сохраняет финальный фидбэк системы."""
        self.session_data["final_feedback"] = feedback
        print("\n[Final Feedback Logged]")

    def save_session(self, filepath: str = "interview_log.json") -> str:
        """
        Сохраняет всю сессию в JSON-файл.

        :param filepath: Путь для сохранения файла.
        :return: Абсолютный путь к сохраненному файлу.
        """
        self.session_data["session_end"] = datetime.now().isoformat()

        # Создаем директорию, если её нет
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, ensure_ascii=False, indent=2)

        abs_path = os.path.abspath(filepath)
        print(f"\n[Session saved to: {abs_path}]")
        return abs_path

    def get_session_summary(self) -> Dict[str, Any]:
        """Возвращает текущие данные сессии для внутреннего использования."""
        return self.session_data.copy()


# Пример использования (для тестирования)
if __name__ == "__main__":
    # Инициализация логгера
    logger = InterviewLogger(team_name="AlphaTeam")

    # Логирование нескольких ходов
    logger.log_turn(
        agent_visible_message="Привет! Расскажи про свой опыт в Python.",
        user_message="Я джун, пишу код 3 месяца.",
        internal_thoughts="[Observer]: Кандидат новичок. [Interviewer]: Нужно спросить про базовые типы данных."
    )

    logger.log_turn(
        agent_visible_message="Какие структуры данных в Python ты знаешь?",
        user_message="Список, словарь, кортеж, множество.",
        internal_thoughts="[Observer]: Ответ верный, но поверхностный. [Interviewer]: Углубиться в сложность операций."
    )

    # Логирование фидбэка
    sample_feedback = {
        "verdict": {
            "grade": "Junior",
            "hiring_recommendation": "No Hire",
            "confidence_score": 75
        },
        "hard_skills": {
            "confirmed": ["Basic Python syntax", "Data structures"],
            "gaps": ["Algorithms complexity", "System design"]
        }
    }
    logger.log_final_feedback(sample_feedback)

    # Сохранение сессии
    logger.save_session("logs/example_interview_log.json")