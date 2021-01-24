import os
from subprocess import call
from mycroft import MycroftSkill
from .badge import MQTT_Client
from .util import wrap_text


class SwagBadge(MycroftSkill):
    """Provide interaction between Mycroft and a Swag Badge.

    For more details on the Swag Badge from LinuxConfAu 2021 see:
    http://www.openhardwareconf.org/wiki/Swagbadge2021
    """

    def __init__(self):
        MycroftSkill.__init__(self)
        self.LINE_LENGTH = 32
        self.NUM_SCREENS = 2
        self.mqttc = None

    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()
        self.add_event("speak", self.send_text_block)
        self.display_image()

    def on_settings_changed(self):
        host = self.settings.get("mqtt_host")
        if host:
            if self.mqttc:
                self.mqttc.disconnect()
            self.mqttc = MQTT_Client(host)

        badge_id = self.settings.get("badge_id")
        if badge_id:
            self.mqttc.set_topic(f"public/{badge_id}/0/in")

    def send_text_block(self, message):
        """Send utterance to Badge.

        Splits text based on line length and prevents words being split
        between the two screens.

        Arguments:
            message (Message): standard Mycroft Message object
        """
        text = message.data.get("utterance")
        if not text:
            return
        chars = int(self.LINE_LENGTH / self.NUM_SCREENS)
        lines_per_screen = wrap_text(text, chars)
        # Add spaces to log correctly across multiple screens.
        padded_lines = [f"{l: <{chars}}" for l in lines_per_screen]
        lines = [
            x + y
            for x, y in zip(
                padded_lines[0 :: self.NUM_SCREENS], padded_lines[1 :: self.NUM_SCREENS]
            )
        ]
        for line in lines:
            success, msg = self.mqttc.log_to_oled(line)
            if not success:
                self.log.error(msg)
                break
    
    def display_image(self, image="m32.png"):
        """Display an image on the Badge screen."""
        image_path = os.path.join(self.root_dir, "images", image)
        self.mqttc.render_image(image_path)

    def shutdown(self):
        self.mqttc.disconnect()


def create_skill():
    return SwagBadge()
