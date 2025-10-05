from discord_webhook import DiscordWebhook
import logging

class DiscordNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_alert(self, message):
        webhook = DiscordWebhook(url=self.webhook_url, content=message)
        webhook.execute()
        logging.info("Discord alert sent.")
