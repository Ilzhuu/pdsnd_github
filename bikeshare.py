import time
import pandas as pd
import numpy as np

# define a dictionary of cities and corresponding files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# define a list of months
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hi there! Let\'s explore some bikeshare data from USA !?')
    
    # get user input for city (chicago, new york city, washington). 
    while True:
        try:
            chosen_city = input('\nWhich city? Choose either Chicago, New York city or Washington by writing the city name!\n')
            verify = CITY_DATA[chosen_city.lower()]
            city = chosen_city.lower()
            print ('\nGot it! We\'ll consider', city.title())
            break
        except:
            print ('\nNope, try again!')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            chosen_month = input('\nChoose either entire period by typing ALL or any month from January to June! \n')
            if chosen_month.lower() in {'all', 'january', 'february', 'march', 'april', 'may', 'june'}:
                month = chosen_month.lower()   
                print ('\nGot it! We\'ll consider', month.title())                
                break
            else:
                print ('\nNope, try again!')
        except:
            print ('\nChoose month!')
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            chosen_day = input('\nWhich day? Choose either all days of the week by typing ALL or any day from Monday to Sunday!\n')
            if chosen_day.lower() in {'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturtday', 'sunday'}:
                day = chosen_day.lower()            
                print ('\nGot it! We\'ll consider', day.title())
                break
            else:
                print ('\nNope, try again!')
        except:
            print ('\nNope, try again!')
            
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

    # convert the start and end time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
        
        # use the index of the months list to get the corresponding int and crate new column in dataframe
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
    
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel of given dataframe."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most popular month is', MONTHS[(df['month'].mode()[0])-1].title(),'(if you did not choose exactly this month in your selection)')

    # display the most common day of week
    print('The most popular day of week is', df['day_of_week'].mode()[0],'(if you did not choose exactly this day in your selection)') 

    # find and display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most popular day start hour is', df['hour'].mode()[0]) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip of given dataframe."""

    print('\nCalculating The Most Popular Stations and Trip for your chosen time period and city...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used starting station is', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most commonly used finish station is', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' - ' + df['End Station']
    print('The most common route is', df['route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration on given dataframe."""

    print('\nCalculating Trip Duration for your chosen time period...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time in this city is', round((df['Trip Duration'].sum()/60/60),2), 'hours')

    # display mean travel time
    print('The mean travel time in this city is', round((df['Trip Duration'].mean()/60),2), 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users on given dataframe."""

    print('\nCalculating User Stats for your chosen time period...\n')
    start_time = time.time()

    # display counts of user types
    print('There are following numbers of each user category in this city:')
    print(df['User Type'].value_counts())

    # display counts of gender
    if 'Gender' in df:
        print('\nThe gender balance of bikeshare users in this city:')
        print(df['Gender'].value_counts())

    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('\nThe oldest registered user is born on', int(df['Birth Year'].min()))
        print('The youngest registered user is born on', int(df['Birth Year'].max()))
        print('The most typical birth year for users in this city is year', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Inquries user about raw data lookup."""
    
    ind = 0
    show_data = input('\nWhould you like to see data entries? Enter Yes or No!\n')
    cont = True
    
    # takes care of running the cycle until the df ends or user stops
    while cont:
        if show_data.lower() == 'yes':
            for i in range(ind, ind+5):
                # prints all columns for 5 rows
                print(df.iloc[i,:])
                # ensures the end of df has not been reached
                if i+1 == len(df):
                    print('This is it - no more entries!')
                    # defing last loop
                    cont = False
                    break    
            # saves the current row if user chooses to continue
            ind = i+1 
            if cont:
                keep_going = input('\nWhould you like to see more data entries? Enter Yes or No!\n')
                if keep_going.lower() == 'yes':
                    continue
                else:
                    break
        else:
            break

def main():
    """Runs the main cycle of interactivity with the user."""

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)       
        raw_data(df)              

        restart = input('\nWould you like to restart with different settings (city, time)? Enter Yes or No!\n')
        if restart.lower() != 'yes':
            print ('\nSee you next time! Bye!')
            break


if __name__ == "__main__":
	main()
