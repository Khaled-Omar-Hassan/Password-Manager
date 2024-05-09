import os
import json
import time

import pandas as pd
from random import choice, shuffle
import pyperclip

UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS = '0123456789'
SYMBOLS = '!#$%&()*+'
ALL_CHARACTERS = list(UPPER + LOWER + NUMBERS + SYMBOLS)


class PasswordManager:
    def __init__(self, user_name):
        self.user_name = user_name
        self.data_file = f"Users/Json_Data/{user_name}_data.json"
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}

    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def generate(self, upper=0, lower=0, number=0, symbol=0):
        uppers = [choice(UPPER) for _ in range(int(upper))]
        lowers = [choice(LOWER) for _ in range(int(lower))]
        numbers = [choice(NUMBERS) for _ in range(int(number))]
        symbols = [choice(SYMBOLS) for _ in range(int(symbol))]
        password_list = uppers + lowers + numbers + symbols
        shuffle(password_list)
        password = "".join(password_list)
        pyperclip.copy(password)
        return password

    def save_password(self, website, email, password, comment=""):
        new_entry = {
            "email": email,
            "password": password,
            "comment": comment
        }
        self.data[website] = new_entry
        self.save_data()

    def search_password(self, website):
        return self.data.get(website, None)

    def show_database(self):
        data_df = pd.DataFrame.from_dict(self.data, orient='index')
        csv_path = f"Users\\CSV_Data\\{self.user_name}_database.csv"
        data_df.to_csv(csv_path)
        time.sleep(1)
        os.startfile(csv_path)
