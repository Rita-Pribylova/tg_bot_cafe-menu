import json
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_CHAT_ID

router = Router()


class OrderState(StatesGroup):
    waiting_for_address = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()

    YOUR_WEBAPP_URL = "https://rita-pribylova.github.io/tg_bot_cafe-menu/frontend/?v=3"

    builder.button(text="📖 Открыть меню кафе", web_app=WebAppInfo(url=YOUR_WEBAPP_URL))

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        f"Добро пожаловать в наше кафе. Нажмите на кнопку ниже, чтобы открыть интерактивное меню с картинками и выбрать блюда!",
        reply_markup=builder.as_markup(),
    )


@router.message(F.web_app_data)
async def process_webapp_data(message: Message, state: FSMContext):

    cart_data = json.loads(message.web_app_data.data)

    if not cart_data:
        await message.answer("Ваша корзина пуста. Пожалуйста, выберите товары в меню.")
        return

    order_items = []
    total_price = 0
    for item in cart_data:
        order_items.append(f"• <b>{item['name']}</b> — {item['price']}₽")
        total_price += item["price"]

    await state.update_data(
        item_name=", ".join([item["name"] for item in cart_data]),
        item_price=total_price,
    )

    items_text = "\n".join(order_items)

    response_text = (
        f"<b>🛒 Ваш заказ сформирован:</b>\n\n"
        f"{items_text}\n\n"
        f"💰 <b>Итого к оплате:</b> <code>{total_price}₽</code>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"Пожалуйста, напишите адрес доставки (город, улица, дом, квартира) для завершения оформления 👇"
    )

    await message.answer(response_text, parse_mode="HTML")

    await state.set_state(OrderState.waiting_for_address)


@router.message(OrderState.waiting_for_address)
async def process_address(message: Message, state: FSMContext, bot: Bot):
    address = message.text
    user_data = await state.get_data()

    item_name = user_data["item_name"]
    item_price = user_data["item_price"]

    await message.answer(
        f"<b>🎉 Заказ успешно принят!</b>\n\n"
        f"🛍 <b>Вы заказали:</b> {item_name}\n"
        f"💰 <b>Сумма к оплате курьеру:</b> <code>{item_price}₽</code>\n\n"
        f"<i>Наш менеджер уже связывается с вами для подтверждения. Спасибо, что выбрали нас!</i>",
        parse_mode="HTML",
    )

    admin_text = (
        f"🔔 <b>НОВЫЙ ЗАКАЗ ИЗ MINI APP!</b>\n\n"
        f"👤 <b>Клиент:</b> {message.from_user.full_name} (@{message.from_user.username})\n"
        f"🛍 <b>Состав заказа:</b> {item_name}\n"
        f"💰 <b>Сумма:</b> {item_price}₽\n"
        f"📍 <b>Адрес доставки:</b> <code>{address}</code>"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text, parse_mode="HTML")
    await state.clear()
