import argparse
import tomllib


# read arguments from input
class Args:
    def __init__(self):
        self.__load_args()

    def __load_args(self):
        parser = argparse.ArgumentParser(
            prog="python3 send-sms.py",
            description="send-sms - CLI client for sending SMS messages"
        )
        parser.add_argument("sender", type=str, help="Sender's phone number (without spaces)")
        parser.add_argument("recipient", type=str, help="Recipient's phone number (without spaces)")
        parser.add_argument("message", type=str, help="Message text")

        # read arguments
        known_args, unknown_args = parser.parse_known_args()

        # add all additional unknown arguments to message
        known_args.message += f" {' '.join(unknown_args)}"

        self.sender = known_args.sender
        self.recipient = known_args.recipient
        self.message = known_args.message

# read data from toml configuration file
class Config:
    def __init__(self, config_path: str = "config.toml"):
        self.config_path = config_path
        self.__load_config()

    def __load_config(self):
        with open(self.config_path, "rb") as file:
            conf = tomllib.load(file)
        self.method = conf["request"]["method"]
        self.default_response_size = conf["request"]["default_response_size"]
        self.timeout = conf["request"]["timeout"]
        self.username = conf["user"]["username"]
        self.password = conf["user"]["password"]
        self.__convert_url(conf["request"]["url"])

    def __convert_url(self, url: str):
        if url.startswith("http:"):
            data = url[7:].split("/", 1)
        elif url.startswith("https:"):
            data = url[8:].split("/", 1)
        else:
            data = url.split("/", 1)

        self.path = "/" + data[1]
        if ":" in data[0]:
            self.host, self.port = data[0].split(":")
        else:
            self.host = data[0]
            self.port = 80



config = Config()
# args = Args()


if __name__ == "__main__":
    print(config.host)
    print(config.port)
    print(config.path)