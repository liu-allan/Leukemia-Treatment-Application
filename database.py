#!/usr/bin/python

# Example script to set-up and create the necessary tables for the database.
# Also serves as the definition of keys and columns of each table.

import bcrypt
import sqlite3

conn = sqlite3.connect("db.db")

conn.execute(
    """
        CREATE TABLE IF NOT EXISTS oncologists
            (username TEXT NOT NULL,
             password TEXT NOT NULL,
             full_name TEXT NOT NULL,
             PRIMARY KEY(username));
    """
)

conn.execute(
    """
        CREATE TABLE IF NOT EXISTS patients
            (id INTEGER NOT NULL,
             user_id TEXT NOT NULL,
             name TEXT NOT NULL,
             phone_number TEXT NOT NULL,
             birthday TEXT NOT NULL,
             age INTEGER NOT NULL, 
             blood_type TEXT NOT NULL CHECK( blood_type IN ('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-') ),
             all_type TEXT NOT NULL CHECK( all_type IN ('Immunophenotype', 'French-American-British (FAB)', 'ALL Cytogenetic Risk Group') ), 
             weight REAL NOT NULL,
             height REAL NOT NULL,
             body_surface_area REAL NOT NULL,
             oncologist_id TEXT NOT NULL,
             PRIMARY KEY(id),
             FOREIGN KEY(oncologist_id)
                REFERENCES oncologists(username)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
    """
)

conn.execute(
    """
        CREATE TABLE IF NOT EXISTS measurements
            (time TEXT NOT NULL,
             anc_measurement REAL NOT NULL,
             dosage_measurement REAL NOT NULL,
             patient_id INTEGER NOT NULL,
             PRIMARY KEY(time, patient_id),
             FOREIGN KEY(patient_id) 
                REFERENCES patients(id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
    """
)

# INSERT examples are listed below, feel free to uncomment to insert any entries as needed.

# encrypting password so it's not stored in plain text
password = "password"
bytes = password.encode("utf-8")
salt = bcrypt.gensalt()
hash = bcrypt.hashpw(bytes, salt)

# conn.execute(
#     '''
#       INSERT INTO oncologists (username, password, full_name)
#       VALUES ('angus', ?, 'Angus Wang')
#     ''',
#     (hash,),
# )

# conn.execute(
#     """
#       INSERT INTO patients (user_id, name, phone_number, birthday, age, blood_type, all_type, weight, height, body_surface_area, oncologist_id)
#       VALUES ('smallbob123456', 'Small Bob', '1234567899', '19900506', 38, 'A+', 'Immunophenotype', 1, 1, 250, 'angus');
#     """
# )

# conn.execute(
#     """
#       INSERT INTO measurements (time, anc_measurement, dosage_measurement, patient_id)
#       VALUES ("20220101", 4, 4, 1);
#     """
# )

conn.execute(
    "PRAGMA foreign_keys = ON"
)  # enable foreign key cascade on delete

conn.commit()  # this is necessary to confirm entry into the database

conn.close()
