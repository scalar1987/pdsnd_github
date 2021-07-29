import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day
    Zto an   Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    cities = ['chicago', 'new york city', 'washington']
    city = input('\nEnter city. \nChoose either chicago, new york city or washington?:  ').lower()
    while city not in cities:
        city = input('\nPlease try again. You should choose either chicago, new york city or washington : ').lower()
        if city in cities:
            print("\nWe are working with {} data".format(city.upper()))
            break
    else:
        print("Ops!, nearly right, try again")

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('\nEnter month:  ').lower()
    while month not in months:
        month = input('\nPlease try again. \nYou should choose either january, february, march, april, may, june or all for no month filter : ').lower()
        if month in months:
            print("\nWe are working with {} data".format(month.upper()))
            break
    else:
        print("Ops!, nearly right, try again")

    days = ['all', 'monday', 'tuesday', 'wednesday', 'thirsday', 'friday', 'saturday', 'sunday']
    day = input('\n Enter day:  ').lower()
    while day not in days:
        day = input('\nPlease try again. \nYou should choose either monday, teusday, wednesday, thirsday, friday, saturday, sunday or all for no month filter : ').lower()
        if day in days:
            print("\nWe are working with {} data".format(day.upper()))
            break
    else:
        print("Ops!, nearly right, try again")

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':

        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most common month:', popular_month)

    popular_weekday = df['day_of_week'].mode()[0]
    print('Most common day of week:', popular_weekday)

    popular_hour = df['hour'].mode()[0]
    print('Most common hour of day:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start = df['Start Station'].mode()[0]
    print('Most commonly used start station:', popular_start)

    popular_end = df['End Station'].mode()[0]
    print('Most commonly used end station:', popular_end)

    df['station_combination'] = df['Start Station'] + ':' + df['End Station']
    popular_station_combination = df['station_combination'].mode()[0]
    print('Most frequent combination of stations:', popular_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    sum_travel_time = df['Trip Duration'].sum() / 60 / 60
    print('total travel time:', sum_travel_time, 'hours')

    avg_travel_time = df['Trip Duration'].mean() / 60
    print('average travel time:', avg_travel_time, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts().to_frame()
    print('User types:', user_types)

    if 'Gender' in df.columns:
       gender_count = df['Gender'].value_counts().to_frame()
       print('Gender count:', gender_count)
    else:
       print("No gender data to share.")

    if 'Birth Year' in df.columns:
        most_recent_birthyear = df['Birth Year'].max()
        print('Most recent year of birth:', int(most_recent_birthyear))
        earliest_birthyear = df['Birth Year'].min()
        print('Earliest year of birth:', int(earliest_birthyear))
        most_common_birthyear = df['Birth Year'].mode()[0]
        print('Most common year of birth:', int(most_common_birthyear))
    else:
        print("No birth year data to share.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        record_no = 5
        while True:
            user_input = input('Would you like to see 5 rows of data data?\nPlease select yes or no: ').lower()
            if (user_input == 'yes'):
                print(df.iloc[record_no],'\n')
                record_no+=5
                continue
            elif (user_input == 'no'):
                break

if __name__ == "__main__":
	main()
