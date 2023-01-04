from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import extract
import recoding
import keyboards as kb
import logger
from app import dp


class PersonInfo(StatesGroup):
    surname = State()
    name = State()
    t_num = State()
    info = State()
    sur_for_fnd = State()


# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Телефонный справочник приветсвует тебя\nНачнем! Вот что я могу:", reply_markup=kb.keyboard)


# Нажатие кнопки ввода данных, введение фамилии
@dp.callback_query_handler(lambda c: c.data == '1')
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
    await message.answer(f"Готово\n\nФамилия: {data['surname']}\n"
                         f"Имя: {data['name']}\n"
                         f"Телефон: {data['t_num']}\n"
                         f"Информация: {data['info']}", reply_markup=kb.keyboard)
    field_names = ['surname', 'name', 't_num', 'info']
    recoding.rec_csv(data, field_names)
    await state.reset_state(with_data=False)


# нажатие кнопки полиска
@dp.callback_query_handler(lambda c: c.data == '2')
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
            await message.answer(f'Фамилия: {x[0]}\nИмя: {x[1]}\nТелефон: {x[2]}\nОписание: {x[3]}')
    else:
        await message.answer(f'Такого контакта у меня нет')
    await message.answer(f'Чем еще могу помочь?', reply_markup=kb.keyboard)


# печать всех данных
@dp.callback_query_handler(lambda c: c.data == '3')
async def output_all(call: types.CallbackQuery):
    b = 'Names.csv'
    data = recoding.for_beauty(recoding.output_csv(b))
    for x in data:
        await call.message.answer(f'Фамилия: {x[0]}\nИмя: {x[1]}\nТелефон: {x[2]}\nОписание: {x[3]}')
    await call.message.answer(f'Чем еще могу помочь?', reply_markup=kb.keyboard)
