import threading
from core.pubnub_listener import pubnub, MySubscribeCallback
from core.config import config
from main import app

my_channel = config.get("CHANNEL")

if __name__ == "__main__":
    moviology_thread = threading.Thread()
    moviology_thread.start()
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(my_channel).execute()
    app.run(port=5000)
