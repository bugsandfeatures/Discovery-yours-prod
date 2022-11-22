from aiogram.types import Message, PollAnswer, CallbackQuery, MediaGroup, InputMediaPhoto, InputFile
from aiogram.dispatcher.filters import Command

import json
from random import choice

from src.bot import dp, bot
from src.config import Config
from src.config import DBConfig
from src.services import DataBase
from src.keyboards import start_keyboard, cb, start_keyboard1, react_keyboard

db = DataBase(DBConfig.user, DBConfig.password, DBConfig.host, DBConfig.port, DBConfig.database)

@dp.message_handler(Command('start'))
async def start(message: Message):
    premium = 1 if message.from_user.is_premium == 'True' else 0
    await db.add_user(message.chat.id, message.chat.first_name, premium)
     
    await bot.send_message(chat_id=message.chat.id, text='Привет!', reply_markup=start_keyboard)

@dp.callback_query_handler(cb.filter(action='reg'))
async def registration(call: CallbackQuery):
    await call.answer(cache_time=10)
    # ['it', 'travels', 'news', 'marketing', 'tech', 'entertainment', 'blogs', 'business', 'crypto', 'economics']
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Какие темы тебе интересны❓',
                        options=['Программирование 💻', # 0
                                 'Путешествие 🏖', # 1
                                 'Новости и СМИ 📰', # 2
                                 'Маркетинг и реклама 📈', # 3
                                 'Технологии ⌚️', # 4
                                 'Юмор и развлечения 😂', # 5
                                 'Блоги 📹', # 6
                                 'Бизнес и стартапы 💰', # 7
                                 'Криптовалюты 🔐', # 8
                                 'Экономика и финансы 💵'], # 9
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

# @dp.callback_query_handler(cb.filter(action='like'))
# async def like_post(call: CallbackQuery):
#     await call.answer(cache_time=None)
#     connect = sqlite3.connect('DiscoveryDB.db')
#     cursor = connect.cursor()
#     data = cursor.execute("""SELECT * FROM channel""").fetchall()
#     # rn = cursor.execute("""SELECT rand FROM users WHERE user_id=(?)""", [call.message.chat.id]).fetchall()[0][0]
#     id = data[rn][0]
#     like = data[rn][8]
#     cursor.execute("""UPDATE channel SET like=(?) WHERE id=(?)""", [int(like)+1, id])
#
#     connect.commit()
#     cursor.close()
#     connect.close()
#
#     await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
#
#     await make_post(call)
#
# @dp.callback_query_handler(cb.filter(action='dislike'))
# async def dislike_post(call: CallbackQuery):
#     await call.answer(cache_time=None)
#     connect = sqlite3.connect('DiscoveryDB.db')
#     cursor = connect.cursor()
#     cursor.execute("""SELECT * FROM channel""")
#     data = cursor.fetchall()
#     cursor.close()
#     cursor = connect.cursor()
#     rn = cursor.execute("""SELECT rand FROM users WHERE user_id=(?)""", [call.message.chat.id]).fetchall()[0][0]
#     id = data[rn][0]
#     dislike = data[rn][9]
#     print(id)
#     cursor.execute("""UPDATE channel SET dislike=(?) WHERE id=(?)""", [int(dislike)+1, id])
#
#     connect.commit()
#     cursor.close()
#     connect.close()
#
#     await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
#
#     await make_post(call)
#
# @dp.callback_query_handler(cb.filter(action='ads'))
# async def ads_post(call: CallbackQuery):
#     await call.answer(cache_time=None)
#     connect = sqlite3.connect('DiscoveryDB.db')
#     cursor = connect.cursor()
#     cursor.execute("""SELECT * FROM channel""")
#     data = cursor.fetchall()
#     cursor.close()
#     cursor = connect.cursor()
#     rn = cursor.execute("""SELECT rand FROM users WHERE user_id=(?)""", [call.message.chat.id]).fetchall()[0][0]
#     id = data[rn][0]
#     ads = data[rn][4]
#
#     cursor.execute("""UPDATE channel SET ads=(?) WHERE id=(?)""", [int(ads)+1, id])
#
#     connect.commit()
#     cursor.close()
#     connect.close()
#
#     await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
#
#     await make_post(call)
#
# @dp.message_handler(Command('update'))
# async def update(message: Message):
#     connect = sqlite3.connect('DiscoveryDB.db')
#     cursor = connect.cursor()
#     cursor.execute('SELECT interests FROM users WHERE user_id=(?)', [message.chat.id])
#     data = cursor.fetchall()
#     interests = data[0][0]
#     choosed = {
#         '0': 'Программирование',
#         '1': 'Путешествие',
#         '2': 'Новости и СМИ',
#         '3': 'Маркетинг и реклама',
#         '4': 'Технологии',
#         '5': 'Юмор и развлечения',
#         '6': 'Блоги',
#         '7': 'Бизнес и стартапы',
#         '8': 'Криптовалюты',
#         '9': 'Экономика и финансы'
#     }
#
#     a = [choosed[i] for i in interests if i in '1234567890']
#     # ['it', 'travels', 'news', 'marketing', 'tech', 'entertainment', 'blogs', 'business', 'crypto', 'economics']
#     await bot.send_poll(chat_id=message.chat.id,
#                         question=f'Решил изменить предпочтения❓\nСейчас у тебя выбрано: \n{[i for i in a]}',
#                         options=['Программирование 💻',  # 0
#                                  'Путешествие 🏖',  # 1
#                                  'Новости и СМИ 📰',  # 2
#                                  'Маркетинг и реклама 📈',  # 3
#                                  'Технологии ⌚️',  # 4
#                                  'Юмор и развлечения 😂',  # 5
#                                  'Блоги 📹',  # 6
#                                  'Бизнес и стартапы 💰',  # 7
#                                  'Криптовалюты 🔐',  # 8
#                                  'Экономика и финансы 💵'],  # 9
#                         is_anonymous=False,
#                         allows_multiple_answers=True)
#
async def make_post(call: CallbackQuery):
    import mysql.connector
    connect = mysql.connector.connect(user=DBConfig.user,
                                      password=DBConfig.password,
                                      host=DBConfig.host,
                                      port=DBConfig.port,
                                      database=DBConfig.database)
    cursor = connect.cursor()
    cursor.execute("""SELECT post_id FROM posts""")
    data = cursor.fetchall()
    ids = [i[0] for i in data]
    rand_post_id = choice(ids)
    cursor.execute("""SELECT * FROM posts WHERE post_id=(%s)""", [rand_post_id])
    post_data = cursor.fetchall()
    type_of_post = post_data[0][1]

    if type_of_post == 'text':
        await bot.send_message(call.message.chat.id, post_data[0][3], reply_markup=react_keyboard)

    if type_of_post == 'photo':
        if post_data[0][11] is None:
            print(post_data[0][6])
            await bot.send_photo(chat_id=call.message.chat.id,
                                 photo='AgACAgIAAxkBAAOPY30VWOVrS3YGtoKS4mS3cWsC8pkAAsXBMRvgSOlLsQMgRZfaZ_0BAAMCAANzAAMrBA',
                                 caption=post_data[0][3],
                                 reply_markup=react_keyboard)
        else:
            username = post_data[0][5]
            media_group_id = post_data[0][11]
            cursor.execute("""SELECT * FROM posts WHERE username=(%s) AND media_group_id=(%s)""",
                           [username, media_group_id])
            group_data = cursor.fetchall()
        # print(group_data)

            print([i[6] for i in group_data])

        # mg = MediaGroup([InputMedia(i[6]) for i in group_data])
        # await bot.send_media_group(call.message.chat.id, mg)

    if type_of_post == 'document':
        username = post_data[0][5]
        media_group_id = post_data[0][11]
        cursor.execute("""SELECT * FROM posts WHERE username=(%s) AND media_group_id=(%s)""",
                       [username, media_group_id])

    if type_of_post == 'web_page':
        pass

    # interests = cursor.execute("""SELECT interests FROM users WHERE user_id=(?)""", [call.message.chat.id]).fetchall()
    # interests = interests[0][0]
    # interests = [int(i) for i in interests if i in '123456789']  # то, что хочет пользователь

    # data = cursor.execute("""SELECT * FROM channel""").fetchall()
    # cursor.close()
    #
    # new_data = []
    # for i in data:
    #     if (i[-2]) in interests:
    #         new_data.append(i)
    #
    # ids = []
    # for i in new_data:
    #     ids.append(i[0])
    #
    # rn = choice(ids)
    # id_rn = rn
    # cursor = connect.cursor()
    # reacts = cursor.execute("""SELECT like, dislike FROM channel WHERE id=(?)""", [id_rn]).fetchall()
    # cursor.close()
    # rn = ids.index(rn)
    # likes = reacts[0][0]
    # dislikes = reacts[0][1]
    # if new_data[rn][3] == 'photo':
    #     photo = new_data[rn][2]
    #     caption = new_data[rn][6]
    #     caption_entities = new_data[rn][-1]
    #     caption_entities = caption_entities.replace(" ", "")
    #     caption_entities = caption_entities.replace("\n", "")
    #     caption_entities = json.loads(caption_entities)
    #
    #     await bot.send_photo(chat_id=call.message.chat.id,
    #                          photo=photo,
    #                          caption=caption+f"\n\n\n❤️:{likes}                 👎:{dislikes}",
    #                          caption_entities=caption_entities,
    #                          reply_markup=react_keyboard,
    #                          parse_mode='HTML')
    #
    # if new_data[rn][3] == 'text':
    #     text = str(new_data[rn][6])
    #
    #     await bot.send_message(chat_id=call.message.chat.id,
    #                            text=text+f"\n\n\n❤️:{likes}                 👎:{dislikes}",
    #                            reply_markup=react_keyboard,
    #                            disable_web_page_preview=True,
    #                            parse_mode='Markdown')
    #
    # if new_data[rn][3] == 'web_page':
    #     text = str(new_data[rn][6])
    #
    #     await bot.send_message(chat_id=call.message.chat.id,
    #                            text=text+f"\n\n\n❤️:{likes}                 👎:{dislikes}",
    #                            reply_markup=react_keyboard,
    #                            parse_mode='Markdown')
    #
    # cursor = connect.cursor()
    # cursor.execute("""UPDATE users SET rand=(?) WHERE user_id=(?)""", [rn, call.message.chat.id])
    # connect.commit()
    # cursor.close()

