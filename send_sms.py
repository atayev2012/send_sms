from http_module import HTTPRequest

def main():
    request = HTTPRequest()
    response = request.send()
    print(response)


if __name__ == '__main__':
    main()