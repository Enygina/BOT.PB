import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from googletrans import Translator
import requests
import extract
import recoding
import keyboards as kb
import logger
from app import dp, bot
from config import chat_id

class PersonInfo(StatesGroup):
    surname = State()
    name = State()
    t_num = State()
    info = State()
    sur_for_fnd = State()


class City(StatesGroup):
    city = State()


translator = Translator()


# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Вертуальный помошник приветсвует тебя\nНачнем! Вот что я могу:", reply_markup=kb.keybd)

# вызов клавиатуры телефонного справочника
@dp.callback_query_handler(lambda c: c.data == "1")
async def callback(call):
    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=kb.keyboard)

# выход в главное меню
@dp.callback_query_handler(lambda c: c.data == "7")
async def callback(call):
    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=kb.keybd)


# Нажатие кнопки ввода данных, введение фамилии
@dp.callback_query_handler(lambda c: c.data == '4')
async def person_reg(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Введите фамилию")
    await PersonInfo.surname.set()


# введение имени
@dp.message_handler(state=PersonInfo.surname)
async def get_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text.replace(" ", '').title())
    await message.answer("Отлично! Теперь введите имя.")
    await PersonInfo.name.set()


# введение телефона
@dp.message_handler(state=PersonInfo.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.replace(" ", '').title())
    await message.answer("Номер телефона")
    await PersonInfo.t_num.set()


# введение информации
@dp.message_handler(state=PersonInfo.t_num)
async def get_t_num(message: types.Message, state: FSMContext):
    await state.update_data(t_num=message.text.replace(" ", '').title())
    await message.answer("И информацию")
    await PersonInfo.info.set()


# логирование, запись в csv, вывод пользователю
@dp.message_handler(state=PersonInfo.info)
async def get_info(message: types.Message, state: FSMContext):
    await state.update_data(info=message.text.replace(" ", '').title())
    data = await state.get_data()
    logger.log_data(data)
    await asyncio.sleep(1)
    await message.answer(f"Готово\n\nФамилия: {data['surname']}\n"
                         f"Имя: {data['name']}\n"
                         f"Телефон: {data['t_num']}\n"
                         f"Информация: {data['info']}", reply_markup=kb.keybd)
    field_names = ['surname', 'name', 't_num', 'info']
    recoding.rec_csv(data, field_names)
    await state.reset_state(with_data=False)


# нажатие кнопки полиска
@dp.callback_query_handler(lambda c: c.data == '5')
async def fnd_srname(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Введите фамилию")
    await PersonInfo.sur_for_fnd.set()


@dp.message_handler(state=PersonInfo.sur_for_fnd)
async def fnd_surname(message: types.Message, state: FSMContext):
    await state.update_data(sur_for_fnd=message.text.replace(" ", '').title())
    res = await state.get_data()
    await message.answer(f"Ищем данные по фамилии\n\n{res['sur_for_fnd']}")
    field_names = ['sur_for_fnd']
    recoding.for_fnd(res, field_names)
    await state.reset_state(with_data=False)
    a = 'for_find.csv'
    search = recoding.for_beauty(recoding.output_csv(a))
    b = 'Names.csv'
    data = recoding.for_beauty(recoding.output_csv(b))
    search_res = extract.empty_fnd(extract.fnd_lastname(data, search))
    if search_res != -1:
        for x in search_res:
            await asyncio.sleep(1)
            await message.answer(f'Фамилия: {x[0]}\nИмя: {x[1]}\nТелефон: {x[2]}\nОписание: {x[3]}')
    else:
        await message.answer(f'Такого контакта у меня нет')
    await asyncio.sleep(2)
    await message.answer(f'Чем еще могу помочь?', reply_markup=kb.keybd)


# печать всех данных
@dp.callback_query_handler(lambda c: c.data == '6')
async def output_all(call: types.CallbackQuery):
    b = 'Names.csv'
    data = recoding.for_beauty(recoding.output_csv(b))
    for x in data:
        await call.message.answer(f'Фамилия: {x[0]}\nИмя: {x[1]}\nТелефон: {x[2]}\nОписание: {x[3]}')
    await asyncio.sleep(2)
    await call.message.answer(f'Чем еще могу помочь?', reply_markup=kb.keybd)


@dp.callback_query_handler(lambda c: c.data == '2')
async def NASA_photo(call: types.CallbackQuery):
    r = requests.get("https://api.nasa.gov/planetary/apod?api_key=rN9UYok6YKqF7YpwbJJx8fnZnJwguxpGJwblLexG")
    json_r = r.json()
    for key in json_r:
        if key == "hdurl":
            a = str(json_r[key])
        if key == "explanation":
            b = translator.translate(str(json_r[key]), dest='ru')
            print(b)
    await bot.send_photo(chat_id=chat_id, photo=a)
    await call.message.answer(f'А это интересно:\n \n{b.text}')
    await asyncio.sleep(5)
    await call.message.answer(f'Чем еще могу помочь?', reply_markup=kb.keybd)

# город для погоды
@dp.callback_query_handler(lambda c: c.data == '3')
async def city(call: types.CallbackQuery):
    await call.message.edit_text("Введите город")
    await City.city.set()

# вывод погоды по городу
@dp.message_handler(state=City.city)
async def get_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text.replace(" ", ''))
    data = await state.get_data()
    for key in data:
        c = str(data[key]) #город, полученный от пользователя
    code_to_photo = {
        "Clear": "Ясно",
        "Clouds": "Облачно",
        "Rain": "Дождь",
        "Drizzle": "Небольшой дождь",
        "Thunderstorm": "Гроза",
        "Snow": "Снег",
        "Mist": "Туман"}
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={c}&appid=5ad7b8fca6310aff7d3bdd2d7d6a2631&units=metric")
        json_r = r.json()
        weather_description = json_r["weather"][0]["main"]#состояние погоды для вывода кортинки
        if weather_description in code_to_photo:
            wb=code_to_photo[weather_description]
        else:
            wb="Посмотри в окно, не пойму, что там за погода"
        await bot.send_photo(chat_id=chat_id, photo=recoding.foto_weather(weather_description))
        await message.answer(f'{wb}\n'
                             f'За окном: {json_r["main"]["temp"]} °C \n'
                             f'Ощущается как: {json_r["main"]["feels_like"]}\n'
                             f'Облачность: {json_r["clouds"]["all"]} % \n'
                             f'Скорость ветра: {json_r["wind"]["speed"]} м/сек.\n')
        await asyncio.sleep(2)
        await message.answer(f'Чем еще могу помочь?', reply_markup=kb.keybd)
    except Exception:
        await message.reply(f'Что-то с городом не так?', reply_markup=kb.keybd)
    await state.reset_state(with_data=False)

__all__ = ['dp']
