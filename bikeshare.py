import time as time_
import pandas as pd
import numpy as np
import datetime as dt

pd.set_option("display.max_rows", None, "display.max_columns", None)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze and checks for valid input.
    
    Args:
        input 1 (string) = city 
        input 2 (string) = month
        input 3 (string) = day

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    print('Hello! I\'m fabesview. Let\'s explore some US bikeshare data!\n With this program you will be able to retrieve descriptive statistics for different cities and timeframes.')
   
    # Get user input for city (chicago, new york city, washington). Uses a while loop to handle invalid inputs
    
    print('We can explore data for the following cities: Chicago, New York City, Washington.')
    city = input('Please input the name of the city you want to explore data from: ').lower()
    
    while city not in CITY_DATA.keys():
        print('The city name you provided is invalid.')
        city = input('Please input the name of the city you want to explore data from: ').lower()

    # Get user input for month (all, january, february, ... , june)
   
    print('\nYou can explore data for "all" months or for individual months from "January" to "June"')
    month = input('Please indicate the month you want to explore data from: ').lower()
    
    while month != 'all' and month not in months:
        print('The month you provided is invalid.')
        month = input('Please indicate the month you want to explore data from: ').lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
                  
    print('\nYou can explore data for "all" weekdays or for individual days from "Monday" to "Sunday"')
    day = input('Please indicate the day you want to explore data from: ').lower()
    
    while day != 'all' and day not in days:
        print('The day you provided is invalid.')
        day = input('Please indicate the day you want to explore data from: ').lower()

    # Added a check in order for the user to see what inputs he/she provided 
    print('\nYour input was city = {}, month = {}, day = {}\n'.format(city, month, day))
    check = input('Is that correct [Yes/No]? ').lower()
    
    # This if statement checks if user input was "No" and in that case exits the program after printing that program is exited.
    if check.lower() == 'no':
        print('Please restart the script to enter other inputs. Exiting program now...')
        exit() 

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
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
   
    Args:
        parameter 1 (df) = dataframe to be used
    
    Returns:
        None
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time_.time()

    # Display the most common month
    
    most_month = df['month'].mode()[0]
    print('The most popular month is: {}'.format(most_month))

    # Display the most common day of week
    
    most_day = df['day_of_week'].mode()[0]
    print('The most popular day of the week is: {}'.format(most_day))
    
    # Create column with hour from Start Time df
    df['hour'] = df['Start Time'].dt.hour
    
    # Display the most common start hour
    most_hour = df['hour'].mode()[0]
    print('The most common start hour is: {}'.format(most_hour)) 

    
    print("\nThis took %s seconds." % (time_.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    Args:
        parameter 1 (df) = dataframe to be used
    
    Returns:
        None
        
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time_.time()

    # Display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print('The most popular start station is: {}'.format(most_start_station))

    # Display most commonly used end station

    most_end_station = df['End Station'].mode()[0]
    print('The most popular end station is: {}'.format(most_end_station))
    
    # Create column with hour from Start Time df
    df['Start End Comb'] = df['Start Station'].str.cat(df['End Station'], sep=' - ')
    
    # Display most frequent combination of start station and end station trip
    most_startend_combo = df['Start End Comb'].mode()[0]
    print('The most frequent combination of start/end station for trips is: {}'.format(most_startend_combo))                   

    print("\nThis took %s seconds." % (time_.time() - start_time))
    print('-'*40)
    
def dhms_from_seconds(seconds):
    """Calculates time in terms of day, hours, minutes and seconds based on input seconds.
    
    Args:
        parameter 1 (seconds) = seconds (int)
       
    Returns:
        (int) days
        (int) hours
        (int) minutes
        (int) seconds
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days, hours, minutes, seconds)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    Args:
        parameter 1 (df) = dataframe to be used
       
    Returns:
        None
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time_.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # Access dhms_from_seconds function in order to convert seconds into days/hours/minutes/seconds
    time_conversion = dhms_from_seconds(int(total_travel_time))
    
    print('The total travel time is {} days, {} hours, {} minutes and {} seconds (days:hours:minutes:seconds)'.format(time_conversion[0], time_conversion[1], time_conversion[2], time_conversion[3]))

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    # Access dhms_from_seconds function in order to convert seconds into days/hours/minutes/seconds
    time_conversion = dhms_from_seconds(int(mean_travel_time))
    
    print('The mean travel time is {} hours, {} minutes and {} seconds (hours:minutes:seconds)'.format(time_conversion[1], time_conversion[2], time_conversion[3]))
    
    print("\nThis took %s seconds." % (time_.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    
    Args:
        parameter 1 (df) = dataframe to be used
    
    Returns:
        None
    
    """

    print('\nCalculating User Stats...\n')
    start_time = time_.time()

    # Display counts of user types
    
    user_type_count = df[['User Type']].groupby(['User Type']).size().reset_index(name='counts')
    print(user_type_count)
    print()

    # Display counts of gender
    
    gender_count = df[['Gender']].groupby(['Gender']).size().reset_index(name='counts')
    print(gender_count)
    print()

    # Display earliest, most recent, and most common year of birth

    earliest_yob = int(df['Birth Year'].min())
    most_recent_yob = int(df['Birth Year'].max())
    most_common_yob = int(df['Birth Year'].mode()[0])
    
    
    print('The oldest user was born in {}'.format(earliest_yob)) 
    print('The youngest user was born in {}'.format(most_recent_yob)) 
    print('The most common year of birth is {}'.format(most_common_yob)) 
    

    print("\nThis took %s seconds." % (time_.time() - start_time))
    print('-'*40)


def display_rawdata(df):
    """Displays raw data for 5 rows at a time if the user requests to see data.
    
    Args:
        parameter 1 (df) = dataframe to be used
    
    Returns:
        None
    
    """
    df_base = df[['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station']]
    display_count = 0
    check_response = ['yes', 'no']
    data_request = ''
    
    # Checks whether input is in check_response list and whether answer is 'yes' or asks for new input if input was invalid
    while data_request not in check_response:
        data_request = input('Do you want to see raw data? [Yes] or [No]: ').lower()
        if data_request == 'yes':
            print(df_base.head())
        elif data_request not in check_response:
            print('The input you provided could not be processed.')
            data_request = input('\nDo you want to see raw data [Yes] or [No]: ').lower()
    
    # Loop in order to show susequent 5 rows if user wants to display those
    while data_request == 'yes':
        data_request = input('\nDo you want to see more raw data? [Yes] or [No]: ').lower()
        display_count += 5
        if data_request == 'yes':
            print(df_base[display_count:display_count+5])
        elif data_request != 'yes':
            break
    print('-'*40)
                                          
          
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_rawdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            

if __name__ == "__main__":
	main()
