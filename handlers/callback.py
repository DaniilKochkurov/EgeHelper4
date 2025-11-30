import os
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, MessageHandler, filters
from telegram.ext import CommandHandler, ContextTypes, ApplicationBuilder
from config import (
    IMAGES_FOLDER, IMAGES_FOLDER2, ANSWERS_FOLDER, ANSWERS_FOLDER2,
    PDF_FOLDER, tasks_data, learning_materials, answers, answers_files, PDF_FOLDER2, PDF_FOLDER3
)

# Кнопка главное меню
MAIN_MENU_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
])

# Баллы для заданий
TASK_POINTS = {**{i: 1 for i in range(1, 13)}, 13: 2, 14: 3, 15: 2, 16: 2, 17: 3, 18: 4, 19: 4}



async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # -----------------------------
    # Главное меню
    # -----------------------------
    if data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("📘 Обучение", callback_data='learning')],
            [InlineKeyboardButton("📝 Экзамен", callback_data='ekzamen')],
            [InlineKeyboardButton("📊 Топ экзамена", callback_data='exam_top')],
            [InlineKeyboardButton("📊Топ недели", callback_data='weekly_top')],
            [InlineKeyboardButton("⭐ Задача недели", callback_data="weekly_task")],
            [InlineKeyboardButton("💯 Отзывы", callback_data='show_feedback')]
        ]
        await query.message.reply_text("🏠 Главное меню:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # -----------------------------
    # ОБУЧЕНИЕ
    # -----------------------------
    if data == 'learning':
        keyboard = [[InlineKeyboardButton("Математика", callback_data='learning_Matematika')],
                    [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
        await query.message.reply_text("Выберите предмет:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == 'learning_Matematika':
        keyboard = [
            [InlineKeyboardButton("Теория", callback_data='learning_theory_Matematika'),
             InlineKeyboardButton("Практика", callback_data='learning_practice_Matematika')],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        await query.message.reply_text("Выберите раздел:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == 'learning_practice_Matematika':
        keyboard = [
            [InlineKeyboardButton("1 часть", callback_data='learning_practice_Matematika_part1')],
            [InlineKeyboardButton("2 часть", callback_data='learning_practice_Matematika_part2')],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        await query.message.reply_text("Выберите часть практики:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == 'learning_theory_Matematika':
        keyboard = [
            [InlineKeyboardButton("1 часть", callback_data='theory_part1')],
            [InlineKeyboardButton("2 часть", callback_data='theory_part2')],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        await query.message.reply_text("Выберите раздел теории:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == 'theory_part1':
        theory_topics = [
            "Планиметрия", "Векторы", "Стереометрия", "Теория вероятности и Сложные вероятности",
            "Простейшие уравнения", "Вычисления", "Производная", "Прикладные задачи",
            "Текстовые задачи", "Графики функций", "Наибольшее и наименьшее значение функций"
        ]
        buttons = [[InlineKeyboardButton(topic, callback_data=f"theory_topic_{i}")] for i, topic in enumerate(theory_topics, 1)]
        buttons.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])
        await query.message.reply_text("Выберите тему 1 части:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    if data == 'theory_part2':
        topics2 = [
            "Уравнения", "Стереометрическая задача", "Неравенства",
            "Финансовая математика", "Планиметрическая задача",
            "Задача с параметром", "Числа и их свойства"
        ]
        buttons = [[InlineKeyboardButton(topic, callback_data=f"theory2_topic_{13 + i}")] for i, topic in enumerate(topics2)]
        buttons.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])
        await query.message.reply_text("Выберите тему 2 части:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    if data.startswith("theory_topic_"):
        number = int(data.split("_")[-1])
        filename = f"Teoria_k_zadaniyu_{number}.pdf"
        path = os.path.join("teory1", filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_document(document=f, filename=filename)
        else:
            await query.message.reply_text(f"Файл с теорией для задания {number} не найден.", reply_markup=MAIN_MENU_KEYBOARD)
        return

    if data.startswith("theory2_topic_"):
        number = int(data.split("_")[-1])
        filename = f"Teoria_k_zadaniyu_{number}.pdf"
        path = os.path.join("teory2", filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_document(document=f, filename=filename)
        else:
            await query.message.reply_text(f"Файл с теорией для задания {number} не найден.", reply_markup=MAIN_MENU_KEYBOARD)
        return

    # -----------------------------
    # ПРАКТИКА → 1 часть
    # -----------------------------
    if data == 'learning_practice_Matematika_part1':
        keyboard = [
            [InlineKeyboardButton("Задания", callback_data='matematik_task_part1')],
            [InlineKeyboardButton("Ответы", callback_data='matematik_answer_part1')],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        await query.message.reply_text("Выберите действие:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == 'matematik_task_part1':
        task_names = [
            "Планиметрия", "Векторы", "Стереометрия", "Теория вероятностей",
            "Сложные вероятности", "Простейшие уравнения", "Вычисления",
            "Производная", "Прикладные задачи", "Текстовые задачи",
            "Графики функций", "Наибольшее/наименьшее"
        ]
        buttons = [[InlineKeyboardButton(name, callback_data=f'part1_task_{i}')] for i, name in enumerate(task_names, 1)]
        buttons.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])
        await query.message.reply_text("Выберите задание (1 часть):", reply_markup=InlineKeyboardMarkup(buttons))
        return

    if data.startswith("part1_task_"):
        number = int(data.split("_")[-1])
        filename = f"egemath{number}.pdf"
        path = os.path.join(PDF_FOLDER, filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_document(document=f, filename=filename)
        else:
            await query.message.reply_text(f"Файл {filename} не найден.", reply_markup=MAIN_MENU_KEYBOARD)
        return

    if data == 'matematik_answer_part1':
        task_names = [
            "Планиметрия", "Векторы", "Стереометрия", "Теория вероятностей",
            "Сложные вероятности", "Простейшие уравнения", "Вычисления",
            "Производная", "Прикладные задачи", "Текстовые задачи",
            "Графики функций", "Наибольшее/наименьшее"
        ]
        buttons = [[InlineKeyboardButton(name, callback_data=f"part1_answer_{i}")] for i, name in enumerate(task_names, 1)]
        buttons.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])
        await query.message.reply_text("Выберите задачу (1 часть):", reply_markup=InlineKeyboardMarkup(buttons))
        return

    if data.startswith("part1_answer_"):
        number = int(data.split("_")[-1])
        filename = f"ege{number}answer.pdf"
        path = os.path.join(PDF_FOLDER, filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_document(document=f, filename=filename)
        else:
            await query.message.reply_text(f"Ответ {filename} не найден.", reply_markup=MAIN_MENU_KEYBOARD)
        return

    # -----------------------------
    # ПРАКТИКА → 2 часть
    # -----------------------------
    if data == 'learning_practice_Matematika_part2':
        keyboard = [
            [InlineKeyboardButton("Задания", callback_data='part2_tasks')],
            [InlineKeyboardButton("Решения", callback_data='part2_answers')],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        await query.message.reply_text("Выберите действие:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    part2_topics = [
        "Уравнения", "Стереометрическая задача", "Неравенства",
        "Финансовая математика", "Планиметрическая задача",
        "Задача с параметром", "Числа и их свойства"
    ]

    if data == 'part2_tasks':
        buttons = [[InlineKeyboardButton(topic, callback_data=f"part2_task_{i + 13}")] for i, topic in enumerate(part2_topics)]
        buttons.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])
        await query.message.reply_text("Выберите тему задания:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    if data == 'part2_answers':
        buttons = [[InlineKeyboardButton(topic, callback_data=f"part2_answer_{i + 13}")] for i, topic in enumerate(part2_topics)]
        buttons.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])
        await query.message.reply_text("Выберите тему решения:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    if data.startswith("part2_task_"):
        number = int(data.split("_")[-1])
        filename = f"egemath{number}.pdf"
        path = os.path.join(PDF_FOLDER2, filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_document(document=f, filename=filename)
        else:
            await query.message.reply_text(f"Файл {filename} не найден.", reply_markup=MAIN_MENU_KEYBOARD)
        return

    if data.startswith("part2_answer_"):
        number = int(data.split("_")[-1])
        filename = f"ege{number}answer.pdf"
        path = os.path.join(PDF_FOLDER2, filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_document(document=f, filename=filename)
        else:
            await query.message.reply_text(f"Ответ {filename} не найден.", reply_markup=MAIN_MENU_KEYBOARD)
        return


    # Остальная логика экзамена, недельных задач, результатов и отзывов остаётся без изменений...

    if data == "weekly_task":
        from datetime import datetime, timedelta
        keyboard = [
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        # Дата старта бота
        if "bot_start_date" not in context.bot_data:
            context.bot_data["bot_start_date"] = datetime.now()
        start_date = context.bot_data["bot_start_date"]

        # Считаем номер недели
        days_passed = (datetime.now() - start_date).days
        week_index = days_passed // 7

        # Список файлов недельных задач
        folder = "weekly_task"
        available = sorted(f for f in os.listdir(folder) if f.startswith("week") and f.endswith(".png"))
        if not available:
            await query.message.reply_text("Задачи недели пока не добавлены.",reply_markup=InlineKeyboardMarkup(keyboard))
            return

        # Выбираем файл текущей недели
        filename = available[week_index % len(available)]
        path = os.path.join(folder, filename)

        # Таймер до конца недели (воскресенье 23:59:59)
        now = datetime.now()
        days_until_sunday = 6 - now.weekday()
        end_of_week = datetime(year=now.year, month=now.month, day=now.day,
                               hour=23, minute=59, second=59) + timedelta(days=days_until_sunday)
        time_remaining = end_of_week - now
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Сохраняем информацию о задаче у пользователя
        context.user_data["weekly_task"] = {
            "filename": filename,
            "attempts": 3,
            "start_time": datetime.now()
        }

        # Отправляем задачу недели
        with open(path, "rb") as f:
            await query.message.reply_photo(f)

        keyboard = [[InlineKeyboardButton("Ответить", callback_data="weekly_task_answer")]]
        await query.message.reply_text(
            f"⭐ Задача недели\n⏱ До конца недели осталось: {time_remaining.days} дней, {hours} часов, {minutes} минут",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # -----------------------------
    # Ответ на задачу недели
    # -----------------------------
    if data == "weekly_task_answer":
        weekly_task = context.user_data.get("weekly_task")
        if not weekly_task:
            await query.message.reply_text("Ошибка: задача недели не найдена.")
            return

        if weekly_task["attempts"] <= 0:
            keyboard = [[InlineKeyboardButton("Показать решение", callback_data="weekly_task_solution")]
                        , [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
                        ]
            await query.message.reply_text(
                "Попытки закончились! Вы можете посмотреть решение:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

        context.user_data["awaiting_weekly_answer"] = True
        await query.message.reply_text(
            f"Введите ваш ответ на задачу недели. Осталось попыток: {weekly_task['attempts']}"
        )
        return

    # -----------------------------
    # ПРАКТИКА → 1 часть
    # -----------------------------
    if data == 'learning_practice_Matematika_part1':
        keyboard = [
            [InlineKeyboardButton("Задания", callback_data='matematik_task_part1')],
            [InlineKeyboardButton("Ответы", callback_data='matematik_answer_part1')],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        await query.message.reply_text("Выберите действие:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == 'matematik_task_part1':
        task_names = [
            "Планиметрия", "Векторы", "Стереометрия", "Теория вероятностей",
            "Сложные вероятности", "Простейшие уравнения", "Вычисления",
            "Производная", "Прикладные задачи", "Текстовые задачи",
            "Графики функций", "Наибольшее/наименьшее"
        ]
        buttons = [[InlineKeyboardButton(name, callback_data=f'part1_task_{i}')] for i, name in enumerate(task_names, 1)],[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        await query.message.reply_text("Выберите задание (1 часть):", reply_markup=InlineKeyboardMarkup(buttons))
        return

    if data.startswith("part1_task_"):
        number = int(data.split("_")[-1])
        filename = f"egemath{number}.pdf"
        path = os.path.join(PDF_FOLDER, filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_document(document=f, filename=filename)
        else:
            await query.message.reply_text(f"Файл {filename} не найден.")
        return

    if data == 'matematik_answer_part1':
        task_names = [
            "Планиметрия", "Векторы", "Стереометрия", "Теория вероятностей",
            "Сложные вероятности", "Простейшие уравнения", "Вычисления",
            "Производная", "Прикладные задачи", "Текстовые задачи",
            "Графики функций", "Наибольшее/наименьшее"
        ]
        buttons = [[InlineKeyboardButton(name, callback_data=f"part1_answer_{i}")] for i, name in enumerate(task_names, 1)],[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        await query.message.reply_text("Выберите задачу (1 часть):", reply_markup=InlineKeyboardMarkup(buttons))
        return

    if data.startswith("part1_answer_"):
        number = int(data.split("_")[-1])
        filename = f"ege{number}answer.pdf"
        path = os.path.join(PDF_FOLDER, filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_document(document=f, filename=filename)
        else:
            await query.message.reply_text(f"Ответ {filename} не найден.")
        return

    # -----------------------------
    # ЭКЗАМЕН
    # -----------------------------
    if data == "ekzamen":
        keyboard = [
            [InlineKeyboardButton("Профильная математика", callback_data="exam_profile")],[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        await query.message.reply_text("Выберите предмет:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == "exam_profile":
        keyboard = [
            [InlineKeyboardButton("1 часть", callback_data="exam_p1")],
            [InlineKeyboardButton("2 часть", callback_data="exam_p2")],
            [InlineKeyboardButton("Результат", callback_data="exam_result")]
            , [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        await query.message.reply_text("Выберите часть или результат:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == "exam_p1":
        buttons = [[InlineKeyboardButton(f"Задание {i}", callback_data=f"p1_task_{i}")] for i in range(1, 13)]
        await query.message.reply_text("Выберите задание 1 части:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    if data == "exam_p2":
        buttons = [[InlineKeyboardButton(f"Задание {i}", callback_data=f"p2_task_{i}")] for i in range(13, 20)]
        await query.message.reply_text("Выберите задание 2 части:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # -----------------------------
    # Задания 1 части
    # -----------------------------
    if data.startswith("p1_task_"):
        number = int(data.split("_")[-1])
        filename = f"ege_math{number}.png"
        path = os.path.join(IMAGES_FOLDER, filename)

        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_photo(f)

            next_buttons = [
                [InlineKeyboardButton("Ответить", callback_data=f"p1_answer_{number}")],[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ]

            if number < 12:
                next_buttons.append(
                    [InlineKeyboardButton("Следующее задание ➡️", callback_data=f"p1_task_{number + 1}")]
                )
            else:
                next_buttons.append(
                    [InlineKeyboardButton("Перейти ко 2 части", callback_data="exam_p2")]
                )

            await query.message.reply_text(
                "Введите ответ или перейдите дальше:",
                reply_markup=InlineKeyboardMarkup(next_buttons)
            )

        else:
            await query.message.reply_text("Фото задания не найдено.")
        return

    if data.startswith("p1_answer_"):
        number = int(data.split("_")[-1])
        context.user_data["awaiting_p1"] = number
        await query.message.reply_text(f"Введите ваш ответ на задание {number}:")
        return
    if data.startswith("p1_show_solution_"):
        number = int(data.split("_")[-1])
        filename = f"math_answer{number}.png"
        path = os.path.join(ANSWERS_FOLDER, filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_photo(f)
        else:
            await query.message.reply_text(f"Файл с решением для задания {number} не найден.")
        return
    # -----------------------------
    # Задания 2 части
    # -----------------------------
    if data.startswith("p2_task_"):
        number = int(data.split("_")[-1])
        filename = f"ege2_math{number}.png"
        path = os.path.join(IMAGES_FOLDER2, filename)

        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_photo(f)

            keyboard = [
                [InlineKeyboardButton("Решил верно", callback_data=f"p2_correct_{number}")],
                [InlineKeyboardButton("Решил неверно", callback_data=f"p2_wrong_{number}")],
                [InlineKeyboardButton("Показать ответ", callback_data=f"p2_show_answer_{number}")],[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ]

            # КНОПКА "Следующее задание"
            if number < 19:
                keyboard.append(
                    [InlineKeyboardButton("Следующее задание ➡️", callback_data=f"p2_task_{number + 1}")]
                )
            else:
                keyboard.append(
                    [InlineKeyboardButton("Показать результат", callback_data="exam_result")]
                )

            await query.message.reply_text(
                "Выберите действие:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await query.message.reply_text("Изображение задания не найдено.")
        return

    if data.startswith("p2_show_answer_"):
        number = int(data.split("_")[-1])
        path = os.path.join(ANSWERS_FOLDER2, f"ege2_math{number}.png")
        if os.path.exists(path):
            with open(path, "rb") as f:
                await query.message.reply_photo(f)
        else:
            await query.message.reply_text("Ответ не найден.")
        return

    if data.startswith("p2_correct_") or data.startswith("p2_wrong_"):
        number = int(data.split("_")[-1])
        correct = data.startswith("p2_correct_")

        if 'p2_score' not in context.user_data:
            context.user_data['p2_score'] = 0
            context.user_data['p2_done'] = set()

        if number not in context.user_data['p2_done']:
            if correct:
                context.user_data['p2_score'] += TASK_POINTS.get(number, 0)
            context.user_data['p2_done'].add(number)

        await query.message.reply_text(f"Задание {number} отмечено как {'верное' if correct else 'неверное'}")
        return

    # -----------------------------
    # РЕЗУЛЬТАТ ЭКЗАМЕНА
    # -----------------------------
    if data == "exam_result":
        p1_score = context.user_data.get('p1_score', 0)
        p2_score = context.user_data.get('p2_score', 0)
        total_score = p1_score + p2_score
        max_score = 12 + sum(TASK_POINTS[i] for i in range(13, 20))
        percent = total_score / max_score * 100
        mark = 2 if percent < 50 else 3 if percent <= 75 else 4 if percent <= 85 else 5

        # Сохраняем результат пользователя в бот данные
        if "exam_results" not in context.bot_data:
            context.bot_data["exam_results"] = {}
        context.bot_data["exam_results"][update.effective_user.id] = {
            "name": update.effective_user.full_name,
            "score": total_score
        }

        # Кнопка обнуления результата
        keyboard_result = [
            [InlineKeyboardButton("🔄 Обнулить результат", callback_data="reset_result")],[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        await query.message.reply_text(
            f"Экзамен завершен!\nБаллы: {total_score}/{max_score}\nПроцент: {percent:.1f}%\nОценка: {mark}",
            reply_markup=InlineKeyboardMarkup(keyboard_result)
        )

        # Кнопки для оценки бота
        keyboard_feedback = [
            [InlineKeyboardButton(str(i), callback_data=f"feedback_{i}") for i in range(1, 6)]
        ]
        await query.message.reply_text(
            "Пожалуйста, оцените работу бота от 1 до 5:",
            reply_markup=InlineKeyboardMarkup(keyboard_feedback)
        )
        return

    # -----------------------------
    # ОБНУЛЕНИЕ РЕЗУЛЬТАТА
    # -----------------------------
    # -----------------------------
    # ОБНУЛЕНИЕ РЕЗУЛЬТАТА
    # -----------------------------
    if data == "reset_result":

        # Полный список ключей экзамена, которые нужно очищать
        keys_to_clear = [
            "p1_score",
            "p2_score",
            "p1_done",
            "p2_done",
            "p1_answers",
            "p2_answers",
            "awaiting_p1",
            "awaiting_p2",
        ]

        for key in keys_to_clear:
            context.user_data.pop(key, None)

        await query.message.reply_text(
            "✅ Результат обнулён! Теперь вы можете заново проходить экзамен.\n"
            "Выберите часть:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("1 часть", callback_data="exam_p1")],
                [InlineKeyboardButton("2 часть", callback_data="exam_p2")],
                [InlineKeyboardButton("Результат", callback_data="exam_result")],[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ])
        )
        return






    # -----------------------------
    # Сбор оценок пользователей
    # -----------------------------
    if data.startswith("feedback_"):
        rating = int(data.split("_")[1])

        # сохраняем у пользователя (опционально)
        context.user_data['bot_rating'] = rating

        # сохраняем во все оценки для подсчета среднего
        if "all_feedbacks" not in context.bot_data:
            context.bot_data["all_feedbacks"] = []
        context.bot_data["all_feedbacks"].append(rating)

        # Отправка владельцу бота сразу (оценки)
        OWNER_ID = 1225488154  # замените на ваш Telegram user_id
        user_name = update.effective_user.full_name
        user_username = update.effective_user.username or "не указан"
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"Пользователь {user_name} (@{user_username}) оценил бота: {rating}/5"
        )

        # Если оценка меньше 4, просим написать отзыв
        if rating < 6:
            context.user_data['awaiting_feedback_text'] = True
            await query.message.reply_text(
                "Спасибо за вашу оценку \nМожете, пожалуйста, кратко написать, что вам понравилось, а что нет? "
                "Ваш отзыв поможет нам сделать бота лучше."
            )
        else:
            await query.message.reply_text(f"Спасибо за оценку! Вы поставили: {rating}/5 ⭐")
        return

        # сохраняем во все оценки для подсчета среднего
        if "all_feedbacks" not in context.bot_data:
            context.bot_data["all_feedbacks"] = []
        context.bot_data["all_feedbacks"].append(rating)

        await query.message.reply_text(f"Спасибо за оценку! Вы поставили: {rating}/5 ⭐")

        # Отправка владельцу бота
        OWNER_ID = 1225488154  # замените на ваш Telegram user_id
        user_name = update.effective_user.full_name
        user_username = update.effective_user.username or "не указан"
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"Пользователь {user_name} (@{user_username}) оценил бота: {rating}/5"
        )
        return

    # -----------------------------
    # Кнопка "Отзывы" — среднее арифметическое всех оценок
    # -----------------------------
    if data == "show_feedback":
        keyboard = [
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        feedbacks = context.bot_data.get("all_feedbacks", [])
        if feedbacks:
            average = sum(feedbacks) / len(feedbacks)
            await query.message.reply_text(f"Средняя оценка бота: {average:.2f}/5 ⭐",reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.message.reply_text("Пока нет оценок.",reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == "exam_top":
        keyboard = [
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        results = context.bot_data.get("exam_results", {})
        if not results:
            await query.message.reply_text("Пока нет результатов экзамена.", reply_markup=InlineKeyboardMarkup(keyboard))
            return

        # Сортируем пользователей по баллам (убывание)
        top_users = sorted(results.values(), key=lambda x: x["score"], reverse=True)[:10]
        message = "🏆 Топ 10 пользователей по экзамену:\n\n"
        for i, user in enumerate(top_users, 1):
            message += f"{i}. {user['name']} — {user['score']} баллов\n"

        await query.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    if data == "weekly_top":
        from datetime import datetime
        keyboard = [
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        # текущая неделя
        start_date = context.bot_data.get("bot_start_date", datetime.now())
        days_passed = (datetime.now() - start_date).days
        week_index = days_passed // 7

        # файл недели (для соответствия с задачей недели)
        week_file = f"week{week_index % 4 + 1}.png"  # используем цикл week1-week4

        top_list = context.bot_data.get("weekly_top", {}).get(week_file, [])
        if not top_list:
            await query.message.reply_text("Пока никто не решил эту задачу недели.", reply_markup=InlineKeyboardMarkup(keyboard))
            return

        # сортировка по времени решения
        def parse_time(t):
            minutes, seconds = map(int, t.replace(" сек", "").split(" мин "))
            return minutes * 60 + seconds

        top_list_sorted = sorted(top_list, key=lambda x: parse_time(x["time"]))[:10]

        message = "🏆 Топ 10 недели:\n\n"
        for i, user in enumerate(top_list_sorted, 1):
            message += f"{i}. {user['username']} — {user['time']}\n"

        await query.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
        return

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    user_answer = update.message.text.strip()
    if update.message and update.message.text:
        user_text = update.message.text.strip()
    else:
        return
    # Если бот ожидает текст отзыва
    if context.user_data.get("awaiting_feedback_text"):
        feedback = user_text
        context.user_data.pop("awaiting_feedback_text", None)

        # Отправляем отзыв владельцу бота
        OWNER_ID = 1225488154
        user_name = update.effective_user.full_name
        user_username = update.effective_user.username or "не указан"
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"Отзыв от {user_name} (@{user_username}): {feedback}"
        )

        await update.message.reply_text("Спасибо за ваш отзыв! Мы обязательно его учтем 👍")
        return

    # -----------------------------
    # Ответ на задачу недели
    # -----------------------------
    if context.user_data.get("awaiting_weekly_answer"):
        weekly_task = context.user_data.get("weekly_task")
        if not weekly_task:
            await update.message.reply_text("Ошибка: задача недели не найдена.")
            context.user_data.pop("awaiting_weekly_answer", None)
            return

        user_text = user_answer
        weekly_task["attempts"] -= 1
        context.user_data.pop("awaiting_weekly_answer", None)

        WEEKLY_ANSWERS = {
            "week1.png": "1120",
            "week2.png": "100",
            "week3.png": "42",
            "week4.png": "100",
        }
        correct_answer = WEEKLY_ANSWERS.get(weekly_task["filename"], "")

        if user_text == correct_answer:
            await update.message.reply_text("✅ Правильно! Отличная работа!")
            from datetime import datetime
            end_time = datetime.now()
            start_time = weekly_task.get("start_time", end_time)
            time_taken = end_time - start_time
            minutes, seconds = divmod(time_taken.seconds, 60)
            formatted_time = f"{minutes} мин {seconds} сек"

            if "weekly_top" not in context.bot_data:
                context.bot_data["weekly_top"] = {}
            week_file = weekly_task["filename"]
            if week_file not in context.bot_data["weekly_top"]:
                context.bot_data["weekly_top"][week_file] = []

            user_name = update.effective_user.username or update.effective_user.full_name
            context.bot_data["weekly_top"][week_file].append({
                "username": user_name,
                "time": formatted_time
            })

            context.user_data.pop("weekly_task", None)
        else:
            if weekly_task["attempts"] > 0:
                await update.message.reply_text(
                    f"❌ Неправильно. Осталось попыток: {weekly_task['attempts']}\nПопробуйте ещё раз, нажмите 'Ответить'."
                )
            else:
                from telegram import InlineKeyboardButton, InlineKeyboardMarkup
                keyboard = [[InlineKeyboardButton("Показать решение", callback_data="weekly_task_solution")]]
                await update.message.reply_text(
                    "❌ Попытки закончились! Вы можете посмотреть решение:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
        return

    # -----------------------------
    # Ответ на задание 1 части экзамена (с проверкой)
    # -----------------------------
    elif "awaiting_p1" in context.user_data:
        task_number = context.user_data["awaiting_p1"]
        context.user_data.pop("awaiting_p1")

        if "p1_done" not in context.user_data:
            context.user_data["p1_done"] = set()

        if task_number in context.user_data["p1_done"]:
            await update.message.reply_text(f"❌ Вы уже отвечали на задание {task_number}. Нельзя решать его повторно.")
            return

        # Словарь правильных ответов для 1 части
        P1_CORRECT_ANSWERS = {
            1: ['150'],
            2: ['3'],
            3: ['198'],
            4: ['0.25', '0,25'],
            5: ['0.25', '0,25'],
            6: ['-0.5', '-0,5'],
            7: ['64'],
            8: ['-7'],
            9: ['30'],
            10: ['8.4', '8,4'],
            11: ['1'],
            12: ['3']
        }

        user_normalized = user_answer.replace(',', '.').lower()
        correct_variants = [ans.lower().replace(',', '.') for ans in P1_CORRECT_ANSWERS.get(task_number, [])]

        if user_normalized in correct_variants:
            context.user_data['p1_score'] = context.user_data.get('p1_score', 0) + 1
            await update.message.reply_text(
                f"✅ Верно! Ваш ответ на задание {task_number} правильный. Баллы: {context.user_data['p1_score']}",
                reply_markup=MAIN_MENU_KEYBOARD  # кнопка Главное меню
            )
        else:
            # Кнопка "Решение" + Главное меню
            solution_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📄 Решение", callback_data=f"p1_show_solution_{task_number}")],
            ])
            await update.message.reply_text(
                f"❌ Неверно. Правильный ответ: {P1_CORRECT_ANSWERS[task_number][0]}",
                reply_markup=solution_keyboard
            )

        # сохраняем введенный ответ
        if "p1_answers" not in context.user_data:
            context.user_data["p1_answers"] = {}
        context.user_data["p1_answers"][task_number] = user_answer

        # отмечаем задание как решенное
        context.user_data["p1_done"].add(task_number)

# Главное меню
async def cmd_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 Обучение", callback_data='learning')],
        [InlineKeyboardButton("📝 Экзамен", callback_data='ekzamen')],
        [InlineKeyboardButton("📊 Топ экзамена", callback_data='exam_top')],
        [InlineKeyboardButton("📊 Топ недели", callback_data='weekly_top')],
        [InlineKeyboardButton("⭐ Задача недели", callback_data="weekly_task")],
        [InlineKeyboardButton("💯 Отзывы", callback_data='show_feedback')]
    ]
    await update.message.reply_text(
        "🏠 Главное меню:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Экзамен
async def cmd_ekzamen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Профильная математика", callback_data="exam_profile")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]
    await update.message.reply_text(
        "Выберите предмет для экзамена:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Теория
async def cmd_theory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1 часть", callback_data='theory_part1')],
        [InlineKeyboardButton("2 часть", callback_data='theory_part2')],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]
    await update.message.reply_text(
        "Выберите часть теории:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Практика
async def cmd_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1 часть", callback_data='learning_practice_Matematika_part1')],
        [InlineKeyboardButton("2 часть", callback_data='learning_practice_Matematika_part2')],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]
    await update.message.reply_text(
        "Выберите часть практики:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Задача недели
async def cmd_weekly_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from datetime import datetime, timedelta
    keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
    start_date = context.bot_data.get("bot_start_date", datetime.now())
    days_passed = (datetime.now() - start_date).days
    week_index = days_passed // 7

    folder = "weekly_task"
    available = sorted(f for f in os.listdir(folder) if f.startswith("week") and f.endswith(".png"))
    if not available:
        await update.message.reply_text("Задачи недели пока не добавлены.", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    filename = available[week_index % len(available)]
    path = os.path.join(folder, filename)

    now = datetime.now()
    days_until_sunday = 6 - now.weekday()
    end_of_week = datetime(year=now.year, month=now.month, day=now.day,
                           hour=23, minute=59, second=59) + timedelta(days=days_until_sunday)
    time_remaining = end_of_week - now
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    context.user_data["weekly_task"] = {
        "filename": filename,
        "attempts": 3,
        "start_time": datetime.now()
    }

    with open(path, "rb") as f:
        await update.message.reply_photo(f)

    keyboard = [[InlineKeyboardButton("Ответить", callback_data="weekly_task_answer")]]
    await update.message.reply_text(
        f"⭐ Задача недели\n⏱ До конца недели осталось: {time_remaining.days} дней, {hours} часов, {minutes} минут",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Топ экзамена
async def cmd_exam_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
    results = context.bot_data.get("exam_results", {})
    if not results:
        await update.message.reply_text("Пока нет результатов экзамена.", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    top_users = sorted(results.values(), key=lambda x: x["score"], reverse=True)[:10]
    message = "🏆 Топ 10 пользователей по экзамену:\n\n"
    for i, user in enumerate(top_users, 1):
        message += f"{i}. {user['name']} — {user['score']} баллов\n"
    await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))

# Топ недели
async def cmd_weekly_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from datetime import datetime
    keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
    start_date = context.bot_data.get("bot_start_date", datetime.now())
    days_passed = (datetime.now() - start_date).days
    week_index = days_passed // 7

    week_file = f"week{week_index % 4 + 1}.png"
    top_list = context.bot_data.get("weekly_top", {}).get(week_file, [])
    if not top_list:
        await update.message.reply_text("Пока никто не решил эту задачу недели.", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    def parse_time(t):
        minutes, seconds = map(int, t.replace(" сек", "").split(" мин "))
        return minutes * 60 + seconds

    top_list_sorted = sorted(top_list, key=lambda x: parse_time(x["time"]))[:10]
    message = "🏆 Топ 10 недели:\n\n"
    for i, user in enumerate(top_list_sorted, 1):
        message += f"{i}. {user['username']} — {user['time']}\n"
    await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))

# Отзывы
async def cmd_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
    feedbacks = context.bot_data.get("all_feedbacks", [])
    if feedbacks:
        average = sum(feedbacks) / len(feedbacks)
        await update.message.reply_text(f"Средняя оценка бота: {average:.2f}/5 ⭐", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("Пока нет оценок.", reply_markup=InlineKeyboardMarkup(keyboard))

app = ApplicationBuilder().token("8534051142:AAGBafxhXxVMds5aYn9NChfNrz-9e_xTHRs").build()

app.add_handler(CommandHandler("menu", cmd_menu))
app.add_handler(CommandHandler("exam", cmd_ekzamen))
app.add_handler(CommandHandler("theory", cmd_theory))
app.add_handler(CommandHandler("practice", cmd_practice))
app.add_handler(CommandHandler("weekly_task", cmd_weekly_task))
app.add_handler(CommandHandler("exam_top", cmd_exam_top))
app.add_handler(CommandHandler("weekly_top", cmd_weekly_top))
app.add_handler(CommandHandler("feedback", cmd_feedback))

# твой CallbackQueryHandler
# app.add_handler(CallbackQueryHandler(handle_callback))


app.run_polling()
