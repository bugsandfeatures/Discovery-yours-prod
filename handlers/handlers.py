from aiogram.types import Message, PollAnswer, CallbackQuery, MediaGroup, InputMediaPhoto, InputFile, \
    InlineKeyboardMarkup, InlineKeyboardButton, MessageEntity
from aiogram.dispatcher.filters import Command

import json
from random import choice

from bot import dp, bot
from config import Config
from config import DBConfig
from services import DataBase
from keyboards import start_keyboard, cb, start_keyboard1

db = DataBase(DBConfig.user, DBConfig.password, DBConfig.host, DBConfig.port, DBConfig.database)

@dp.message_handler(Command('start'))
async def start(message: Message):
    premium = 1 if message.from_user.is_premium == 'True' else 0
    await db.add_user(message.chat.id, message.chat.first_name, premium)
     
    await bot.send_message(chat_id=message.chat.id, text='Привет!', reply_markup=start_keyboard)

@dp.message_handler(content_types=['photo'])
async def get_content(message: Message):
    if message.chat.id == 5894913649:
        file_id = str(message.caption)
        new_file_id = str(message.photo[0].file_id)
        import mysql.connector
        connect = mysql.connector.connect(user=DBConfig.user,
                                          password=DBConfig.password,
                                          host=DBConfig.host,
                                          port=DBConfig.port,
                                          database=DBConfig.database)
        cursor = connect.cursor()
        cursor.execute("""UPDATE posts SET new_file_id=(%s) WHERE file_id=(%s)""",
                       [new_file_id, file_id])
        cursor.close()
        connect.commit()
        connect.close()

@dp.message_handler(content_types=['document'])
async def get_content(message: Message):
    if message.chat.id == 5894913649:
        file_id = str(message.caption)
        new_file_id = str(message.document.file_id)
        import mysql.connector
        connect = mysql.connector.connect(user=DBConfig.user,
                                          password=DBConfig.password,
                                          host=DBConfig.host,
                                          port=DBConfig.port,
                                          database=DBConfig.database)
        cursor = connect.cursor()
        cursor.execute("""UPDATE posts SET new_file_id=(%s) WHERE file_id=(%s)""",
                       [new_file_id, file_id])
        cursor.close()
        connect.commit()
        connect.close()

@dp.callback_query_handler(cb.filter(action='reg'))
async def registration(call: CallbackQuery):
    await call.answer(cache_time=10)
    # 'tech business crypto economics design entertainment marketing news'
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Какие темы тебе интересны❓',
                        options=['Технологии 💻',
                                 'Бизнес 💰',
                                 'Криптовалюты 🔐',
                                 'Экономика 📈',
                                 'Дизайн 🖼',
                                 'Юмор и развлечения 😂',
                                 'Маркетинг 📈',
                                 'Новости 📰'],
                        is_anonymous=False,
                        allows_multiple_answers=True)

@dp.poll_answer_handler()
async def handle_poll_answer(poll_answer: PollAnswer):
    user_id = poll_answer['user']['id']
    interests = str(poll_answer['option_ids'])

    await db.add_interests(interests, user_id)

    await bot.send_message(poll_answer.user.id, 'Готово!', reply_markup=start_keyboard1)

@dp.callback_query_handler(cb.filter(action='start'))
async def wall(call: CallbackQuery):
    await make_post(call)

async def make_post(call: CallbackQuery):
    import mysql.connector
    connect = mysql.connector.connect(user=DBConfig.user,
                                      password=DBConfig.password,
                                      host=DBConfig.host,
                                      port=DBConfig.port,
                                      database=DBConfig.database)

    cursor = connect.cursor()
    cursor.execute("""SELECT * FROM users WHERE user_id=(%s)""",
                   (call.message.chat.id,))
    interests = cursor.fetchall()[0][3]
    category_id = choice([1, 2, 3, 4, 5, 6, 7, 8]) if interests == 'all'\
        else choice([int(i) for i in interests if i in '12345678'])
    cursor.execute("""SELECT post_id FROM posts WHERE category_id=(%s)""",
                   (category_id,))
    data = cursor.fetchall()
    ids = [i[0] for i in data]
    rand_post_id = choice(ids)
    cursor.execute("""SELECT * FROM posts WHERE post_id=(%s)""", [rand_post_id])
    post_data = cursor.fetchall()
    type_of_post = post_data[0][1]
    react_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='❤️', callback_data=f'mark:like:{rand_post_id}'),
                InlineKeyboardButton(text='👎', callback_data=f'mark:dislike:{rand_post_id}')
            ],
            [
                InlineKeyboardButton(text='Реклама!!!', callback_data=f'mark:ads:{rand_post_id}'),
            ]
        ]
    )
    import ast

    # var = str((post_data[0][-1])).replace("'_': 'MessageEntity', ", "")
    # var = ast.literal_eval(var)
    # print(var)

    if type_of_post == 'text':
        await bot.send_message(call.message.chat.id,
                               post_data[0][3],
                               reply_markup=react_keyboard)

    if type_of_post == 'photo':
        if post_data[0][12] is None:
            photo = post_data[0][7]
            await bot.send_photo(chat_id=call.message.chat.id,
                                 photo=photo,
                                 caption=post_data[0][3],
                                 reply_markup=react_keyboard)
        else:
            username = post_data[0][5]
            media_group_id = post_data[0][12]
            cursor.execute("""SELECT * FROM posts WHERE username=(%s) AND media_group_id=(%s)""",
                           [username, media_group_id])
            group_data = cursor.fetchall()
            mg = MediaGroup()
            for i in range(len(group_data)):
                mg.attach_photo(group_data[i][7],
                                caption=group_data[i][3])

            await bot.send_media_group(call.message.chat.id, mg)
            await bot.send_message(call.message.chat.id, 'Реакции', reply_markup=react_keyboard)

    if type_of_post == 'document':
        if post_data[0][12] is None:
            await bot.send_document(call.message.chat.id,
                                    post_data[0][7],
                                    reply_markup=react_keyboard)

        else:
            username = post_data[0][5]
            media_group_id = post_data[0][12]
            cursor.execute("""SELECT * FROM posts WHERE username=(%s) AND media_group_id=(%s)""",
                           [username, media_group_id])
            group_data = cursor.fetchall()
            mg = MediaGroup()
            for i in range(len(group_data)):
                mg.attach_document(group_data[i][7],
                                   caption=post_data[i][3])

            await bot.send_media_group(call.message.chat.id, mg)
            await bot.send_message(call.message.chat.id, 'Реакции', reply_markup=react_keyboard)

    if type_of_post == 'web_page':
        pass

@dp.callback_query_handler(cb.filter(action='like'))
async def like_post(call: CallbackQuery, callback_data: dict):
    import mysql.connector
    connect = mysql.connector.connect(user=DBConfig.user,
                                      password=DBConfig.password,
                                      host=DBConfig.host,
                                      port=DBConfig.port,
                                      database=DBConfig.database)

    cursor = connect.cursor()
    post_id = callback_data['post_id']
    cursor.execute("""SELECT likes, dislikes, ads FROM posts""")
    data = cursor.fetchall()
    likes = data[0][0]
    dislikes = data[0][1]
    ads = data[0][2]
    await db.update_reacts(likes+1, dislikes, ads, post_id)
    connect.commit()
    cursor.close()
    connect.close()

    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    await make_post(call)

@dp.callback_query_handler(cb.filter(action='dislike'))
async def dislike_post(call: CallbackQuery, callback_data: dict):
    import mysql.connector
    connect = mysql.connector.connect(user=DBConfig.user,
                                      password=DBConfig.password,
                                      host=DBConfig.host,
                                      port=DBConfig.port,
                                      database=DBConfig.database)

    cursor = connect.cursor()
    post_id = callback_data['post_id']
    cursor.execute("""SELECT likes, dislikes, ads FROM posts""")
    data = cursor.fetchall()
    likes = data[0][0]
    dislikes = data[0][1]
    ads = data[0][2]
    await db.update_reacts(likes, dislikes+1, ads, post_id)
    connect.commit()
    cursor.close()
    connect.close()

    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    await make_post(call)

@dp.callback_query_handler(cb.filter(action='ads'))
async def ads_post(call: CallbackQuery, callback_data: dict):
    post_id = callback_data['post_id']
    await bot.send_message(call.message.chat.id, 'Спасибо, информация передана админам!')
    # 461656218,
    for i in [888899980]:
        await bot.send_message(i, f'Пост с id: {post_id} помечен, как реклама!')

    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await make_post(call)
