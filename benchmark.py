import os
import pymysql

DB = pymysql.connect(
    os.environ["DATABASE_HOST"],
    os.environ["DATABASE_USER"],
    os.environ["DATABASE_PASSWORD"],
    os.environ["DATABASE_NAME"]
)

CURSOR = DB.cursor()

# @profile


def single_commit_insert_benchmark():
    for insert in range(2000):
        CURSOR.execute('''INSERT INTO american_football_event_states (id, event_id, current_state,
        sequence_number, period_value, period_time_elapsed, period_time_remaining, clock_state, down,team_in_possession_id, distance_for_1st_down, field_side, field_line, context)
        VALUES ({}, '3119', '1', NULL, '0', NULL, '15:00', NULL, NULL, NULL, NULL,
        NULL, NULL, 'event');'''.format(insert + 250))
    DB.commit()

# @profile


def one_commit_per_insert_benchmark():
    for insert in range(2000):
        CURSOR.execute('''INSERT INTO american_football_event_states (id, event_id, current_state,
        sequence_number, period_value, period_time_elapsed, period_time_remaining, clock_state,
        down, team_in_possession_id, distance_for_1st_down, field_side, field_line, context)
        VALUES ({}, '3119', '1', NULL, '0', NULL, '15:00', NULL, NULL, NULL, NULL, NULL, NULL,
        'event');'''.format(insert + 2250))
        DB.commit()

# @profile


def update_benchmark():
    for primary_key in range(4000):
        CURSOR.execute('''UPDATE american_football_event_states SET context = 'updated_event'
        WHERE id = {}'''.format(primary_key + 250))


# @profile
def delete_benchmark():
    for primary_key in range(4000):
        CURSOR.execute("DELETE FROM american_football_event_states WHERE id = {}".format(
            primary_key + 250))


if __name__ == "__main__":
    single_commit_insert_benchmark()
    one_commit_per_insert_benchmark()
    update_benchmark()
    delete_benchmark()
    DB.close()
