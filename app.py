import os
import streamlit as st
import mysql.connector
import pandas as pd

# sql connection
conn = mysql.connector.connect(
    host="localhost",
    user="Cse299",
    password="12345",
    database="attendance_system"
)
cursor = conn.cursor()

# getrecords
def fetch_attendance():
    query = """
    SELECT a.student_id, s.name, a.timestamp
    FROM Attendance a
    JOIN Students s ON a.student_id = s.student_id
    """
    cursor.execute(query)
    records = cursor.fetchall()
    return [{"Student ID": r[0], "Name": r[1], "Timestamp": r[2]} for r in records]


st.title("Facial Recognition Attendance System")

if st.button("Start Recognition"):
    st.info("Running facial recognition system...")
    try:
        os.system("python atten2.py")  
        st.success("Facial recognition system is running.")
    except Exception as e:
        st.error(f"Error while running recognition: {e}")

# button to display attendance table
if st.button("Display Attendance Table"):
    records = fetch_attendance()
    if records:
        df = pd.DataFrame(records)
        st.table(df)
    else:
        st.write("No attendance records found.")

conn.close()




