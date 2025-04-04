import socket
import json
from base64 import b64encode
from log_module import logger
from utils import Config, Args


class Connection:
    def __init__(self, conf: Config = Config()):
        self.host = conf.host
        self.port = conf.port
        self.timeout = conf.timeout

    @logger
    def __enter__(self) -> socket.socket:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
        return self.sock

    @logger
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()


class HTTP:
    def __init__(self):
        self.status_code = None
        self.status_message = None
        self.first_line = ""
        self.headers = {}
        self.body = {}

    @logger
    def from_bytes(self, binary_data: bytes):
        first_line_headers, body = binary_data.decode("utf-8").split("\r\n\r\n", 1)
        self.first_line, headers = first_line_headers.split("\r\n", 1)
        _, self.status_code, self.status_message = self.first_line.split(" ", 2)

        for line in headers.split("\r\n"):
            key, value = line.split(": ", 1)
            self.headers[key] = value

        if self.headers.get("Content-type") == "application/json":
            self.body = json.loads(body)

        return self

    @logger
    def to_bytes(self) -> bytes:
        body_str = json.dumps(self.body) if self.body else ""
        self.headers["Content-Length"] = str(len(body_str))

        headers_str = "\r\n".join(f"{key}: {value}" for key, value in self.headers.items()) if self.headers else ""
        raw_request = f"{self.first_line}\r\n{headers_str}\r\n\r\n{body_str}"
        return raw_request.encode("utf-8")


class HTTPRequest(HTTP):
    def __init__(self, conf: Config = Config(), args: Args = Args()):
        super().__init__()
        self.conf = conf
        self.args = args
        self.__request_generator()

    @logger
    def __auth_data_encoding(self):
        if hasattr(self.conf, "username") and hasattr(self.conf, "password"):
            credentials = f"{self.conf.username}:{self.conf.password}".encode("utf-8")
            encoded_credentials = b64encode(credentials).decode("utf-8")
            self.headers["Authorization"] = f"Basic {encoded_credentials}"

    @logger
    def __request_generator(self):
        self.first_line = " ".join([self.conf.method, self.conf.path, f" HTTP/1.1"])

        self.headers["Content-type"] = "application/json"
        self.headers["Accept"] = "application/json"
        self.headers["Connection"] = "close"
        self.__auth_data_encoding()

        self.body["sender"] = self.args.sender
        self.body["recipient"] = self.args.recipient
        self.body["message"] = self.args.message

    @logger
    def send(self):
        with Connection() as conn:
            conn.send(self.to_bytes())
            binary_response = conn.recv(self.conf.default_response_size)
            try:
                while True:
                    binary_response += conn.recv(self.conf.default_response_size)
                    if self.__check_response_loaded(binary_response):
                        break
            except TimeoutError as e:
                print("Connection timed out")
            response = HTTPResponse()
            response.from_bytes(binary_response)
            return response

    @logger
    def __check_response_loaded(self, response: bytes):
        response_str = response.decode("utf-8")
        if "\r\n\r\n" in response_str:
            header, body = response_str.split("\r\n\r\n", 1)
            for line in header.split("\r\n")[1:]:
                key, value = line.split(": ", 1)
                if key == "Content-Length":
                    return len(body) == int(value)
        return False


class HTTPResponse(HTTP):
    @logger
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"status code: {self.status_code}\tbody: {self.body}"
