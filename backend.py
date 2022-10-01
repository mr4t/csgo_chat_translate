from PyQt5.QtCore import QThread, pyqtSignal
import requests
import socket


class backend(QThread):
    update_progress = pyqtSignal(str)
    def __init__(self, target_lang):
        super().__init__()
        self.target_lang = target_lang

        self.HOST = "localhost"
        self.PORT = 2121
        self.url = "https://nlp-translation.p.rapidapi.com/v1/translate"

        self.payload_template = "text={}&to={}"
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": "", # API KEY
            "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"
        }


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            print("connected")
            while True:
                message = s.recv(1024)
                try:
                    message = message.decode("utf-8")
                    if " : " in message:
                        message_split = list(map(lambda x: x.strip(), message.split(" : ")))
                        query_string = " ".join(message_split[1:])

                        payload = self.payload_template.format("%20".join(query_string.split()), self.target_lang)
                        payload = payload.encode("utf-8")
                        response = requests.request("POST", self.url, data=payload, headers=self.headers).json()

                        if response.get("status") == 200:
                            translated = response.get("translated_text").get("tr")
                            self.update_progress.emit(f"{message_split[0]} : {translated}")
                except UnicodeDecodeError:
                    print(message)
