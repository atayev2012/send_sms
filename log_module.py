from datetime import datetime, UTC
from os.path import isfile

def logger(func):
    def wrapper(*args, **kwargs):
            if not isfile("log.txt"):
                open("log.txt", "w").close()

            try:
                with open(f"log.txt", "a") as file:
                    date = datetime.now(UTC).strftime("[%d.%m.%Y %H:%M:%S.%f]")
                    message = f"{date} - Module: {func.__module__} - Method: {args[0].__class__.__name__}.{func.__name__} launched with args: {args}\n"
                    file.write(message)

                    value = func(*args, **kwargs)
                    results = f" - return values: {value}" if value else ""

                    date = datetime.now(UTC).strftime("[%d.%m.%Y %H:%M:%S.%f]")
                    message = f"{date} - Module: {func.__module__} - Method: {args[0].__class__.__name__}.{func.__name__} successfully executed with args: {args}{results}\n"
                    file.write(message)
                    return value
            except (FileNotFoundError, PermissionError) as e:
                date = datetime.now(UTC).strftime("[%d.%m.%Y %H:%M:%S.%f]")
                message = f"{date} - Error with writing to log file: {str(e)}\n"
                print(message)
                exit(1)
            except Exception as e:
                date = datetime.now(UTC).strftime("[%d.%m.%Y %H:%M:%S.%f]")
                message = f"{date} - Error: {str(e)} in Module: {func.__module__} - Method: {args[0].__class__.__name__}.{func.__name__} with args: {args}\n"
                try:
                    with open(f"log.txt", "a") as file:
                        file.write(message)
                    print(f"\033[91m{message}\033[0m")
                    exit(1)
                except (FileNotFoundError, PermissionError) as e:
                    date = datetime.now(UTC).strftime("[%d.%m.%Y %H:%M:%S.%f]")
                    message = f"{date} - Error with writing to log file: {str(e)}\n"
                    print(f"\033[91m{message}\033[0m")
                    exit(1)
    return wrapper