import time

import pandas as pd

THIS_TOOK_S_SECONDS_PREFIX = '\nThis took %s seconds.'

# main columns names
START_TIME_COL = 'Start Time'
END_TIME_COL = 'End Time'
TRIP_DURATION_COL = 'Trip Duration'
START_STATION_COL = 'Start Station'
END_STATION_COL = 'End Station'
USER_TYPE_COL = 'User Type'
BIRTH_YEAR_COL = 'Birth Year'
GENDER_COL = 'Gender'

MANDATORY_COL_SET = {
    START_TIME_COL, END_TIME_COL, TRIP_DURATION_COL, START_STATION_COL, END_STATION_COL, USER_TYPE_COL
}

# added columns names
DAY_OF_WEEK_COL = 'Day of Week'
MONTH_COL = 'Month'
TRIP_COL = 'Trip'

CITY_INPUT_MAP = {'1': 'chicago', '2': 'new york city', '3': 'washington'}
MONTH_INPUT_MAP = {'0': 'All', '1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June'}
WEEK_DAY_INPUT_MAP = {'0': 'All', '1': 'Saturday', '2': 'Sunday', '3': 'Monday', '4': 'Tuesday', '5': 'Wednesday', '6': 'Thursday', '7': 'Friday'}

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}


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
    city = get_user_input('Select city to analyze: 1- Chicago, 2- New York City 3- Washington ', CITY_INPUT_MAP)
    month = get_user_input('Select Month filter: 1- January, 2- February, 3- March, 4- April, 5- May, 6- June, or 0 no filter ', MONTH_INPUT_MAP)
    day = get_user_input('Select day filter: 1- Saturday, 2- Sunday, 3- Monday, 4- Tuesday, 5- Wednesday, 6- Thursday, 7- Friday, or 0 no filter ', WEEK_DAY_INPUT_MAP)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # validate mandatory columns
    for col in MANDATORY_COL_SET:
        if col not in df.columns:
            print(f'Missing column \'{col}\' in \'{CITY_DATA[city]}\' file')
            exit(1)

    # convert the Start Time column to datetime
    df[START_TIME_COL] = pd.to_datetime(df[START_TIME_COL])

    # extract month and day of week from Start Time to create new columns
    df[MONTH_COL] = df[START_TIME_COL].dt.month
    df[DAY_OF_WEEK_COL] = df[START_TIME_COL].dt.day_name()

    # filter by month if applicable
    if month != 'All':
        # use the key of the months map to get the corresponding int
        month = int(next((k for k, v in MONTH_INPUT_MAP.items() if v == month), None))

        # filter by month to create the new dataframe
        df = df[df[MONTH_COL] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df[DAY_OF_WEEK_COL] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_months = df[MONTH_COL].value_counts()
    print(f'Most commonly used month: {MONTH_INPUT_MAP[str(common_months.index[0])]} ({common_months.iloc[0]})')

    # display the most common day of week
    common_days = df[DAY_OF_WEEK_COL].value_counts()
    print(f'Most Common Day: {common_days.index[0]} ({common_days.iloc[0]})')

    # display the most common start hour
    common_hours = df[START_TIME_COL].dt.hour.value_counts()
    print(f'Most Common Start Hour: {common_hours.index[0]} ({common_hours.iloc[0]})')

    print(THIS_TOOK_S_SECONDS_PREFIX % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_starts = df[START_STATION_COL].value_counts()
    print(f'Most commonly used Start Station: {common_starts.index[0]} ({common_starts.iloc[0]})')

    # display most commonly used end station
    common_ends = df[END_STATION_COL].value_counts()
    print(f'Most commonly used End Station: {common_ends.index[0]} ({common_ends.iloc[0]})')

    # display most frequent combination of start station and end station trip
    df[TRIP_COL] = df[START_STATION_COL] + ' <-> ' + df[END_STATION_COL]
    common_trips = df[TRIP_COL].value_counts()
    print(f'Most frequent Trip: {common_trips.index[0]} ({common_trips.iloc[0]})')

    print(THIS_TOOK_S_SECONDS_PREFIX % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df[TRIP_DURATION_COL].sum()
    print('Total travel time: ', total_time)

    # display mean travel time
    mean_duration = df[TRIP_DURATION_COL].mean()
    print('Average trip duration: ', mean_duration)

    print(THIS_TOOK_S_SECONDS_PREFIX % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df[USER_TYPE_COL].value_counts()
    for count in count_user_types.index:
        print(count, count_user_types[count])

    # Display counts of gender
    if GENDER_COL in df.columns:
        print('-' * 20)
        count_gender = df[GENDER_COL].value_counts()
        for count in count_gender.index:
            print(count, count_gender[count])

    # Display earliest, most recent, and most common year of birth
    if BIRTH_YEAR_COL in df.columns:
        print('-' * 20)
        earliest_date = df[BIRTH_YEAR_COL].min()
        print('Earliest date:', earliest_date)
        most_recent_date = df[BIRTH_YEAR_COL].max()
        print('Most recent date:', most_recent_date)
        most_common_dates = df[BIRTH_YEAR_COL].value_counts()
        print(f'Most common date: {most_common_dates.index[0]} ({most_common_dates.iloc[0]})')

    print(THIS_TOOK_S_SECONDS_PREFIX % (time.time() - start_time))
    print('-' * 40)


def show_dataset_part(df):
    """Displays rows from data frame."""

    cols = list(df.columns.intersection(MANDATORY_COL_SET))
    if GENDER_COL in df.columns:
        cols.append(GENDER_COL)
    if BIRTH_YEAR_COL in df.columns:
        cols.append(BIRTH_YEAR_COL)

    df = df[cols]
    # Display first 5 rows
    show = input('\nDo you want to check the first 5 rows of the dataset related to the chosen city? Enter no/n to exit.\n')
    if show.lower() in ['no', 'n']:
        return
    # Display full columns
    pd.set_option('display.max_columns', None)
    print(df.head(5))

    # Display next 5 rows
    count = 5
    while count < len(df):
        show = input('\nDo you want to check another 5 rows of the dataset? Enter no/n to exit.\n')
        if show.lower() in ['no', 'n']:
            break
        print(df[count:count + 5])
        count += 5


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
