from settings import settings
import requests

def telegram_post(message):
    boturl = "{}{}/sendMessage?chat_id={}&text={}".format(
        settings['telegram']['url'],
        settings['telegram']['token'],
        settings['telegram']['groupid'],
        message
    )
    r = requests.request("GET", boturl)
