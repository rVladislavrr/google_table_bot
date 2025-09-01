from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.config import botSettings
from bot.logger import setup_logging
from bot.schemas import BrokerMsgBot, UserBot
from bot.utils.keybB import main_kb, ready_kb, cancel_kb
from bot.utils.req import verify_google_sheet_access, ServerHTTPError, fetch_delete_to_config
from bot.utils.users import get_user_config


class ConfigStates(StatesGroup):
    id_table = State()
    check_access = State()


log = setup_logging('Обычные команды')

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    log.info("Command: start")
    await message.answer(
        "Бот по записыванию информаций о расходах в гугл таблицах",
        reply_markup=main_kb(),
        parse_mode="HTML"
    )


async def show_current_config(message: types.Message, config: dict):
    table_id = config.get("table_id")

    await message.answer(
        "📋 Текущая конфигурация:\n\n"
        f"🔗 Таблица: <code>{table_id}</code>\n"
        "Данные актуальны на момент последней проверки.\n"
        "Если нужно изменить, введите команду /reconfig ",
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(Command("reconfig"))
async def reconfig_cmd(message: types.Message, state: FSMContext):
    log.info("Command: reconfig")
    status_code = await fetch_delete_to_config(message.chat.id)
    if status_code == 200 or status_code == 404:
        await state.set_state(ConfigStates.id_table)
        await message.answer("Шаг 1: Укажите ID Google Таблицы:", reply_markup=cancel_kb())

@router.message(Command("config"))
async def config_cmd(message: types.Message, state: FSMContext):
    log.info("Command: config")
    user_config = await get_user_config(message.from_user.id)
    if user_config:
        log.info('Отображение полученного конфига')
        await show_current_config(message, user_config)
        return
    await state.set_state(ConfigStates.id_table)
    await message.answer("Шаг 1: Укажите ID Google Таблицы:", reply_markup=cancel_kb())


@router.message(
    ConfigStates.id_table,
    ~F.text.startswith('/'),
    ~F.text.in_(["❌ Отмена"])
)
async def process_table_id(message: types.Message, state: FSMContext):
    table_id = message.text.strip()
    await state.update_data(id_table=table_id)

    await state.set_state(ConfigStates.check_access)
    await message.answer(
        f"🔗 Таблица: <code>{table_id}</code>\n\n"
        f"🔐 Пожалуйста, предоставьте доступ к таблице для бота (email: <code>{botSettings.EMAIL}</code>), "
        "а затем нажмите <b>✅ Готово</b>.",
        reply_markup=ready_kb(),
        parse_mode="HTML"
    )


@router.message(ConfigStates.check_access, F.text == "✅ Готово")
async def check_table_access(message: types.Message, state: FSMContext):
    log.info("start verify")
    chat_id = message.chat.id
    user_msg_id = message.message_id
    table_id = (await state.get_data()).get("id_table")

    user_data = UserBot(
        username=message.from_user.username,
        chat_id=chat_id,
        msg_id=user_msg_id,
    )
    await state.clear()
    bot_msg = (await message.answer("Ожидайте подтверждения",
                                    reply_markup=main_kb(),
                                    reply_to_message_id=user_msg_id))
    bot_msg_id = bot_msg.message_id

    broker_msg = BrokerMsgBot(
        bot_msg_id=bot_msg_id,
        user=user_data,
        table_id=table_id
    )
    try:
        await verify_google_sheet_access(broker_msg)
    except ServerHTTPError as e:
        await bot_msg.delete()
        await message.answer(
            "Какая то ошибка в обработке, повторите попытку позже, сервер не принял запрос",
            reply_markup=main_kb(),
            reply_to_message_id=user_msg_id)
    except:
        await bot_msg.delete()
        await message.answer(
            "Какая то ошибка в обработке, повторите попытку позже",
            reply_markup=main_kb(),
            reply_to_message_id=user_msg_id)

    log.info("end verify")


@router.message(F.text == "❌ Отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.clear()
        await message.answer(
            "✅ Конфигурация отменена",
            reply_markup=main_kb()
        )
    else:
        await message.answer("ℹ️ Нет активной конфигурации для отмены", reply_markup=main_kb())
