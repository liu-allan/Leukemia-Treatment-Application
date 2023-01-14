#!/usr/bin/python

# Example script to set-up and create the necessary tables for the database.
# Also serves as the definition of keys and columns of each table.

import sqlite3

conn = sqlite3.connect("db.db")

conn.execute(
    """
        CREATE TABLE IF NOT EXISTS oncologists
            (username TEXT NOT NULL,
             password TEXT NOT NULL,
             PRIMARY KEY(username));
    """
)

conn.execute(
    """
        CREATE TABLE IF NOT EXISTS patients
            (id INTEGER NOT NULL,
             name TEXT NOT NULL,
             weight REAL NOT NULL,
             height REAL NOT NULL,
             body_surface_area REAL NOT NULL,
             dosage REAL NOT NULL,
             oncologist_id TEXT NOT NULL,
             PRIMARY KEY(id),
             FOREIGN KEY(oncologist_id)
                REFERENCES oncologists(id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
    """
)

conn.execute(
    """
        CREATE TABLE IF NOT EXISTS measurements
            (time TEXT NOT NULL,
             anc_measurement REAL NOT NULL,
             patient_id INTEGER NOT NULL,
             PRIMARY KEY(time, patient_id),
             FOREIGN KEY(patient_id) 
                REFERENCES patients(id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
    """
)

# INSERT examples are listed below, feel free to uncomment to insert any entries as needed.

# conn.execute(
#     '''
#       INSERT INTO oncologists (username, password)
#       VALUES ('angus', 'password')
#     '''
# )

# conn.execute(
#     """
#       INSERT INTO patients (name, weight, height, body_surface_area, dosage, oncologist_id)
#       VALUES ('Small Mac', 1, 1, 250, 60, 'angus');
#     """
# )

# conn.execute(
#     """
#       INSERT INTO measurements (time, anc_measurement, patient_id)
#       VALUES ("20220101", 4, 4);
#     """
# )

conn.commit()  # this is necessary to confirm entry into the database

conn.close()
