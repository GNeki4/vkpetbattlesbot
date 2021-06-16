from vk_api.bot_longpoll import VkBotEventType
import felix_bot


bot = felix_bot.Bot()
trigger_1, trigger_2 = 'феликс', 'фл'


def check_command(spl_response, length, command):
    return len(spl_response) >= length and \
           ((spl[0] == trigger_1) or (spl[0] == trigger_2)) and spl[1] == command


while True:
    for event in bot.longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = event.message.text.lower()

            if event.from_user or event.from_chat:
                spl = response.split()

                if response == 'спокойной ночи, феликс':
                    bot.send_message(event, 'Спасибо, и тебе')

                elif check_command(spl, 2, '/usd'):
                    bot.send_currency(event, 'доллар', 'usd')

                elif check_command(spl, 2, '/eur'):
                    bot.send_currency(event, 'евро', 'eur')

                elif check_command(spl, 2, '/btc'):
                    bot.send_currency(event, 'Bitcoin', 'btc')

                elif check_command(spl, 3, '/setnick'):
                    bot.set_nickname(event)

                elif check_command(spl, 3, '/changenick'):
                    bot.change_nickname(event)

                elif check_command(spl, 2, '/mynick'):
                    bot.get_nickname(event)

                elif check_command(spl, 2, 'жмых'):
                    bot.send_distortion(event, spl)

                elif check_command(spl, 2, 'демотиватор'):
                    bot.send_demotivator(event, response)

                elif check_command(spl, 2, '/help'):
                    bot.send_help(event)
