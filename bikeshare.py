import numpy as np 
import pandas as pd 
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ["January","February","March","April","May","June"]
days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]


def get_filters():
    '''
    this functions aim to get filters from user to perform analysis
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    '''
    print('-'*80)
    print("Hello there! Welcom to Bikeshare Analysis.\nThis analysis is only for Chicago, New York City and Washington.")
    city = ""
    month = ""
    day = ""
    while city == "":
        try:
            answer_1 = input("kindly enter city: ").lower()
            if answer_1 in CITY_DATA:
                city = answer_1
            else:
                print("kindly choose a city from Chicago, New York City and Washington only")
        except:
            print("invalid entry. kindly choose a city from Chicago, New York City and Washington only")
            break
    while month == "":
        try:
            answer_2 = input("kindly choose month (from January to June) or enter 'all': ").capitalize()
            if answer_2 in months:
                month = answer_2
            elif answer_2 == "All":
                month = answer_2
            else:
                print("kindly choose month (from January to June) or enter 'all'")
        except:
            print("invalid entry. kindly choose month (from January to June) or enter 'all")
            break
    while day == "":
        try:
            answer_3 = input("kindly choose day (from Sunday to Saturday) or enter 'all': ").capitalize()
            if answer_3 in days:
                    day = answer_3                
            elif answer_3 == "All":
                day = answer_3
            else:
                print("kindly choose day (from Sunday to Saturday) or enter 'all'")
        except:
            print("invalid entry. kindly choose day (from Sunday to Saturday) or enter 'all")
            break
    print('-'*80)
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
    month_num = [x for x in range(1,7)]
    day_num = [x for x in range(7)]

    months_dict = dict(zip(months, month_num))
    days_dict = dict(zip(days, day_num))
    
    df = pd.read_csv("{}".format(CITY_DATA[city]))
    df.drop(df.columns[0], axis = 1, inplace=True)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df['month'] = df['Start Time'].dt.month
    df['week day'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    if month in months_dict:
        df = df.loc[df['month'] == months_dict[month]]
    if day in days_dict:
        df = df.loc[df['week day'] == days_dict[day]]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    if month != "All":
        print("The current data is only for {}".format(month))
    else:
        count_month = [0]*7 #create a list for months as placeholder. First index is ignored
        for i in df["month"]:
            for j in range(1,len(months)+1):
                if i == j:
                    count_month[j] +=1 #count trip per month
        max_val = count_month.index(max(count_month))
        top_month = months[max_val-1]
        print('Most Popular Month:', top_month)

    # display the most common day of week
    if day != "All":
        print("The current data is only for {}".format(day))
    else:
        count_weekday = [0]*8 #create a list for days as placeholder. First index is ignored
        for i in df["week day"]:
            for j in range(1,len(days)+1):
                if i == j:
                    count_weekday[j] +=1 #count trip per day
        max_val = count_weekday.index(max(count_weekday))
        top_weekday = days[max_val-1]
        print('Most Popular Weekday:', top_weekday)

    # display the most common  hour
    count_hour = [0]*24 #create a list for hours as placeholder. First index not ignored
    for i in df["hour"]:
        for j in range(len(count_hour)):
            if i == j:
                count_hour[j] +=1 # count trip per hour
    max_val = count_hour.index(max(count_hour))
    top_hour = max_val 
    print('Most Popular Hour:', top_hour)
   
    print("\nThis took %s seconds." % (round(time.time() - start_time,2)))
    print('-'*80)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_st = df["Start Station"].mode()[0]
    print("Most Popular Start Station: {}".format(start_st))
    # display most commonly used end station
    end_st = df["End Station"].mode()[0]
    print("Most Popular End Station: {}".format(end_st))

    # display most frequent combination of start station and end station trip
    freq = df.groupby(['Start Station','End Station']).size().nlargest(1).to_string()
    print("Most Frequent Combination Of Start Station And End Station Trip:\n{}".format(freq))
    
    print("\nThis took %s seconds." % (round(time.time() - start_time,2)))
    print('-'*80)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time Trip Duration
    total = round(df["Trip Duration"].sum()/3600,2)
    print("Total Trip Duration is: {} hours".format(total))
    # display mean travel time
    avg = round(df["Trip Duration"].mean()/60,2)
    print("average Trip Duration is: {} minutes".format(avg))

    print("\nThis took %s seconds." % (round(time.time() - start_time,2)))
    print('-'*80)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_num = df["User Type"].value_counts().to_string()
    print("The Count of User Types is:\n{}".format(user_num))
    # Display counts of gender
    if city == "washington":
        print("No Gender Data Available for Washington!")
    else:
        gender_num = df["Gender"].value_counts().to_string()
        print("The Count of Gender is:\n{}".format(gender_num))

    # Display earliest, most recent, and most common year of birth 
    if city == "washington":
        print("No Birthday Data Available for Washington!")
    else:
        earliest = int(df["Birth Year"].min())
        print("The Earlist Year of Birth is: {}".format(earliest))
        recent = int(df["Birth Year"].max())
        print("The Most Recent Year of Birth is: {}".format(recent))
        common = df["Birth Year"].mode().to_string()
        print("The Most common Year of Birth is:\n{}".format(common))

    print("\nThis took %s seconds." % (round(time.time() - start_time,2)))
    print('-'*80)


def main():
    while True:
        city_1, month_1, day_1 = get_filters()
        df = load_data(city_1, month_1, day_1)
        print(df.head())
        x = 5
        y = 10
        while True:
            answer_0 = input("Would You Like to Dispaly More Raw Data? (yes/no)")
            if answer_0 == "yes":
                print(df.iloc[x:y])
                x += 5
                y += 5
            else:
                break
        print('#'*80)
        answer_1 = input("Would you like to see stats regarding Time? (yes/no)")
        if answer_1.lower() == "yes":
            time_stats(df, month_1, day_1)
        else:
            print("Moving to next option >>>>>>>>")
        answer_2 = input("Would you like to see stats regarding Stations? (yes/no)")
        if answer_2.lower() == "yes":
            station_stats(df)
        else:
            print("Moving to next option >>>>>>>>")
        answer_3 = input("Would you like to see stats regarding Trip Duration? (yes/no)")
        if answer_3.lower() == "yes":
            trip_duration_stats(df)
        else:
            print("Moving to next option >>>>>>>>")
        answer_4 = input("Would you like to see stats regarding User? (yes/no)")
        if answer_4.lower() == "yes":
            user_stats(df,city_1)
        else:
            print("Moving to next option >>>>>>>>")
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

