from datetime import datetime

def get_current_academic_term():
    # Get the current date
    today = datetime.today()

    # Determine the academic year (e.g., 2024-2025)
    current_year = today.year
    if today.month >= 8:  # August to December
        academic_year = f"{current_year}-{current_year + 1}"
        current_semester = '1st'  # 1st Semester
    elif today.month <= 5:  # January to May
        academic_year = f"{current_year - 1}-{current_year}"
        current_semester = '2nd'  # 2nd Semester
    else:
        academic_year = f"{current_year - 1}-{current_year}"
        current_semester = 'Sum'  # Summer Semester

    # Return the academic year and semester as a tuple
    return academic_year, current_semester