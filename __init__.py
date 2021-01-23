from subprocess import call
import paho.mqtt.client as mqtt
from mycroft import MycroftSkill
from .util import wrap_text


class SwagBadge(MycroftSkill):
    """Provide interaction between Mycroft and a Swag Badge.

    For more details on the Swag Badge from LinuxConfAu 2021 see:
    http://www.openhardwareconf.org/wiki/Swagbadge2021
    """

    def __init__(self):
        MycroftSkill.__init__(self)
        self.LINE_LENGTH = 31
        self.mqttc = None

    def initialize(self):
        self.add_event("speak", self.send_text_block)
        self.mqttc = mqtt.Client()

    def send_text_block(self, message):
        text = message.data["utterance"]
        lines = wrap_text(text, self.LINE_LENGTH)
        for line in lines:
            self.log_to_oled(line)

    def log_to_oled(self, text):
        mqtt_host = self.settings.get("mqtt_host")
        badge_id = self.settings.get("badge_id")
        topic = f"public/{badge_id}/0/in"
        payload = f"(oled:log {text})"
        if mqtt_host and badge_id:
            self.mqttc.connect(mqtt_host)
            self.mqttc.publish(topic, payload)
            self.mqttc.disconnect()
        else:
            self.log.info("Could not publish speech to Swag Badge")
            self.log.info("Please check your Skill settings at https://home.mycroft.ai")

    def shutdown(self):
        self.mqttc.disconnect()


def create_skill():
    return SwagBadge()
