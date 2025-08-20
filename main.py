import os
import json
import random
import math
import argparse
from datetime import datetime, date, timedelta
import time
import threading
import generate_words
import db

DB_PATH = "repetition.db"

BASE_INTERVALS = [0, 1, 3, 7, 15]  # Интервалы для повторений

dt1 = date(2025, 7, 19)


def get_array():
    str_list = generate_words.generate_words()
    words = str_list.strip().split('\n')
    array = []

    # Ручное разделение на 30 строк по 10 слов
    for i in range(0, 300, 10):  # 30 строк * 10 слов = 300
        line = ' '.join(words[i:i+10])
        array.append(line)

    return array


def main():
    today_date = date.today()
    if not db.db_file_exists():
        cursor = db.connection_db()
        db.init_db(cursor)

        array = get_array()

        for study_day in range(1, 31):  # study_day от 1 до 30
            # Для каждого интервала повторения
            for interval in BASE_INTERVALS:
                repetition_day = study_day + interval
                db.insert_db(cursor, study_day, repetition_day, array[study_day-1])

    cursor = db.connection_db()
    nowadays_words = db.get_db(cursor, (today_date - dt1).days)

    print(nowadays_words)


if __name__ == '__main__':
    main()
