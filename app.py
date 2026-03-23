from flask import Flask
import random

app = Flask(__name__)

days = ["Пн", "Вт", "Ср", "Чт", "Пт"]

courses = {

    "1 курс РПО": {
        "groups": ["РПО1", "РПО2", "РПО3"],
        "subjects": {
            "Математика": 2,
            "Физика": 2,
            "Информатика": 2,
            "Литература": 1,
            "Химия": 1,
            "Русский": 1,
            "Английский": 2,
            "История": 1,
            "Физ-ра": 1,
            "География": 1,
            "Интернет-маркетинг": 1
        }
    },

    "1 курс ГД": {
        "groups": ["ГД1", "ГД2", "ГД3"],
        "subjects": {
            "Математика": 1,
            "Физика": 1,
            "Русский": 1,
            "Литература": 1,
            "Английский": 2,
            "История": 1,
            "Физ-ра": 2,
            "Биология": 1,
            "Информатика": 2,
            "Обществознание": 2,
            "Illustrator": 2,
            "Навигационный дизайн": 1
        }
    },

    "2 курс РПО": {
        "groups": ["РПО1", "РПО2"],
        "subjects": {
            "История": 1,
            "Английский": 2,
            "Физ-ра": 1,
            "Разработка модулей": 4,
            "Тестирование": 1,
            "Мобильные приложения": 3,
            "C++": 6
        }
    },

    "2 курс ГД": {
        "groups": ["ГД1", "ГД2"],
        "subjects": {
            "Основы рисунка": 2,
            "Дизайн интерьера": 3,
            "ТЗ графический дизайн": 6,
            "Дизайн-проектирование": 7
        }
    },

    "3 курс РПО": {
        "groups": ["РПО"],
        "subjects": {
            "Английский": 2,
            "Физ-ра": 2,
            "HTML-CSS-JS": 6,
            "Разработка ПО": 2,
            "Инструментальные средства": 2,
            "Мат.моделирование": 2,
            "Поддержка систем": 2,
            "Качество систем": 6
        }
    },

    "3 курс ГД": {
        "groups": ["ГД"],
        "subjects": {
            "Английский": 2,
            "Многостраничный дизайн": 3,
            "Дизайн упаковки": 5,
            "Maya 3D": 2,
            "ZBrush": 1,
            "Adobe Premiere": 2,
            "Сборка дизайна": 2
        }
    }
}

teachers = {
    "Физика": "Бунед",
    "Математика": "Бунед",
    "Мат.моделирование": "Бунед",

    "C++": "Влад",
    "HTML-CSS-JS": "Влад",
    "Поддержка систем": "Влад",
    "Качество систем": "Влад",

    "Разработка модулей": "Артемий",
    "Мобильные приложения": "Артемий",
    "Тестирование": "Артемий",

    "Информатика": "Максим",
    "Биология": "Али",
    "Английский": "Татьяна",

    "Интернет-маркетинг": "Ольшанская",
    "Maya 3D": "Ольшанская",

    "Русский": "Тамара",
    "Литература": "Тамара",

    "Химия": "Юлия Вячеславовна",
    "История": "Марина",
    "Обществознание": "Марина",
    "География": "Марина",

    "Физ-ра": "Вера",

    "Illustrator": "Анна",

    "Навигационный дизайн": "Юлия",
    "Дизайн интерьера": "Юлия",
    "Дизайн-проектирование": "Юлия",
    "Многостраничный дизайн": "Юлия",
    "Сборка дизайна": "Юлия",

    "ZBrush": "Данил",
    "Adobe Premiere": "Данил"
}

def generate_schedule(subjects, global_teacher_busy):

    lessons = []
    for subject, count in subjects.items():
        lessons += [subject] * count

    random.shuffle(lessons)

    schedule = {day: [] for day in days}

    for lesson in lessons:
        placed = False

        random_days = days[:]
        random.shuffle(random_days)

        for day in random_days:

            if schedule[day] and schedule[day][-1] == lesson:
                continue

            if len(schedule[day]) >= 3:
                continue

            teacher = teachers.get(lesson)

            if teacher and (day, teacher) in global_teacher_busy:
                continue

            schedule[day].append(lesson)

            if teacher:
                global_teacher_busy[(day, teacher)] = True

            placed = True
            break

        if not placed:
            for day in days:
                if len(schedule[day]) < 3:
                    schedule[day].append(lesson)
                    break

    return schedule


all_schedules = {}
global_teacher_busy = {}

for course, data in courses.items():
    for group in data["groups"]:
        all_schedules[group] = generate_schedule(
            data["subjects"],
            global_teacher_busy
        )


@app.route("/")
def index():
    return str(all_schedules)
