import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city
    city = ""
    while city not in CITY_DATA:
        city = input("Please enter the name of the city to analyze (chicago, new york city, washington): ").lower()
        if city not in CITY_DATA:
            print("Invalid city name. Please try again.")

    # Get user input for month
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = ""
    while month not in months:
        month = input("Please enter the month to filter by (all, january, february, ... , june): ").lower()
        if month not in months:
            print("Invalid month name. Please try again.")

    # Get user input for day of the week
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ""
    while day not in days:
        day = input("Please enter the day of the week to filter by (all, monday, tuesday, ... sunday): ").lower()
        if day not in days:
            print("Invalid day name. Please try again.")

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
    # Get file name
    filename = CITY_DATA[city]
    # Load data file into a DataFrame
    df = pd.read_csv(filename)
    
    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Get name of the month from the 'Start Time' column
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    
    # Get the day of the week from the 'Start Time' column
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    
    # Filter the DataFrame by the input month
    if month != 'all':
        df = df[df['month'] == month]
     
    # Filter the DataFrame by the input day
    if day != 'all':
        df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # find the most popular month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', popular_month)

    # find the most popular day
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Start Day:', popular_day)
    
    ## get hour from the 'Start Time' column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # find the most popular start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular start station:", popular_start_station)

    # find the most popular end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most popular end station:", popular_end_station)

    # Create a new column 'Trip' combining start station and end station
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    
    # Display the most frequent combination of start station and end station trip
    popular_trip = df['Trip'].mode()[0]
    print("The most frequent combination of start station and end station trip:", popular_trip)
    
    print(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time:", total_travel_time)

    # mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types: {user_types}")

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("Counts of gender:", gender_counts)
    else:
        print("Gender information is not available for this dataset.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("Earliest year of birth:", earliest_birth_year)
        print("Most recent year of birth:", most_recent_birth_year)
        print("Most common year of birth:", most_common_birth_year)
    else:
        print("Birth year information is not available for this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        view_data = input("Would you like to view 5 rows of individual trip data? Enter 'yes' or 'no': ")
        if view_data.lower() == 'yes':
            start_loc = 0
            while view_data.lower() == 'yes':
                print(df.iloc[start_loc:start_loc+5])
                start_loc += 5
                view_data = input("Do you wish to continue? Enter 'yes' or 'no': ")
        else:
            print("\nYou will see all the data of bike sharing.")
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
