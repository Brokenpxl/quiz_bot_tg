from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
from aiogram import Router
import Utils.keyboards as keyb
import Utils.db as db
import Utils.questions as qe
import Utils.func as fn


router = Router()

# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Статистика"))
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

    # Хэндлер на команды /quiz
@router.message(F.text=="Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз
    await fn.new_quiz(message)

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса для данного пользователя
    current_question_index = await db.get_quiz_index(callback.from_user.id)

    correct_option = qe.quiz_data[current_question_index]['correct_option']

    # Отправляем в чат сообщение, что ответ верный
    await callback.message.answer(f"Верно! Это {qe.quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    #записываем правильный результат в бд
    correct_answers, total_questions = await db.get_result(callback.from_user.id)
    await db.save_result(callback.from_user.id, correct_answers + 1, total_questions + 1)

    await db.update_quiz_index(callback.from_user.id, current_question_index)

    # Проверяем достигнут ли конец квиза
    if current_question_index < len(qe.quiz_data):
        # Следующий вопрос
        await fn.get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")

@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса для данного пользователя
    current_question_index = await db.get_quiz_index(callback.from_user.id)

    correct_option = qe.quiz_data[current_question_index]['correct_option']

    # Отправляем в чат сообщение об ошибке с указанием верного ответа
    await callback.message.answer(f"Неправильно. Правильный ответ: {qe.quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    #записываем неправильный результат в бд
    correct_answers, total_questions = await db.get_result(callback.from_user.id)
    await db.save_result(callback.from_user.id, correct_answers, total_questions + 1)
    await db.update_quiz_index(callback.from_user.id, current_question_index)

    # Проверяем достигнут ли конец квиза
    if current_question_index < len(qe.quiz_data):
        # Следующий вопрос
        await fn.get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")

@router.message(F.text=="Статистика")
@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    results = await db.get_all_results()
    if not results:
        await message.answer("Статистика пока пустая")
    else:
        stats = "/n".join([f"User {user_id}: {correct}/{total}" for user_id, correct, total in results])
        await message.answer(f"Статистика игроков:\n{stats}")



@router.message()
async def handle_message(message: types.Message):
    reply_markup = types.ReplyKeyboardRemove()
    await message.answer(f"Вы ответили: {message.text}", reply_markup=reply_markup)