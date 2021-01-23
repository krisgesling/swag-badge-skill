from subprocess import call
from mycroft import MycroftSkill


class SwagBadge(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.LINE_LENGTH = 31

    def initialize(self):
        self.add_event("speak", self.send_text_block)

    def send_text_block(self, message):
        text = message.data["utterance"]
        lines = wrap_text(text, self.LINE_LENGTH)
        for line in lines:
            self.log_to_oled(line)

    def log_to_oled(self, text):
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
            f"(oled:log {text})",
        ]
        if mqtt_host and badge_id:
            call(cmd)
        else:
            self.log.info("Could not publish speech to Swag Badge")
            self.log.info("Please check your Skill settings at https://home.mycroft.ai")


def create_skill():
    return SwagBadge()


def wrap_text(text, line_length):
    """Wrap a string of text based on the given line length.

    Words that are longer than the line length will be split with a dash.

    Arguments:
        text (Str): the text that will be wrapped
        line_length (Int): the max length of a line
    Returns:
        List [Str]
    """
    words = text.split()
    lines = []
    while len(words) > 0:
        line = ""
        while len(line) < line_length and len(words) > 0:
            characters_left = line_length - len(line)
            if characters_left >= len(words[0]):
                word = words.pop(0)
            else:
                if len(line) == 0:
                    # Word is too long for line, split word across lines
                    length = line_length - 1  # Give room for the dash
                    word, words[0] = (words[0][:length], words[0][length:])
                    word += "-"
                else:
                    break
            line = " ".join((line, word)).strip()
        lines.append(line)
    return lines
