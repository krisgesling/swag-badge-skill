import paho.mqtt.client as mqtt


class MQTT_Client:
    """A simple MQTT Client for use in Mycroft Skills.

    This is a wrapper for the Paho MQTT Client. The paho-mqtt
    package is provided under the Eclipse Public License v1.0.
    """

    def __init__(self, host, port=1883):
        self.mqttc = mqtt.Client()
        self.set_host(host)
        self.set_port(port)
        self.set_topic(None)

    def connect(self):
        """Connect to the MQTT host"""
        host = self.get_host()
        self.mqttc.connect(host)

    def disconnect(self):
        """Disconnect from the MQTT host"""
        self.mqttc.disconnect()

    def get_host(self):
        return self.__host

    def set_host(self, host):
        self.__host = host

    def get_port(self):
        return self.__port

    def set_port(self, port):
        self.__port = port

    def get_topic(self):
        return self.__topic

    def set_topic(self, topic):
        self.__topic = topic

    def log_to_oled(self, text):
        """Log a line of text to the OLED screen.

        The LCA2021 badge has a 32 character limit split across two screens.

        Arguments:
            text (Str): text to be logged
        Returns:
            Tuple (Bool, Str):
                Bool: A boolean of whether the request was made
                Str: Descriptive message
        """
        host = self.get_host()
        port = self.get_port()
        topic = self.get_topic()
        payload = f"(oled:log {text})"
        if host and topic:
            self.mqttc.connect(host, port)
            self.mqttc.publish(topic, payload)
            self.mqttc.disconnect()
            return (True, "SUCCESS")
        else:
            failure_msg = (
                "Could not publish speech to Swag Badge. "
                "Please check your Skill settings at https://home.mycroft.ai"
            )
            return (False, failure_msg)
