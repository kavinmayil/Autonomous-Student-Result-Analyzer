import streamlit as st
import pandas as pd

st.title("🎓 Student Result Analyzer")

sheet_url = st.text_input("Enter your Google Sheet URL (Set sharing to 'Anyone with the link')")

def compute_result(assign, test, attendance, semester_mark):
    try:
        attendance_mark = (attendance / 100) * 20
        internal_40 = (assign + test + attendance_mark) * (40 / 60)
        sem_60 = semester_mark * (60 / 100)
        total = internal_40 + sem_60

        # Grade
        if total >= 90:
            grade = "A+"
        elif total >= 80:
            grade = "A"
        elif total >= 70:
            grade = "B+"
        elif total >= 60:
            grade = "B"
        elif total >= 50:
            grade = "C"
        else:
            grade = "F"

        status = "Pass" if total >= 50 else "Fail"

        return round(internal_40, 2), round(sem_60, 2), round(total, 2), grade, status
    except:
        return 0, 0, 0, "Error", "Error"

if sheet_url:
    try:
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

        df = pd.read_csv(csv_url)

        results = df.apply(lambda row: compute_result(
            row['Assignment Mark'],
            row['Test Mark'],
            row['Attendance (%)'],
            row['Semester Mark (/100)']
        ), axis=1)

        df[['Internal (40)', 'Semester (60)', 'Total', 'Grade', 'Result']] = pd.DataFrame(results.tolist(), index=df.index)

        st.subheader("📊 Full Result Data")
        st.dataframe(df)

        total_students = len(df)
        pass_students = df[df['Result'] == "Pass"]
        fail_students = df[df['Result'] == "Fail"]

        st.subheader("📌 Summary")
        st.write(f"**Total Students:** {total_students}")
        st.write(f"✅ Pass: {len(pass_students)}")
        st.write(f"❌ Fail: {len(fail_students)}")

        st.subheader("✅ Passed Students")
        st.dataframe(pass_students[['Student Name', 'Grade', 'Total']])

        st.subheader("❌ Failed Students")
        st.dataframe(fail_students[['Student Name', 'Grade', 'Total']])

    except Exception as e:
        st.error("❌ Failed to load sheet. Please check the URL and column names.")
        st.exception(e)
