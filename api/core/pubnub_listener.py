import json
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from .config import config
from .logger import logger
from .redis import timestamp_list, heart_list, sweat_list
from .db import bio_data


pnconfig = PNConfiguration()
pnconfig.subscribe_key = config.get("SUB_KEY")
pnconfig.publish_key = config.get("PUB_KEY")
pnconfig.user_id = config.get("UID")
pubnub = PubNub(pnconfig)


class MySubscribeCallback(SubscribeCallback):
    def __init__(self) -> None:
        super().__init__()
        self.listener_state = None
        self.review_id = None
        self.machine_id = None

    def presence(self, pubnub, event):
        action = event.event  # join, leave, timeout, state-change, interval
        channel = event.channel
        occupancy = event.occupancy
        logger("PubNub").info(f"action={action}|channel={channel}|occupancy={occupancy}")

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            logger("PubNub").error("Unexpected Disconnection")
        elif status.category == PNStatusCategory.PNConnectedCategory:
            logger("PubNub").info("Connected to PubNub")
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            logger("PubNub").warn("Reconnecting to PubNub")

    def message(self, pubnub, message):
        print(message.message)
        if type(message.message) == "start":
            self.listener_state = "STARTED"
            logger("PubNub").info("***************START****************")
        elif message.message == "pause":
            self.listener_state = "PAUSED"
            logger("PubNub").info("***************PAUSE****************")
        elif message.message == "resume":
            self.listener_state = "RESUMED"
            logger("PubNub").info("***************RESUME****************")
        elif message.message == "stop":
            self.listener_state = "STOPPED"
            logger("PubNub").info("***************STOP****************")

        if self.listener_state == "STARTED" or self.listener_state == "RESUMED":
            bio_object = json.loads(message.message)

            self.review_id = bio_object[0]["biodata"][0]
            self.machine_id = bio_object[0]["biodata"][1]
            heart_rate = bio_object[0]["biodata"][2]
            sweat_rate = bio_object[0]["biodata"][3]
            timestamp = bio_object[0]["biodata"][4]

            heart_list.lpush(f"{self.review_id}:{self.machine_id}", heart_rate)
            sweat_list.lpush(f"{self.review_id}:{self.machine_id}", sweat_rate)
            timestamp_list.lpush(f"{self.review_id}:{self.machine_id}", timestamp)
        elif self.listener_state == "PAUSED":
            pass
        elif self.listener_state == "STOP":
            new_biodata = {
                "review_id": self.review_id,
                "machine_id": self.machine_id,
                "heart_rate": heart_list.lrange(f"{self.review_id}:{self.machine_id}", 0, -1),
                "sweat": sweat_list.lrange(f"{self.review_id}:{self.machine_id}", 0, -1),
                "timestamp": timestamp_list.lrange(f"{self.review_id}:{self.machine_id}", 0, -1),
                "average_sweat": 0,
                "average_heart_rate": 0
            }
            print("ABOUT TO SEND DATA")
            print(new_biodata)
            bio_data.insert_one(new_biodata)
