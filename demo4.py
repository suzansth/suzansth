import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

# Function to calculate total salary
def calculate_salary(hours, rate):
    return hours * rate

# Initialize session state for storing work hours data
if 'work_hours' not in st.session_state:
    st.session_state.work_hours = []

# Title of the app
st.title("WorkHour")

# Input form for logging work hours
with st.form(key='log_hours_form'):
    date = st.date_input("Date", datetime.today())
    company = st.text_input("Company")
    hours = st.number_input("Hours Worked", min_value=0.0, step=0.5)
    rate = st.number_input("Hourly Rate", min_value=0.0, step=0.5)
    submit_button = st.form_submit_button(label='Log Hours')

    if submit_button:
        st.session_state.work_hours.append({
            "Date": date,
            "Company": company,
            "Hours Worked": hours,
            "Hourly Rate": rate,
            "Salary": calculate_salary(hours, rate)
        })
        st.success(f"Logged {hours} hours at rate ¥{rate} for {company} on {date}")

# Display logged work hours
if st.session_state.work_hours:
    df = pd.DataFrame(st.session_state.work_hours)
    st.subheader("Logged Work Hours")
    st.table(df)

    # Display total salary
    total_salary = df['Salary'].sum()
    st.subheader(f"Total Salary: ¥{total_salary:.2f}")

    # Download button
    st.download_button(
        label="Download Data as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='work_hours.csv',
        mime='text/csv',
    )

    # Generate and display charts
    st.subheader("Work Hours Chart")
    st.bar_chart(df.set_index("Date")["Hours Worked"])

    st.subheader("Cumulative Salary Chart")
    df['Cumulative Salary'] = np.cumsum(df['Salary'])
    st.line_chart(df.set_index("Date")["Cumulative Salary"])
