from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database.methods import add_profile, get_profile, update_profile
from keyboards import create_inline_kb

router = Router()


# Класс состояния формы профиля пользователя
class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_age = State()
    fill_gender = State()
    fill_weight = State()
    fill_height = State()

    profile_for_change = None


# Этот хэндлер срабатывает на команду "/cancel" в любых состояниях
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    reply_markup = create_inline_kb(1, 'btn_user_form')
    await message.answer(
        text='Отменять нечего.',
        reply_markup=reply_markup,
    )


# Этот хэндлер срабатывает на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключает машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    reply_markup = create_inline_kb(1, 'btn_user_form')
    await message.answer(
        text='Вы прервали заполнение анкеты',
        reply_markup=reply_markup,
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@router.callback_query(F.data == 'btn_change_profile',
                       StateFilter(default_state))
async def change_profile(callback: CallbackQuery,
                         state: FSMContext,
                         session: AsyncSession):
    profile_for_change = await get_profile(session, callback.from_user.id)
    FSMFillForm.profile_for_change = profile_for_change
    await callback.answer()
    await callback.message.answer(text='Пожалуйста, введите ваше имя')
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер срабатывает на команду кнопку начала заполнения анкеты
# и переводит бота в состояние ожидания ввода имени
@router.callback_query(F.data == "btn_user_form", StateFilter(default_state))
async def process_fillform_command(callback: CallbackQuery,
                                   state: FSMContext,
                                   session: AsyncSession):
    # Проверяем есть ли у пользователя профиль
    user_profile = await get_profile(session, callback.from_user.id)
    if user_profile:
        reply_markup = create_inline_kb(1, 'btn_change_profile')
        await callback.message.answer(
            text='Профиль уже существует.\nЖелаете его изменить?',
            reply_markup=reply_markup)
    # Если не существует начинаем заполнение
    else:
        await callback.answer()
        await callback.message.answer(text='Пожалуйста, введите ваше имя')
        # Устанавливаем состояние ожидания ввода имени
        await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер срабатывает, если введено корректное имя
# и переводит в состояние ожидания ввода возраста
@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш возраст')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_age)


# Этот хэндлер срабатывает, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на имя\n\n'
             'Пожалуйста, введите ваше имя\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


# Этот хэндлер срабатывает, если введен корректный возраст
# и переводит в состояние выбора пола
@router.message(StateFilter(FSMFillForm.fill_age),
                lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    # Создаем объекты инлайн-кнопок
    reply_markup = create_inline_kb(2, male='Мужской ♂', female='Женский ♀')
    await message.answer(
        text='Спасибо!\n\nУкажите ваш пол',
        reply_markup=reply_markup
    )
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_gender)


# Этот хэндлер срабатывает, если во время ввода возраста
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_age))
async def warning_not_age(message: Message):
    await message.answer(
        text='Возраст должен быть целым числом от 4 до 120\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать на нажатие кнопки при
# выборе пола и переводит в состояние ожидания ввода веса
@router.callback_query(StateFilter(FSMFillForm.fill_gender),
                       F.data.in_(['male', 'female']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    # Удаляем сообщение с кнопками
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(
        text='Спасибо! Введите вес'
    )
    # Устанавливаем состояние ожидания ввода веса
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


# Этот хэндлер срабатывает, если введен корректный вес
# и переводит в состояние ввода роста
@router.message(StateFilter(FSMFillForm.fill_weight), F.text.isdigit())
async def process_weight_sent(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer(text='Спасибо! Введите рост')
    await state.set_state(FSMFillForm.fill_height)


# Этот хэндлер срабатывает, если во время ввода веса
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_weight))
async def warning_not_weight(message: Message):
    await message.answer(
        text='Вес должен быть целым числом\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel'
    )


# Этот хэндлер срабатывает, если введен корректный рост
# сохраняет информацию в бд и предлагает просмотреть профиль
@router.message(StateFilter(FSMFillForm.fill_height), F.text.isdigit())
async def process_height_sent(message: Message,
                              state: FSMContext,
                              session: AsyncSession):
    await state.update_data(height=message.text)
    # Сохраняем/обновляем информацию о профиле пользователя
    data = await state.get_data()
    if FSMFillForm.profile_for_change:
        await update_profile(session, data, message.from_user.id)
    else:
        await add_profile(session, data, message)
    await state.clear()
    await message.answer('Спасибо, анкета успешно сохранена!'
                         '\n\n/profile - для просмотра профиля')

    FSMFillForm.profile_for_change = None


@router.message(StateFilter(FSMFillForm.fill_height))
async def warning_not_height(message: Message):
    await message.answer(
        text='Рост должен быть целым числом\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать на отправку команды /profile
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@router.message(Command(commands='profile'), StateFilter(default_state))
async def process_showdata_command(message: Message, session: AsyncSession):
    user_profile = await get_profile(session, message.from_user.id)
    # Отправляем пользователю анкету, если она есть в "базе данных"
    if user_profile:
        reply_markup = create_inline_kb(1, 'btn_change_profile')
        await message.answer(
            text=f'Имя: {user_profile.name}\n'
                 f'Возраст: {user_profile.age}\n'
                 f'Пол: {user_profile.gender}\n'
                 f'Вес: {user_profile.weight}\n'
                 f'Рост: {user_profile.height}',
            reply_markup=reply_markup,
        )
    else:
        reply_markup = create_inline_kb(1, 'btn_user_form')
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(
            text='Вы еще не заполняли анкету. Чтобы приступить нажмите кнопку',
            reply_markup=reply_markup
        )
