"""functions.py contains all functions within the program"""

from dictionaries import *
import pandas as pd
import os

def get_year():
    """Gets the user input for the year within the valid range [2024-2050].

    Returns:
    int: The selected year.
    """
    while True:
        try:
            print("Please enter the year you'd like. [2024-2050]")
            year = int(input("] "))
            if (2024 <= year <= 2050):
                break
            else:
                print("That year is out of range!")
        except ValueError:
            print("Please input a valid integar!")
    return year

def get_month():
    """Gets user input for the month within the valid range [1-12].

    Returns:
    int: The selected month.
    """
    while True:
        try:
            print("Please enter the month you'd like. [1-12]")
            month = int(input("] "))
            if 1 <= month <= 12:
                break
            else:
                print("That month is out of range!")
        except ValueError:
            print("Please input a valid integar!")
    return month

def days_in_month(year, month):
    """Determines amount of days for input month and the year.

    Parameters:
    year(int): The year.
    month(int): The Month.

    Returns:
    int: Specific amount of days in specified month.
    """
    if (month == 2) and ((year % 4 == 0 and year % 100 !=0) or (year % 400 == 0)):
        return 29
    else:
        monthDays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return monthDays[month]
    
def get_day(year, month):
    """Gets user input for the day within the valid range for the given month.

    Parameters:
    year(int): The year.
    month(int): The month.

    Returns:
    int: The selected day.
    """
    while True:
        try:
            print(f"Please enter the day you'd like. [1-{days_in_month(year, month)}]")
            day = int(input("] "))
            if (1 <= day <= days_in_month(year, month)):
                break
            else:
                print("That day is out of range!")
        except ValueError:
            print("Please input a valid integar!")
    return day

def get_date(year, month, day):
    """Gets user input for date and returns formatted date.

    Returns:
    str: Date string in DD-MM-YYYY format.
    """
    # Adds '0' infront of singular integars.
    month = str(month).zfill(2)
    day = str(day).zfill(2)

    datePhase = f"{day}-{month}-{year}"

    return datePhase

def retrieve_phase(date):
    """Determines moon phase for a given date.

    Parameters:
    date(str): The date used to determine moon phase.

    Returns:
    str: The moon phase for the corresponding date.

    """
    # Gets directory of the current script file.
    fileDirectory = os.path.dirname(os.path.realpath(__file__))
    # Joins directory path and file name to get full path of CSV file.
    filePath = os.path.join(fileDirectory, 'data.csv')

    # Reads CSV file into DataFrame.
    moonPhaseDataFrame = pd.read_csv(filePath)
    # Sets 'Data' Column as the index.
    moonPhaseDataFrame.set_index('Date', inplace=True)

    # Gets phase for selected date.
    return moonPhaseDataFrame.loc[date, 'Phase'].strip()

def retrieve_eclipses(eclipseType, year):
    """Determines eclipses for a given year.

    Parameters:
    eclipseType(str): The type of eclipse to retrieve.
    year(int): The year to retrieve eclipses from.

    Returns:
    list: List of eclipse information.

    """
    # Gets directory of the current script file.
    fileDirectory = os.path.dirname(os.path.realpath(__file__))
    # Joins directory path and file name to get full path of CSV file.
    filePath = os.path.join(fileDirectory, 'data.csv')

    # Reads CSV file into DataFrame.
    moonPhaseData = pd.read_csv(filePath)

    year_str = str(year)

    if (eclipseType == "Lunar & Solar"):
        eclipses = moonPhaseData[
            ((moonPhaseData['Events'] == 'Lunar Eclipse') | (moonPhaseData['Events'] == 'Solar Eclipse')) &
            (moonPhaseData['Date'].str.endswith(year_str))
        ]
    else:
        eclipses = moonPhaseData[
            (moonPhaseData['Events'] == eclipseType) &
            (moonPhaseData['Date'].str.endswith(year_str))
        ]
        
    eclipseInfo = eclipses[['Date', 'Events']].values.tolist()

    return eclipseInfo

def retrieve_moons_type(moonType, year):
    """Determines moon dates for a given year.

    Parameters:
    moonType(str): The type of moon phase to retrieve.
    year(int): The year to retrieve moon phase from.

    Returns:
    list: List of dats for specified moon phase.

    """
    # Gets directory of the current script file.
    fileDirectory = os.path.dirname(os.path.realpath(__file__))
    # Joins directory path and file name to get full path of CSV file.
    filePath = os.path.join(fileDirectory, 'data.csv')

    # Reads CSV file into DataFrame.
    moonPhaseData = pd.read_csv(filePath)

    moonDates = []

    year_str = str(year)

    moons = moonPhaseData[(moonPhaseData['Phase'] == moonType) & (moonPhaseData['Date'].str.endswith(year_str))]

    moonDates = moons['Date'].tolist()

    return moonDates

def get_mode():
    """Determines the mode for the calendar.
    """
    print("              Which mode would you like to use?              \n"
          "            Please choose from the options below.            \n"
          "")
    while True:
        try:
            print("1 ] Search Moon Phase by Date.\n"
                  "2 ] Monthly Moon Overview.\n"
                  "3 ] Annual Eclipse Overview.\n"
                  "4 ] Annual Moon Overview.")
            mode = int(input("] "))
            if (1 <= mode <= 4):
                break
            else:
                print("Choose between [1-4]!")
        except ValueError:
            print("Please input a valid integar!")
            
    return mode

def phase_by_date():
    """Retrieves selected date, determines corresponding phase, and displays result.
    """
    print()
    year = get_year()
    month = get_month()
    day = get_day(year, month)

    datePhase = get_date(year, month, day)
    phase = retrieve_phase(datePhase)
    phaseEmoji = phaseToEmoji.get(phase, '')

    print("\n"
          f"    --------| The Phase of the Moon on {datePhase} |--------\n"
          "\n"
          f"{datePhase} -- {phaseEmoji} | {phase}\n"
          "")

def monthly_moons():
    """Retrieves selected month, determines corresponding phases in month, and displays result.
    """
    print()
    year = get_year()
    month = get_month()

    monthDays = days_in_month(year, month)
    monthInText = monthToText.get(month)

    print("\n"
          f"    --------| The Phases for {monthInText} {year} |--------\n"
          "")

    for day in range(1, monthDays + 1):
        datePhase = get_date(year, month, day)
        phase = retrieve_phase(datePhase)
        phaseEmoji = phaseToEmoji.get(phase, '')

        print(f"{datePhase} -- {phaseEmoji} | {phase}")

    print()

def annual_eclipses():
    """Retreieves selected year, determines all chosen eclipse types within year, and displays results.
    """
    print()

    print("              Which type of Eclipse would you like?\n"
          "              Please choose from the options below.\n"
          "")
    
    while True:
        try:
            print("1 ] Lunar Eclipses.\n"
                  "2 ] Solar Eclipses.\n"
                  "3 ] Lunar & Solar.")
            eclipseType = int(input("] "))
            if (1 <= eclipseType <= 3):
                break
            else:
                print("Please choose between [1-3]!")
        except ValueError:
            print("Please input a valid integar!")

    eclipseType = eclipseOptions.get(eclipseType)
    print()
    year = get_year()

    print("\n"
          f"      --------| All {eclipseType} in {year} |--------\n"
          "")

    for date, event in retrieve_eclipses(eclipseType, year):
        print(f"{date} -- {event}")

    print()

def annual_moons():
    """Retrieves selected year, determines all full moons within year, and displays result.
    """
    print()

    print("              Which type of Moon would you like?\n"
          "             Please choose from the options below.\n"
          "")
    
    while True:
        try:
            print("1 ] Full Moons.\n"
                  "2 ] New Moons.\n"
                  "3 ] First Quarter.\n"
                  "4 ] Third Quarter.")
            moonType = int(input("] "))
            if (1 <= moonType <= 4):
                break
            else:
                print("Choose between [1-4]!")
        except ValueError:
            print("Please input a valid integar!")

    moonType = moonOptions.get(moonType)
    print()
    year = get_year()

    print("\n"
          f"      --------| All {moonType}s in {year} |--------")
    
    moonDates = retrieve_moons_type(moonType, year)

    for date in moonDates:
        phase = retrieve_phase(date)
        phaseEmoji = phaseToEmoji.get(phase, '')

        print(f"{date} -- {phaseEmoji} {phase}")

    print()

def main():
    """Calls chosen functions and handles multiple calls
    """
    while True:
        mode = get_mode()
        if (mode == 1):
            phase_by_date()
        elif (mode == 2):
            monthly_moons()
        elif (mode == 3):
            annual_eclipses()
        elif (mode == 4):
            annual_moons()

        print("             Would you like to use another mode?\n"
              "                             Y/N")
        recall = str(input("] ")).lower()
        print()

        if (recall not in {"yes", "y", ""}):
            break