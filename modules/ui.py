from InquirerPy import inquirer, prompt
from InquirerPy.validator import ValidationError
import os
import time

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_error(ui_type: str, msg: str, sleep_duration: float = 3):
    print(f"\033[91m[!] - {msg}\033[0m")
    time.sleep(sleep_duration)

def not_empty_validator(val):
    if len(val.strip()) == 0:
        raise ValidationError(message="Boş bırakılamaz.")
    return True

def validation_error(msg: str):
    raise ValidationError(message=msg)

def select_menu(ui_type: str, choices: list, message: str = "Bir seçenek seçin:", Type: str = "fuzzy", header=None) -> str:
    clear_screen()
    if header:
        print(header)
        
    question = [
        {
            "type": Type, # BURADAKİ 'Type' parametresi string olmalı
            "name": "selection",
            "message": message,
            "choices": choices,
            "border": True,
            "cycle": True,
            "max_height": "70%",
        }
    ]
    result = prompt(question)
    return result.get("selection", "")

def search_menu(ui_type: str, message: str = "Bir şey yazın:") -> str:
    clear_screen()
    result = inquirer.text(
        message=message,
        validate=not_empty_validator
    ).execute()
    return result

