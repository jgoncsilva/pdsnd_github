from datetime import timedelta
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#So I need to answer the questions based on this code! 
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    check = False 

    while True:
        city = str(input("\nChoose which cities you want to explore (chicago, new york city, washington): ").strip().lower())
        if city not in ("chicago", "new york city", "washington"):
            print("\nSorry!That\'s not an option. Please try again")
            continue
        else:
            print("\nGood choice! It looks like you want to see data for: '{}' ".format(city.title()))
            check_option()
            break
    # get user input for month (all, january, february, ... , june)
    
    while True:
        month = str(input("From JANUARY to JUNE!Type the name of the month you want to filter ? (Use commas to list more than one):").strip().lower())
        
        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print("\nSorry! That\'s not an option. Please type in month name(or \"all\" to select all of them)")
            continue
        else:
            print("\nOK! Confirm that you have chosen to filter by: '{} ".format(month.title()))
            check_option()
        break
    
    while True:
        day = str(input("\nChoose a day of the week and write to filter by:").strip().lower())
            
        if day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday" , "sunday", "all"):
            print("Sorry. Please type in valid day (i.e. Saturday) or \"all\" of them to select everyday:")
            continue        
        else:
            print("\nOK! Confirm that you have chosen to filter by: '{}' ".format(day.title()))
            check_option()
            break
            
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("\nYou selected '{}' as city, '{}' as month, and '{}' as day. \nFiltering by your choices....".format(city.title(), month.title(), day.title()))
    print()
    print('-'*40)
    return city, month, day

def check_option(): 
    
    while True: 
        check = str(input(" Are yoy sure about this? Type 'yes' to continue and 'no' to restart: \n").strip().lower())#I Made this change by order of Udacity git-github project
        if check not in ("yes", "no"):
            print("\nSorry! That\'s not an option. Please try again")
            continue
        elif check == 'yes':
            break
        else: 
            get_filters()


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
    
    #columns for statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

    #filtering by month using the actual month for input
    if month != 'all':
        #Index Month list in chronological order/ int 
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        
        #Int Output
        month = months.index(month) + 1
        df = df[df['Month'] ==  month]

    #same idea for days
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        df = df[df['Day_of_Week'] == day.title()]
        
    return df




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    look_up = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May',
        '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}
    # display the most common month
    popular_month = df['Month'].mode()[0]
    month_in_string = look_up[str(popular_month)]
    print("1. Result = most common month: ", month_in_string)
    
    # display the most common day of week
    popular_day = df['Day_of_Week'].mode()[0]
    print("2. Result = most common day: {}".format(popular_day))

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print('3. Result = most common day of start hour :', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("1. Result = Most commonly used start station: '{}' ".format(start_station))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("2. Result = Most commonly used end station: '{}' ".format(end_station))

    # display most frequent combination of start station and end station trip
    
    final_start_end = df.groupby(['Start Station', 'End station']).size().sort_values(ascending = False).reset_index(name="counts")
    
    
    frequent_start_pair= final_start_end['Start station'][0]
    frequent_end_pair = final_start_end['End Station'][0]

    print("3. Result = The start station for most frequent combination is '{}' and the end station is '{}'".format(frequent_start_pair, frequent_end_pair))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    t2 = total_travel_time.astype('float64', copy=False)
    time_in_duration = timedelta(seconds=t2)
    
    print("Result = Total travel time in seconds: '{}' converts to '{}' in duration. ".format(total_travel_time, time_in_duration))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time is: '{}' seconds ".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df["User Type"].value_counts()
    print(count_user_type)

    # Display counts of gender
    if "Gender" in df.columns: 
        gender_count = df["Gender"].value_counts()
        nan_values = df["Gender"].isna().sum()
        
        print("\nCounts by Gender: \n{}\n \n*Attention: there were '{}' NuLL values for 'Gender' column".format(gender_count,nan_values))
    else:
        print("\nSorry! There\'s no column named 'Gender' in this dataset")    
    
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:

        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("\nEarliest birth year: '{}'. \nMost recent birth year: '{}'. \nMost common birth year: '{}'.".format(earliest, most_recent, most_common))

    else:
        print("\nSorry! There\'s no column named 'Birth Year' in this dataset")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Display 5 line of sorted raw data each time."""

    print("\nOkay!You opted to view raw data.")
    
    display_raw_input = input("\nWould you like to see individual raw data? Enter 'yes' or 'no'\n").strip().lower()    
    if display_raw_input in ("yes", "y"):
        i = 0
        
        #While loops used if the user wants to repeat the process
        while True:
            if (i + 5 > len(df.index) -1): #Use slicing lower included and upper excluded
                print(df.iloc[i:len(df.index), :]) #len(df.index) will not print upper 
                print("OMG! We are in the end of the rows. Sorry ")
                break
            print(df.iloc[i:i+5, :]) #Until is not out of limits, we keep moving printing the dataframe 
            i += 5
    
            more_five_input = input("\nKeep exploring! Want to see the next 5 lines? Type in 'yes' or 'no'\n").strip().lower()
            if more_five_input not in ("yes","y"):
                break #get out and finally break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
