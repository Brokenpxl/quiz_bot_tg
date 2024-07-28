import Utils.db as db
import Utils.keyboards as keyb
import Utils.questions as qe

async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза в 0
    current_question_index = 0
    await db.update_quiz_index(user_id, current_question_index)

    await db.save_result(user_id, 0, 0)
    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)

async def get_question(message, user_id):

    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await db.get_quiz_index(user_id)
    # Получаем индекс правильного ответа для текущего вопроса
    correct_index = qe.quiz_data[current_question_index]['correct_option']
    # Получаем список вариантов ответа для текущего вопроса
    opts = qe.quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = keyb.generate_options_keyboard(opts, opts[correct_index])
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{qe.quiz_data[current_question_index]['question']}", reply_markup=kb)

