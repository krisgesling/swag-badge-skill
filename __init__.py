from mycroft import MycroftSkill, intent_file_handler


class SwagBadge(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('badge.swag.intent')
    def handle_badge_swag(self, message):
        self.speak_dialog('badge.swag')


def create_skill():
    return SwagBadge()

