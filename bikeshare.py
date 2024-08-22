import time
import pandas as pd

# Constants for messages and column names
TIME_TAKEN_MSG = '\nThis took %s seconds.'
START_TIME = 'Start Time'
END_TIME = 'End Time'
TRIP_DURATION = 'Trip Duration'
START_STATION = 'Start Station'
END_STATION = 'End Station'
USER_TYPE = 'User Type'
BIRTH_YEAR = 'Birth Year'
GENDER = 'Gender'

# Set of mandatory columns
REQUIRED_COLUMNS = {START_TIME, END_TIME, TRIP_DURATION, START_STATION, END_STATION, USER_TYPE}

# Additional column names
DAY_OF_WEEK = 'Day of Week'
MONTH = 'Month'
TRIP = 'Trip'

# Mapping for user input
CITY_OPTIONS = {'1': 'chicago', '2': 'new york city', '3': 'washington'}
MONTH_OPTIONS = {'0': 'All', '1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June'}
DAY_OPTIONS = {'0': 'All', '1': 'Saturday', '2': 'Sunday', '3': 'Monday', '4': 'Tuesday', '5': 'Wednesday', '6': 'Thursday', '7': 'Friday'}

# File paths for city data
CITY_DATA_FILES = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}


def get_user_input(prompt, valid_inputs):
    """Helper function to get valid user input."""
    user_input = ''
    while user_input not in valid_inputs:
        user_input = input(prompt)
    return valid_inputs[user_input]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = get_user_input('Select city to analyze: 1- Chicago, 2- New York City 3- Washington ', CITY_OPTIONS)
    month = get_user_input('Select Month filter: 1- January, 2- February, 3- March, 4- April, 5- May, 6- June, or 0 no filter ', MONTH_OPTIONS)
    day = get_user_input('Select day filter: 1- Saturday, 2- Sunday, 3- Monday, 4- Tuesday, 5- Wednesday, 6- Thursday, 7- Friday, or 0 no filter ', DAY_OPTIONS)
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA_FILES[city])

    # Validate mandatory columns
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        print(f'Missing columns {missing_columns} in {CITY_DATA_FILES[city]} file')
        exit(1)

    # Convert start time to datetime
    df[START_TIME] = pd.to_datetime(df[START_TIME])
    df[MONTH] = df[START_TIME].dt.month
    df[DAY_OF_WEEK] = df[START_TIME].dt.day_name()

    # Filter by month if applicable
    if month != 'All':
        month = int(next(k for k, v in MONTH_OPTIONS.items() if v == month))
        df = df[df[MONTH] == month]

    # Filter by day if applicable
    if day != 'All':
        df = df[df[DAY_OF_WEEK] == day.title()]

    return df


def display_stats(df, column, description):
    """Helper function to display statistics."""
    common_values = df[column].value_counts()
    print(f'Most Common {description}: {common_values.index[0]} ({common_values.iloc[0]})')


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Args:
        df: Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    display_stats(df, MONTH, 'Month')
    display_stats(df, DAY_OF_WEEK, 'Day')
    common_hours = df[START_TIME].dt.hour.value_counts()
    print(f'Most Common Start Hour: {common_hours.index[0]} ({common_hours.iloc[0]})')

    print(TIME_TAKEN_MSG % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    display_stats(df, START_STATION, 'Start Station')
    display_stats(df, END_STATION, 'End Station')

    df[TRIP] = df[START_STATION] + ' <-> ' + df[END_STATION]
    display_stats(df, TRIP, 'Trip')

    print(TIME_TAKEN_MSG % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df[TRIP_DURATION].sum()
    average_duration = df[TRIP_DURATION].mean()
    print(f'Total travel time: {total_duration}')
    print(f'Average trip duration: {average_duration}')

    print(TIME_TAKEN_MSG % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    display_stats(df, USER_TYPE, 'User Type')

    if GENDER in df.columns:
        print('-' * 20)
        display_stats(df, GENDER, 'Gender')

    if BIRTH_YEAR in df.columns:
        print('-' * 20)
        earliest_year = df[BIRTH_YEAR].min()
        most_recent_year = df[BIRTH_YEAR].max()
        most_common_years = df[BIRTH_YEAR].value_counts()
        print(f'Earliest year: {earliest_year}')
        print(f'Most recent year: {most_recent_year}')
        print(f'Most common year: {most_common_years.index[0]} ({most_common_years.iloc[0]})')

    print(TIME_TAKEN_MSG % (time.time() - start_time))
    print('-' * 40)


def show_dataset_part(df):
    """Displays rows from data frame."""
    columns_to_display = list(df.columns.intersection(REQUIRED_COLUMNS))
    if GENDER in df.columns:
        columns_to_display.append(GENDER)
    if BIRTH_YEAR in df.columns:
        columns_to_display.append(BIRTH_YEAR)

    df = df[columns_to_display]
    pd.set_option('display.max_columns', None)
    row_count = 0
    while row_count < len(df):
        show_more = input('\nDo you want to check the next 5 rows of the dataset? Enter no/n to exit.\n')
        if show_more.lower() in ['no', 'n']:
            break
        print(df[row_count:row_count + 5])
        row_count += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_dataset_part(df)

        restart = input('\nWould you like to restart? Enter yes/y.\n')
        if restart.lower() not in ['yes', 'y']:
            break


if __name__ == '__main__':
    main()
