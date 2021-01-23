from subprocess import call, Popen
from mycroft import MycroftSkill, intent_file_handler


class SwagBadge(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.add_event('speak', self.log_to_badge)

    def log_to_badge(self, message):
        speech = message.data['utterance']
        mqtt_host = self.settings.get("mqtt_host")
        badge_id = self.settings.get("badge_id")
        mqtt_topic = f"public/{badge_id}/0/in"
        cmd = [
               "mosquitto_pub",
               "-h",
               mqtt_host,
               "-t",
               mqtt_topic,
               "-m",
               f"(oled:log {speech})"
        ]
        if mqtt_host and badge_id:
            call(cmd)
        else:
            self.log.info("Could not publish speech to Swag Badge")
            self.log.info("Please check your Skill settings at https://home.mycroft.ai")


def create_skill():
    return SwagBadge()

