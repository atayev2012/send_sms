# Send SMS Client Application

A Python-based SMS sender that uses HTTP requests to send messages, with configurable settings via TOML and built-in logging.

## 📦 Modules Overview
- `send_sms.py` - Main script to initiate sending the HTTP requests.
- `utils.py` - Handles command-line arguments and TOML config parsing.
- `http_module.py` - Manages socket connection for HTTP requests/responses for SMS APIs.
- `log_module.py` - Provides logging decorators for function calls.

---

## 🛠 Installation

### Prerequisites
- Python 3.11+
- Pip package manager

### Steps
- Clone the repository:
   ```bash
   git clone https://github.com/atayev2012/send_sms.git
   cd send_sms
   
- For unit tests need to install additional pytest library:
   ```bash
   pip install -r requirements.txt

## ⚙️ Configuration
- Edit config.toml in the project root:
    ```bash
    [user]
    username = "user"
    password = "pass"
    
    [request]
    url = "http://example.com:80/send_sms"
    timeout = 10 # in seconds
    method = "POST"
    default_response_size = 4096 # in bytes (4kb)

## 🚀 Usage
-   Command-Line Arguments
- The script requires 3 arguments:

  1. Sender's phone number
  2. Recipient's phone number
  3. Message text
 
    ```bash
    python send_sms.py +79999999999 +71112223344 Hello friend
   
 -  On MacOS/Unix like systems should be run with python3
    ```bash
    python3 send_sms.py +79999999999 +71112223344 Hello friend!

## Logging

- All operations are logged to log.txt file in project root
    
    Example log entry
    ```bash
   [04.04.2025 13:07:51.222760] - Module: http_module - Method: HTTPRequest.send successfully executed with args: (<http_module.HTTPRequest object at 0x102c45010>,) - return values: status code: 200	body: {'status': 'success', 'message_id': '123456'}
## Result
- Upon successful operation response details will be introduced in terminal as shown below

    ```bash
    status code: 200        body: {'status': 'success', 'message_id': '123456'}