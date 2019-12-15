import time
import multiprocessing as mp
import psutil
import numpy as np
from keras.models import load_model
import pymysql

DB = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     db='cesi')

CURSOR = DB.cursor()



def single_commit_insert_benchmark():
    for insert in range(2000):
        CURSOR.execute("INSERT INTO american_football_event_states (id, event_id, current_state, sequence_number, period_value, period_time_elapsed, period_time_remaining, clock_state, down, team_in_possession_id, distance_for_1st_down, field_side, field_line, context) VALUES ({}, '3119', '1', NULL, '0', NULL, '15:00', NULL, NULL, NULL, NULL, NULL, NULL, 'event');".format(insert + 250))
    DB.commit()



def one_commit_per_insert_benchmark():
    for insert in range(2000):
        CURSOR.execute("INSERT INTO american_football_event_states (id, event_id, current_state, sequence_number, period_value, period_time_elapsed, period_time_remaining, clock_state, down, team_in_possession_id, distance_for_1st_down, field_side, field_line, context) VALUES ({}, '3119', '1', NULL, '0', NULL, '15:00', NULL, NULL, NULL, NULL, NULL, NULL, 'event');".format(insert + 2250))
        DB.commit()



def update_benchmark():
    for primary_key in range(4000):
        CURSOR.execute("UPDATE american_football_event_states SET context = 'updated_event' WHERE id = {}".format(
            primary_key + 250))



def delete_benchmark():
    for primary_key in range(4000):
        CURSOR.execute("DELETE FROM american_football_event_states WHERE id = {}".format(
            primary_key + 250))


def monitor(target):
    worker_process = mp.Process(target=target)
    worker_process.start()
    p = psutil.Process(worker_process.pid)

    # log cpu usage of `worker_process` every 10 ms
    cpu_percents = []
    while worker_process.is_alive():
        cpu_percents.append(p.disk_io_counters())
        time.sleep(0.01)

    worker_process.join()
    return cpu_percents


def media(percents):
    suma = 0
    for percent in percents:
        suma = suma + percent

    media = suma / len(percents)
    return media

cpu_percents = monitor(target=single_commit_insert_benchmark)
print("single_commit_insert_benchmark: ", cpu_percents)

cpu_percents = monitor(target=one_commit_per_insert_benchmark)
print("one_commit_per_insert_benchmark: ", cpu_percents)

cpu_percents = monitor(target=update_benchmark)
print("update_benchmark: ", cpu_percents)

cpu_percents = monitor(target=delete_benchmark)
print("DELETE: ", cpu_percents)

print(" ")
print(" ")