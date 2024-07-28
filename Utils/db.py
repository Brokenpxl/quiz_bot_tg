import aiosqlite

# Зададим имя базы данных
DB_NAME = 'quiz_bot.db'

async def create_table():
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect('quiz_bot.db') as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        # Выполняем SQL-запрос к базе данных для сохранения результата
        await db.execute('''CREATE TABLE IF NOT EXISTS results (user_id INTEGER PRIMARY KEY, correct_answers INTEGER NOT NULL, total_questions INTEGER NOT NULL)''')
        # Сохраняем изменения
        await db.commit()

async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            row = await cursor.fetchone()
            if row is not None:
                return row[0]
            else:
                return 0
        
async def update_quiz_index(user_id, index):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Сохраняем изменения
        await db.commit()

async def save_result(user_id, correct_answers, total_questions):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''INSERT OR REPLACE INTO results (user_id, correct_answers, total_questions) VALUES (?, ?, ?)''', (user_id, correct_answers, total_questions))
        await db.commit()

async def get_result(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT correct_answers, total_questions FROM results WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row if row else (0, 0)
        
async def get_all_results():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT user_id, correct_answers, total_questions FROM results') as cursor:
            rows = await cursor.fetchall()
            return rows