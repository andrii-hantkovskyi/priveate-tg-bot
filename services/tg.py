import datetime


async def generate_five_minutes_request_invite_link(bot, channel_id):
    invite_link = await bot.create_chat_invite_link(channel_id, datetime.datetime.now(
        datetime.timezone.utc) + datetime.timedelta(minutes=5), creates_join_request=True)
    return invite_link.invite_link


async def remind_for_channel(bot, user_id, expire_date, channel_id):
    invite_link = await generate_five_minutes_request_invite_link(bot, channel_id)
    await bot.send_message(user_id, f"агов, друже! у тебе є прохід у приватний тг канал аж до "
                                    f"{expire_date.strftime('%d.%m.%Y')}\n"
                                    f"на тобі посилання: {invite_link}\n"
                                    f"але дій швидко, посилання діє всього 5хв))")


async def remind_for_subscription_expiration(bot, user_id):
    await bot.send_message(user_id, 'чуваче, твоя підписка закінчиться менше, ніж за тиждень, варто поповнити ^^')
