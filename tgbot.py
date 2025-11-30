import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

IMAGES_FOLDER = 'images'
IMAGES_FOLDER2 = 'images2'
ANSWERS_FOLDER = 'answers'
ANSWERS_FOLDER2 = 'answers2'
PDF_FOLDER = 'pdf'  # папка, где лежат egemath*.pdf
ASKING_IMPROVEMENT_FEEDBACK = "asking_improvement_feedback"

answers_files = {
    "Планиметрия": "ege1answer.pdf",
    "Векторы": "ege2answer.pdf",
    "Стереометрия": "ege13answer.pdf",
    "Начала теории вероятностей": "ege4answer.pdf",
    "Вероятности сложных событий": "ege5answer.pdf",
    "Простейшие уравнения": "ege6answer.pdf",
    "Вычисления и преобразования": "ege7answer.pdf",
    "Производная и первообразная": "ege8answer.pdf",
    "Задачи с прикладным содержанием": "ege9answer.pdf",
    "Текстовые задачи": "ege10answer.pdf",
    "Графики функций": "ege11answer.pdf",
    "Наибольшее и наименьшее значение функций": "ege12answer.pdf"
}

tasks_data = {
    "Математика": ["ЕГЭ 1 часть", "ЕГЭ 2 часть"],
}

learning_materials = {
    "Математика": ["Алгебра", "Геометрия"],
}

answers = {
    '1': ['150', 'сто пятьдесят'],
    '2': ['3', 'три'],
    '3': ['198', 'сто девяносто восемь'],
    '4': ['0,25', '0.25'],
    '5': ['0,25', '0.25'],
    '6': ['-0,5', '-0.5'],
    '7': ['64', 'шестьдесят четыре'],
    '8': ['-7', 'минус семь'],
    '9': ['30', 'тридцать'],
    '10': ['8,4', '8.4'],
    '11': ['1', 'один'],
    '12': ['3', 'три'],
}


def get_keyboard_with_back(buttons):
    keyboard = buttons[:]
    keyboard.append([InlineKeyboardButton('Назад', callback_data='back')])
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Обучение", callback_data='learning')],
        [InlineKeyboardButton("Экзамен", callback_data='ekzamen')],
        [InlineKeyboardButton("Обратная связь", callback_data='feedback')],
        [InlineKeyboardButton("Опрос по качеству", callback_data='survey')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("Здравствуйте! Выберите раздел:", reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text("Здравствуйте! Выберите раздел:", reply_markup=reply_markup)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'learning':
        keyboard = [[InlineKeyboardButton("Математика", callback_data='learning_Matematika')]]
        await query.message.reply_text("Выберите предмет для обучения:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == 'learning_Matematika':
        keyboard = [
            [InlineKeyboardButton("Теория", callback_data='learning_theory_Matematika'),
             InlineKeyboardButton("Практика", callback_data='learning_practice_Matematika')]
        ]
        await query.message.reply_text("Выберите раздел:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == 'learning_theory_Matematika':
        await query.message.reply_text("Здесь будут материалы по теории математики.")
        return

    if data == 'learning_practice_Matematika':
        keyboard = [
            [InlineKeyboardButton("1 часть (1-12)", callback_data='learning_practice_Matematika_part1')],
            [InlineKeyboardButton("2 часть (13-19)", callback_data='learning_practice_Matematika_part2')],
        ]
        await query.message.reply_text("Выберите часть:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == 'learning_practice_Matematika_part1':
        keyboard = [
            [InlineKeyboardButton("Задания", callback_data='matematik_task_part1')],
            [InlineKeyboardButton("Ответы", callback_data='matematik_answer_part1')],
        ]
        await query.message.reply_text("Выберите действие:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == 'matematik_task_part1':
        task_names = [
            "Планиметрия", "Векторы", "Стереометрия", "Начала теории вероятностей",
            "Вероятности сложных событий", "Простейшие уравнения", "Вычисления и преобразования",
            "Производная и первообразная", "Задачи с прикладным содержанием", "Текстовые задачи",
            "Графики функций", "Наибольшее и наименьшее значение функций"
        ]
        buttons = [[InlineKeyboardButton(name, callback_data=f'part1_task_{i}')] for i, name in enumerate(task_names, 1)]
        await query.message.reply_text("Выберите название задания:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # ✅ ВСТАВЛЕННЫЙ КОД (ОТПРАВКА PDF ПО НОМЕРУ)
    if data.startswith("part1_task_"):
        try:
            task_number = int(data.split("_")[-1])
        except ValueError:
            await query.message.reply_text("Неверный номер задания.")
            return

        pdf_filename = f"egemath{task_number}.pdf"
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                await query.message.reply_document(document=f, filename=pdf_filename)
        else:
            await query.message.reply_text(f"Файл {pdf_filename} не найден в папке /{PDF_FOLDER}/")

        return

    if data == 'matematik_answer_part1':
        buttons = [
            [InlineKeyboardButton(f"Ответ к заданию {i}", callback_data=f'part1_answer_{i}')]
            for i in range(1, 13)
        ]
        await query.message.reply_text("Выберите номер задания:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    if data.startswith("part1_answer_"):
        try:
            task_number = int(data.split("_")[-1])
        except ValueError:
            await query.message.reply_text("Неверный номер задания.")
            return

        ans_filename = f"ege{task_number}answer.pdf"
        ans_path = os.path.join(PDF_FOLDER, ans_filename)

        if os.path.exists(ans_path):
            with open(ans_path, "rb") as f:
                await query.message.reply_document(document=f, filename=ans_filename)
        else:
            await query.message.reply_text(f"Файл {ans_filename} не найден в папке /{PDF_FOLDER}/")

        return

        tema_list = list(answers_files.keys())
        if 1 <= idx <= len(tema_list):
            tema_name = tema_list[idx - 1]
            ans_filename = answers_files.get(tema_name)
            if ans_filename:
                ans_path = os.path.join(PDF_FOLDER, ans_filename)
                if os.path.exists(ans_path):
                    with open(ans_path, "rb") as f:
                        await query.message.reply_document(document=f, filename=ans_filename)
                else:
                    await query.message.reply_text("Файл с ответами не найден на сервере.")
            else:
                await query.message.reply_text("Для этой темы не назначен файл с ответами.")
        else:
            await query.message.reply_text("Неверный номер.")
        return

    # Обработка выбора "Практика" в меню экзамена
    if data == 'ekzamen':
        keyboard = []
        for subject in tasks_data.keys():
            keyboard.append([
                InlineKeyboardButton(subject, callback_data=f'ekzamen_subject_{subject}'),
                InlineKeyboardButton("ЕГЭ 1 часть", callback_data=f'ege_1_{subject}'),
                InlineKeyboardButton("ЕГЭ 2 часть", callback_data=f'ege_2_{subject}')
            ])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Выберите раздел экзамена:", reply_markup=reply_markup)
        return

    if data == 'feedback':
        await query.message.reply_text("По всем вопросам и предложениям, свяжитесь с нами через @Charmant27.")
        return

    if data == 'survey':
        await query.message.reply_text("Пожалуйста, пройдите наш опрос по качеству. Спасибо!")
        questions_keyboard = [
            [InlineKeyboardButton("Как вы оцениваете качество обучения?", callback_data='question_quality')],
            [InlineKeyboardButton("Что можно улучшить?", callback_data='question_improve')],
        ]
        reply_markup = InlineKeyboardMarkup(questions_keyboard)
        await query.message.reply_text("Выберите вопрос для ответа:", reply_markup=reply_markup)
        return

    if data == 'question_quality':
        ratings_keyboard = [
            [InlineKeyboardButton("1", callback_data='rating_1')],
            [InlineKeyboardButton("2", callback_data='rating_2')],
            [InlineKeyboardButton("3", callback_data='rating_3')],
            [InlineKeyboardButton("4", callback_data='rating_4')],
            [InlineKeyboardButton("5", callback_data='rating_5')],
        ]
        reply_markup = InlineKeyboardMarkup(ratings_keyboard)
        await query.message.reply_text("Пожалуйста, выберите вашу оценку (1-5):", reply_markup=reply_markup)
        return

    if data == 'question_improve':
        await query.message.reply_text("Пожалуйста, напишите, что, по вашему мнению, можно улучшить.")
        context.user_data['waiting_for_improve_feedback'] = True
        return

    if data.startswith('rating_'):
        rating = data.split('_')[1]
        await query.message.reply_text(f"Спасибо за вашу оценку: {rating}")
        return

    if data is None:
        pass

    if data.startswith('learning_'):
        subject = data.split('_', 1)[1]
        materials = learning_materials.get(subject, [])
        if materials:
            message = f"Обучающие материалы по {subject}:\n"
            for item in materials:
                message += f"\n- {item}"
            await query.message.reply_text(message)
        else:
            await query.message.reply_text(f"Обучающие материалы по {subject} отсутствуют.")
        return

    if data.startswith('ekzamen_subject_'):
        subject = data.split('_')[-1]
        await query.message.reply_text(f"Вы выбрали экзамен по {subject}. Здесь пока нет упражнений.")
        return

    if data.startswith('ege_'):
        parts = data.split('_')
        part_type = parts[1]
        subject = parts[2]
        if part_type == '1':
            buttons = []
            for i in range(1, 13):
                callback_data = f'{subject}_task_1_{i}'
                buttons.append([InlineKeyboardButton(str(i), callback_data=callback_data)])
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.reply_text(f"Выберите задание для {subject} (часть 1):", reply_markup=reply_markup)
        elif part_type == '2':
            buttons = []
            for task_num in range(13, 20):
                callback_data = f'{subject}_task_2_{task_num}'
                buttons.append([InlineKeyboardButton(str(task_num), callback_data=callback_data)])
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.reply_text(f"Выберите задание для {subject} (часть 2):", reply_markup=reply_markup)
        return

    if '_task_' in data:
        parts = data.split('_')
        subject = parts[0]
        part_number = parts[2]
        task_number = parts[3]

        if part_number == '1':
            filename = f'ege_math{task_number}.png'
            folder = IMAGES_FOLDER
            buttons = [
                [InlineKeyboardButton("Ответить", callback_data=f'answer_{subject}_{task_number}')],
                [InlineKeyboardButton("Решение", callback_data=f'solution_{subject}_{task_number}')],
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            path = os.path.join(folder, filename)
            if os.path.exists(path):
                with open(path, 'rb') as photo:
                    await query.message.reply_photo(photo=photo, reply_markup=reply_markup)
            else:
                await query.message.reply_text("Изображение задания не найдено.")
        elif part_number == '2':
            filename = f'ege2_math{task_number}.png'
            folder = IMAGES_FOLDER2
            buttons = [
                [InlineKeyboardButton("Проверить себя", callback_data=f'check_self_{subject}_{task_number}')]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            path = os.path.join(folder, filename)
            if os.path.exists(path):
                with open(path, 'rb') as photo:
                    await query.message.reply_photo(photo=photo, reply_markup=reply_markup)
            else:
                await query.message.reply_text("Изображение задания не найдено.")
        else:
            await query.message.reply_text("Некорректный номер части.")
        return

    if data.startswith('answer_'):
        parts = data.split('_')
        subject = parts[1]
        task_number = parts[2]
        context.user_data['awaiting_answer'] = {'task_number': task_number, 'subject': subject}
        await query.message.reply_text("Пожалуйста, отправьте ваш ответ на задание.")
        return

    if data.startswith('solution_'):
        parts = data.split('_')
        subject = parts[1]
        task_number = parts[-1]
        filename = f'math_answer{task_number}.png'
        filepath = os.path.join(ANSWERS_FOLDER, filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as photo:
                await query.message.reply_photo(photo=photo)
        else:
            await query.message.reply_text("Решение для этого задания отсутствует.")
        return

    if data.startswith('check_self_'):
        parts = data.split('_')
        subject = parts[1]
        task_number = parts[-1]
        filename = f'mat_answer{task_number}.png'
        filepath = os.path.join(ANSWERS_FOLDER2, filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as photo:
                await query.message.reply_photo(photo=photo)
        else:
            await query.message.reply_text("Ответное изображение для этого задания отсутствует.")
        return


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    awaiting = context.user_data.get('awaiting_answer')
    if awaiting:
        user_answer = update.message.text.strip()
        task_number = awaiting['task_number']
        correct_answers = answers.get(task_number)

        if correct_answers:
            def normalize(ans):
                return ans.replace(',', '.').replace(' ', '').lower()

            normalized_user_answer = normalize(user_answer)
            if any(normalize(ans) == normalized_user_answer for ans in correct_answers):
                await update.message.reply_text("Верно! Вы правильно ответили.")
            else:
                correct_display = correct_answers[0]
                await update.message.reply_text(f"Неверно. Правильный ответ: {correct_display}")
        else:
            await update.message.reply_text("Ответ для этого задания не найден в базе данных.")
        context.user_data.pop('awaiting_answer', None)
        return

    if context.user_data.get('waiting_for_improve_feedback'):
        feedback_text = update.message.text
        # Сохранение отзыва можно реализовать здесь
        await update.message.reply_text("Спасибо за ваш отзыв!")
        context.user_data['waiting_for_improve_feedback'] = False
        return

    await update.message.reply_text("Спасибо за сообщение!")


if __name__ == '__main__':
    TOKEN = '8029123789:AAHCka_FonzvZjin4xS8BQQ9upHD19TQbnc'
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()