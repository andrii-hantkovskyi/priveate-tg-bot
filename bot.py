import asyncio
import datetime
import logging

import aioschedule
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import CantRestrictChatOwner, BadRequest

from services.db import add_user_to_db, get_all_subscribers_id, check_if_user_registered, get_expire_date
from services.process import add_months_to_subscription, check_for_subscription, get_last_minute_statements, \
    check_for_access
from services.tg import remind_for_channel, generate_five_minutes_request_invite_link, \
    remind_for_subscription_expiration
from settings import API_TOKEN, CHANNEL_ID, MONO_JAR_URL

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    return await message.reply(
        "Привіііітик! Я бот, котрий видає підписку на приватний канал)))0)\n"
        "Пиши /register, щоб зареєструватися :*"
    )


@dp.message_handler(commands=['register'])
async def register_subscriber(message: types.Message):
    is_registered = check_if_user_registered(message.from_user.id)

    if is_registered:
        return await message.reply("Куда, ти вже зареєстрований, пам'ять відшибло?!")
    add_user_to_db(message.from_user.id)
    return await message.reply("Вас успішно зареєстровано)")


@dp.message_handler(commands=['buy_pass'])
async def user_buy_pass(message: types.Message):
    is_registered = check_if_user_registered(message.from_user.id)
    if is_registered:
        await message.answer(
            f"{MONO_JAR_URL[:-1] if MONO_JAR_URL.endswith('/') else MONO_JAR_URL}/?t={message.from_user.id}\n")
        return await message.answer(
            "в цю банку кидаєш гроші по формулі:\n"
            "1 місяць підписки = 100 гривень\n"
            "бот сам розділить суму і видасть прохід на n-ну к-сть місяців :)\n"
            "Запрошення прийде протягом 2хв після оплати"
            "\n\n"
            "УВАГА!!! не чіпайте коментар, то код! без нього лишишся без проходу)))\n\n")
    else:
        return await message.reply("ти може зареєструєшся спочатку?! мм??!! /register")


@dp.chat_join_request_handler()
async def user_joined(chat_member: types.ChatJoinRequest):
    has_access_to_join = check_for_access(chat_member.from_user.id)
    if not has_access_to_join:
        await chat_member.decline()
        return await bot.send_message(chat_member.from_user.id,
                                      "хочеш в приватний канал?)) тоді купи доступ, /buy_pass")
    return await chat_member.approve()


async def check_subscribers():
    users_id = get_all_subscribers_id()
    for user_id in users_id:
        subscribed, expire_date = check_for_subscription(user_id)
        if not subscribed:
            try:
                await bot.ban_chat_member(CHANNEL_ID, user_id)
            except CantRestrictChatOwner:
                pass
        else:
            try:
                user = await bot.get_chat_member(CHANNEL_ID, user_id)
                if user.status in ('left', 'kicked'):
                    await bot.unban_chat_member(CHANNEL_ID, user_id)
                    await remind_for_channel(bot, user_id, expire_date, CHANNEL_ID)
            except BadRequest:
                await remind_for_channel(bot, user_id, expire_date, CHANNEL_ID)


async def check_statements():
    statements = get_last_minute_statements()
    for statement in statements:
        add_months_to_subscription(
            int(statement['comment']), int(statement['amount'] / 1000))
        invite_link = await generate_five_minutes_request_invite_link(bot, CHANNEL_ID)
        await bot.send_message(int(statement['comment']),
                               f"Оплата пройшла успішно, на тобі посилання: {invite_link}\n"
                               f"але дій швидко, посилання діє всього 5хв))")


async def check_for_subscription_expiration():
    subscribers = get_all_subscribers_id()
    for subscriber in subscribers:
        exp_date = get_expire_date(subscriber)
        if (datetime.date.today() - exp_date).days < 7:
            await remind_for_subscription_expiration(bot, user_id=subscriber)


async def scheduler():
    aioschedule.every().hour.do(check_subscribers)
    aioschedule.every().minute.do(check_statements)
    aioschedule.every().day.do(check_for_subscription_expiration)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
