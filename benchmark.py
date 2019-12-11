import pymysql
import os

db = pymysql.connect(
    os.environ["DATABASE_HOST"], 
    os.environ["DATABASE_USER"], 
    os.environ["DATABASE_PASSWORD"], 
    os.environ["DATABASE_NAME"]
    )

cursor = db.cursor()

#@profile
def singleCommitInsertBenchmarck():
    for insert in range(2000):
        cursor.execute("INSERT INTO american_football_event_states (id, event_id, current_state, sequence_number, period_value, period_time_elapsed, period_time_remaining, clock_state, down, team_in_possession_id, distance_for_1st_down, field_side, field_line, context) VALUES ({}, '3119', '1', NULL, '0', NULL, '15:00', NULL, NULL, NULL, NULL, NULL, NULL, 'event');".format(insert + 250))
    db.commit()

#@profile
def oneCommitPerInsertBenchmark():
    for insert in range(2000):    
        cursor.execute("INSERT INTO american_football_event_states (id, event_id, current_state, sequence_number, period_value, period_time_elapsed, period_time_remaining, clock_state, down, team_in_possession_id, distance_for_1st_down, field_side, field_line, context) VALUES ({}, '3119', '1', NULL, '0', NULL, '15:00', NULL, NULL, NULL, NULL, NULL, NULL, 'event');".format(insert + 2250))
        db.commit()

#@profile
def updateBenchmark():
    for primary_key in range(4000):    
        cursor.execute("UPDATE american_football_event_states SET context = 'updated_event' WHERE id = {}".format(primary_key + 250))


#@profile
def deleteBenchmark():
    for primary_key in range(4000):
        cursor.execute("DELETE FROM american_football_event_states WHERE id = {}".format(primary_key + 250))



if __name__ == "__main__":
    singleCommitInsertBenchmarck()
    oneCommitPerInsertBenchmark()
    updateBenchmark()
    deleteBenchmark()
    db.close()
