import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging
from culture_info_slack import CultureInfoSlack

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]


app = App(token=SLACK_BOT_TOKEN)
logging.basicConfig(level=logging.DEBUG)

cultureInfo = CultureInfoSlack(app)

if __name__ == "__main__":
    logging.info("Starting app")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
