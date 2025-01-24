from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
import httpx

from bot.states import ProductState
# from bot.keyboards import get_product_keyboard
from bot.config import config
import bot.keyboards as kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.reply(
        "Добро пожаловать! Нажмите кнопку ниже, чтобы получить данные по товару.",
        reply_markup=kb.main,
    )


@router.message(F.text == "Получить данные по товару")
async def handle_get_product(message: Message, state: FSMContext):
    await message.answer("Введите артикул товара.")
    await state.set_state(ProductState.waiting_for_artikul)


@router.message(ProductState.waiting_for_artikul)
async def handle_artikul_input(message: Message, state: FSMContext):
    artikul = message.text.strip()

    if not artikul.isdigit():
        await message.answer("Пожалуйста, введите корректный артикул (только цифры).")
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{config.API_URL}/api/v1/products/{artikul}")

    if response.status_code == 200:
        product = response.json()
        await message.answer(
            f"**Название:** {product['name']}\n"
            f"**Цена:** {product['price']} руб.\n"
            f"**Рейтинг:** {product['rating']}\n"
            f"**Остаток на складах:** {product['stock_quantity']} шт.",
            parse_mode="Markdown",
        )
    elif response.status_code == 404:
        await message.answer(f"Товар с артикулом {artikul} не найден.")
    else:
        await message.answer("Ошибка при получении данных. Попробуйте позже.")

    await message.answer(
        "Если хотите ввести другой артикул, нажмите кнопку ниже.",
        reply_markup=kb.main,
    )

    await state.clear()
