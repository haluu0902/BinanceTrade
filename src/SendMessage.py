import telepot

class SendMessageTelegram:
    def __init__(self):
        token = '5631591222:AAEpGSfqDaBzmzMoLMKtFgJ7IJHav_4cdLs' # telegram token
        #self.receiver_id = 1846504253 # https://api.telegram.org/bot<TOKEN>/getUpdates
        #1846504253

        #530396422 Vu

        self.bot = telepot.Bot(token)

    def SendMessage(self, id, message):
        self.bot.sendMessage(id, message) # send a activation message to telegram receiver id