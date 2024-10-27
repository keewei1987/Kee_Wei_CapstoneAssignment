import streamlit as st


st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)


def calculate_rest_day_pay(job_type, monthly_salary, normal_working_hours_per_day, hours_worked_on_rest_day, employer_request=True):
    """
    Calculate pay for work done on a rest day based on employer or employee request.
    Includes logic for workman and non-workman based on monthly salary limits.

    Parameters:
    - job_type: Type of job, either "Non-workman" or "Workman".
    - monthly_salary: Monthly basic salary of the employee.
    - normal_working_hours_per_day: Normal daily working hours (e.g., 8 hours).
    - hours_worked_on_rest_day: Total hours worked on the rest day.
    - employer_request: If True, calculation is based on employer's request; 
                        if False, based on employee's request.

    Returns:
    - Pay for work done on the rest day.
    """

    # Define salary limits for overtime eligibility
    non_workman_salary_limit = 2600
    workman_salary_limit = 4500
    
    # Check overtime eligibility based on job type and salary
    if (job_type == "Non-workman" and monthly_salary > non_workman_salary_limit) or \
       (job_type == "Workman" and monthly_salary > workman_salary_limit):
        return 0  # If salary exceeds limit, no overtime pay is given

    # Calculate hourly basic rate of pay
    hourly_rate = (12 * monthly_salary) / (52 * 44)

    # Calculate pay based on working hours on rest day
    if employer_request:
        if hours_worked_on_rest_day <= normal_working_hours_per_day / 2:
            # For up to half of normal daily working hours
            rest_day_pay = hourly_rate * normal_working_hours_per_day
        elif hours_worked_on_rest_day <= normal_working_hours_per_day:
            # For more than half of normal daily working hours
            rest_day_pay = hourly_rate * normal_working_hours_per_day * 2
        else:
            # Beyond normal daily working hours (2 days' salary + overtime)
            rest_day_pay = hourly_rate * normal_working_hours_per_day * 2 + hourly_rate * 1.5 * (hours_worked_on_rest_day - normal_working_hours_per_day)
    else:
        if hours_worked_on_rest_day <= normal_working_hours_per_day / 2:
            # At the employee’s request: half day’s salary
            rest_day_pay = hourly_rate * normal_working_hours_per_day / 2
        elif hours_worked_on_rest_day <= normal_working_hours_per_day:
            # At the employee’s request: 1 day’s salary
            rest_day_pay = hourly_rate * normal_working_hours_per_day
        else:
            # Beyond normal daily working hours (1 day’s salary + overtime)
            rest_day_pay = hourly_rate * normal_working_hours_per_day + hourly_rate * 1.5 * (hours_worked_on_rest_day - normal_working_hours_per_day)

    return round(rest_day_pay, 2)

# Streamlit app setup
st.title("Rest Day Pay Calculator")

# Select job type
job_type = st.radio("Select Job Type", 
                    ("Non-workman earning a monthly basic salary of $2,600 or less.", 
                     "Workman earning a monthly basic salary of $4,500 or less."))

# Convert job type selection to simplified type for calculation
job_type = "Non-workman" if "Non-workman" in job_type else "Workman"

# Input fields for user data
monthly_salary = st.number_input("Enter Monthly Salary ($)", min_value=0, value=2600)
normal_working_hours_per_day = st.number_input("Enter Normal Working Hours Per Day", min_value=1, max_value=12, value=8)
hours_worked_on_rest_day = st.number_input("Enter Hours Worked on Rest Day", min_value=0.0, max_value=24.0, value=10.0)
employer_request = st.radio("Was the work done at the employer’s request?", ("Yes", "No"))

# Convert radio button input to boolean
employer_request_bool = True if employer_request == "Yes" else False

# Calculate pay when the user clicks the button
if st.button("Calculate Rest Day Pay"):
    pay = calculate_rest_day_pay(job_type, monthly_salary, normal_working_hours_per_day, hours_worked_on_rest_day, employer_request_bool)
    if pay == 0:
        st.write("### Overtime pay is not applicable as the monthly salary exceeds the limit for the selected job type.")
    else:
        st.write(f"### Pay for work done on rest day: **${pay}**")

# Footer information
st.markdown(
    """
    - **Hourly Rate Calculation Formula**: (12 x Monthly Basic Pay) / (52 x 44).
    - Pay is calculated based on different conditions specified by the Employment Act.
    """
)
