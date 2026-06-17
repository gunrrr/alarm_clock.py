#!/usr/bin/env python3

import time
import shutil
import requests
from datetime import datetime

API_KEY = "72f08bebdc3c58877e393a7e3c36dadd"
CITY_ID = "5921357"
ALARM_TIME = input("Set alarm (HH:MM): ")

DIGITS = {
    "0": [" ███ ",
          "█   █",
          "█   █",
          "█   █",
          " ███ "],
    "1": ["  █  ",
          " ██  ",
          "  █  ",
          "  █  ",
          "█████"],
    "2": ["████ ",
          "    █",
          " ███ ",
          "█    ",
          "█████"],
    "3": ["████ ",
          "    █",
          " ███ ",
          "    █",
          "████ "],
    "4": ["█   █",
          "█   █",
          "█████",
          "    █",
          "    █"],
    "5": ["█████",
          "█    ",
          "████ ",
          "    █",
          "████ "],
    "6": [" ███ ",
          "█    ",
          "████ ",
          "█   █",
          " ███ "],
    "7": ["█████",
          "    █",
          "   █ ",
          "  █  ",
          " █   "],
    "8": [" ███ ",
          "█   █",
          " ███ ",
          "█   █",
          " ███ "],
    "9": [" ███ ",
          "█   █",
          " ████",
          "    █",
          " ███ "],
    ":": ["     ",
          "  █  ",
          "     ",
          "  █  ",
          "     "],
    " ": ["     ",
          "     ",
          "     ",
          "     ",
          "     "]
}


def render_time(t):
    rows = [""] * 5
    for ch in t:
        for i in range(5):
            rows[i] += DIGITS[ch][i] + "  "
    return rows


def get_weather():
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?id={CITY_ID}&appid={API_KEY}&units=metric"
        )
        data = requests.get(url, timeout=5).json()
        temp = round(data["main"]["temp"])
        desc = data["weather"][0]["main"]
        return f"{temp}°C  {desc}"
    except:
        return "Weather unavailable"


def box(width, text):
    return "║" + text.center(width - 2) + "║"


def line(width):
    return "╠" + "═" * (width - 2) + "╣"


def top(width):
    return "╔" + "═" * (width - 2) + "╗"


def bottom(width):
    return "╚" + "═" * (width - 2) + "╝"


def alarm_beep():
    try:
        while True:
            for _ in range(3):
                print("\a", end="", flush=True)
                time.sleep(0.15)
            time.sleep(0.6)
    except KeyboardInterrupt:
        pass


print("\033[2J\033[H\033[?25l", end="")

last_weather = 0
weather = "Loading..."

try:
    while True:
        now = datetime.now()
        width = max(70, shutil.get_terminal_size().columns)

        tstr = now.strftime("%I:%M:%S").lstrip("0")

        if time.time() - last_weather > 600:
            try:
                url = (
                    f"https://api.openweathermap.org/data/2.5/weather"
                    f"?id={CITY_ID}&appid={API_KEY}&units=metric"
                )
                data = requests.get(url, timeout=5).json()
                temp = round(data["main"]["temp"])
                desc = data["weather"][0]["main"]
                weather = f"{temp}°C  {desc}"
            except:
                weather = "Weather unavailable"
            last_weather = time.time()

        date_str = now.strftime("%A  %B %d, %Y")

        print("\033[H", end="")
        print("\033[92m", end="")

        print(top(width))
        print(box(width, date_str))
        print(line(width))

        for row in render_time(tstr):
            print(box(width, row))

        print(line(width))
        print(box(width, f"Alarm: {ALARM_TIME}"))
        print(box(width, f"Outside: {weather}"))
        print(bottom(width))

        print("\033[0m", end="", flush=True)

        if now.strftime("%H:%M") == ALARM_TIME:
            alarm_beep()

        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    print("\033[?25h\033[0m")
