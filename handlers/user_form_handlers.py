from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

from keyboards.keyboards import create_inline_kb

router = Router()


# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, int]] = {}


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_age = State()
    fill_gender = State()
    fill_weight = State()
    fill_height = State()


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    reply_markup = create_inline_kb(1, 'btn_user_form')
    await message.answer(
        text='Отменять нечего.',
        reply_markup=reply_markup,
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    reply_markup = create_inline_kb(1, 'btn_user_form')
    await message.answer(
        text='Вы прервали заполнение анкеты',
        reply_markup=reply_markup,
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду /fillform
# и переводить бота в состояние ожидания ввода имени
@router.callback_query(F.data == "btn_user_form", StateFilter(default_state))
async def process_fillform_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пожалуйста, введите ваше имя')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш возраст')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_age)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на имя\n\n'
             'Пожалуйста, введите ваше имя\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать, если введен корректный возраст
# и переводить в состояние выбора пола
@router.message(StateFilter(FSMFillForm.fill_age),
                lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "age"
    await state.update_data(age=message.text)
    # Создаем объекты инлайн-кнопок
    reply_markup = create_inline_kb(2, male='Мужской ♂', female='Женский ♀')
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Спасибо!\n\nУкажите ваш пол',
        reply_markup=reply_markup
    )
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_gender)


# Этот хэндлер будет срабатывать, если во время ввода возраста
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_age))
async def warning_not_age(message: Message):
    await message.answer(
        text='Возраст должен быть целым числом от 4 до 120\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать на нажатие кнопки при
# выборе пола и переводить в состояние отправки фото
@router.callback_query(StateFilter(FSMFillForm.fill_gender),
                       F.data.in_(['male', 'female']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
    # по ключу "gender"
    await state.update_data(gender=callback.data)
    # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(
        text='Спасибо! Введите вес'
    )
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(FSMFillForm.fill_weight)


# Этот хэндлер будет срабатывать, если во время выбора пола
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_gender))
async def warning_not_gender(message: Message):
    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             'при выборе пола\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel'
    )


@router.message(StateFilter(FSMFillForm.fill_weight), F.text.isdigit())
async def process_weight_sent(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer(text='Спасибо! Введите рост')
    await state.set_state(FSMFillForm.fill_height)


@router.message(StateFilter(FSMFillForm.fill_weight))
async def warning_not_weight(message: Message):
    await message.answer(
        text='Вес должен быть целым числом\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel'
    )


@router.message(StateFilter(FSMFillForm.fill_height), F.text.isdigit())
async def process_height_sent(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    print(await state.get_data())
    user_dict[message.from_user.id] = await state.get_data()
    await state.clear()
    await message.answer('Спасибо, анкета успешно сохранена!'
                         '\n\n/profile - для просмотра профиля')


# Этот хэндлер будет срабатывать на отправку команды /showdata
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@router.message(Command(commands='profile'), StateFilter(default_state))
async def process_showdata_command(message: Message):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    if message.from_user.id in user_dict:
        await message.answer(
            text=f'Имя: {user_dict[message.from_user.id]["name"]}\n'
                 f'Возраст: {user_dict[message.from_user.id]["age"]}\n'
                 f'Пол: {user_dict[message.from_user.id]["gender"]}\n'
                 f'Вес: {user_dict[message.from_user.id]["weight"]}\n'
                 f'Рост: {user_dict[message.from_user.id]["height"]}'
        )
    else:
        reply_markup = create_inline_kb(1, 'btn_user_form')
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(
            text='Вы еще не заполняли анкету. Чтобы приступить нажмите кнопку',
            reply_markup=reply_markup
        )
