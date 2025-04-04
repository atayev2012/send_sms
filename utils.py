import tomllib
from log_module import logger
import sys

config_toml_path = "config.toml"

# read arguments from input
class Args:
    def __init__(self, args: list = sys.argv):
        self.__load_args(args)

    @logger
    def __load_args(self, args: list):
        if len(args) < 4:
            raise Exception("Not enough arguments passed through command line, should be at least 3 arguments!")

        self.sender = self.__validate_phone_number(args[1])
        self.recipient = self.__validate_phone_number(args[2])
        self.message = " ".join(args[3:])

    @logger
    def __validate_phone_number(self, phone_number: str):
        # removing + sign if contains
        number = phone_number.strip().replace("+", "")

        # removing brackets ()
        number = number.replace("(", "")
        number = number.replace(")", "")

        #check if digit
        if number.isdigit():
            return f"+{number}"
        else:
            raise Exception(f"Invalid phone number: {phone_number}")

    def __str__(self):
        return f"{self.sender} {self.recipient} {self.message}"

# read data from toml configuration file
class Config:
    def __init__(self, config_path: str = config_toml_path):
        self.config_path = config_path
        self.__load_config()

    @logger
    def __load_config(self):
        with open(self.config_path, "rb") as file:
            conf = tomllib.load(file)
        self.method = conf["request"]["method"]
        self.default_response_size = conf["request"]["default_response_size"]
        self.timeout = int(conf["request"]["timeout"])
        self.username = conf["user"]["username"]
        self.password = conf["user"]["password"]
        self.__convert_url(conf["request"]["url"])
    @logger
    def __convert_url(self, url: str):
        if url.startswith("http:"):
            data = url[7:].split("/", 1)
        elif url.startswith("https:"):
            data = url[8:].split("/", 1)
        else:
            data = url.split("/", 1)

        self.path = "/" + data[1]
        if ":" in data[0]:
            self.host, port = data[0].split(":")
            self.port = int(port)
        else:
            self.host = data[0]
            self.port = 80
