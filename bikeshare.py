import csv
import time
from datetime import datetime


# ## Filenames
# chicago = 'chicago.csv'
# new_york_city = 'new_york_city.csv'
# washington = 'washington.csv'


# Lists
city_list = ["chicago", "new_york_city", "washington"]
time_period_list = ["month", "day", "none"]
month_list = ["January", "February", "March", "April", "May", "June"]
day_list = ["0", "1", "2", "3", "4", "5", "6"]


def get_city():
    '''Asks the user for a city and returns the filename for
    that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''

    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago'
                 ', New York City, or Washington?\n')
    city = city.replace(" ", "_").lower()
    while city not in city_list:
        print("Not an option. Please choose from the 3 options")
        city = input('Would you like to see data for Chicago, New York City'
                     ', or Washington?\n')
        city = city.replace(" ", "_").lower()
    return city + ".csv"


def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

    Args:
        none.
    Returns:
        (str) Received time period from month, day, or none.
    '''

    time_period = input('\nWould you like to filter the data '
                        'by month, day, or not at'
                        ' all? Type "none" for no time filter.\n')
    time_period = time_period.lower()
    while time_period not in time_period_list:
        print("Not an option. Please choose from the 3 options")
        time_period = input(
            '\nWould you like to filter the data by month, day, or not at'
            ' all? Type "none" for no time filter.\n')
        time_period = time_period.lower()
    return time_period


def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        (int) User-provided month index from Jan(1)-June(6).
    '''
    month = input('\nWhich month? January, February,'
                  ' March, April, May, or June?\n')
    month = month.title()
    while month not in month_list:
        print("Not an option. Please choose from the 6 months")
        month = input('\nWhich month? January, '
                      'February, March, April, May, or June?\n')
        month = month.title()
    index = 0
    for i in range(len(month_list)):
        if month == month_list[i]:
            index = i + 1
    return index


def get_day():
    '''Asks the user for a day and returns the specified day.

    Args:
        none.
    Returns:
        (int) User-provided day from Monday(0)- Sunday(6).
    '''
    day = input('\nWhich day? Please type your response as an integer.'
                '\nFor example, Monday is 0 and Sunday is 6')
    while day not in day_list:
        print("Not an option. Please choose from the 6 days")
        day = input('\nWhich day? Please type your response as an integer.'
                    '\nFor example, Monday is 0 and Sunday is 6')
    return int(day)


def popular_month(time_period, reader):
    '''Prints the most popular month for a given time period.

    Args:
        (list) Time period for city data.
        (csv) CSV reader.
    Returns:
        none.
    '''

    popular = dict()
    for x in range(1, 7):
        popular[x] = 0
    for read in reader:
        if time_period[0] == "day" and time_period[1] != datetime.strptime(
                read['Start Time'],
                '%Y-%m-%d %H:%M:%S').weekday():
            continue
        a = datetime.strptime(read['Start Time'], "%Y-%m-%d %H:%M:%S").month
        popular[a] += 1
    ans = month_list[max(popular, key=popular.get) - 1]
    print("Popular month: " + ans)


def popular_day(time_period, reader):
    '''Prints the most popular weekday for the given time period.

    Args:
         (list) Time period for city data.
         (csv) CSV Reader.
    Returns:
         none.
    '''
    popular = dict()
    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
               "Saturday", "Sunday"]
    for x in range(0, 7):
        popular[x] = 0
    for read in reader:
        if time_period[0] == "month":
            if datetime.strptime(read['Start Time'],
                                 "%Y-%m-%d %H:%M:%S").month != time_period[1]:
                continue
        a = datetime.strptime(read['Start Time'], "%Y-%m-%d %H:%M:%S").weekday()
        popular[a] += 1
    ans = day_list[max(popular, key=popular.get)]
    print("Popular weekday: {}".format(weekday[int(ans)]))


def popular_hour(time_period, reader):
    '''Prints the most popular hour for the given time period.

    Args:
         (list) Time period for city data.
         (csv) CSV Reader.
    Returns:
         none.
    '''
    popular = dict()
    for x in range(0, 24):
        popular[x] = 0
    for read in reader:
        if time_period[0] == "month":
            if datetime.strptime(read['Start Time'],
                                 "%Y-%m-%d %H:%M:%S").month != time_period[1]:
                continue
        if time_period[0] == "day" and time_period[1] != datetime.strptime(
                read['Start Time'],
                '%Y-%m-%d %H:%M:%S').weekday():
            continue
        a = datetime.strptime(read['Start Time'], "%Y-%m-%d %H:%M:%S").hour
        popular[a] += 1

    ans = max(popular, key=popular.get)

    print(str(ans) + ":00")


def trip_duration(time_period, reader):
    '''Prints the max trip duration and average trip duration.

    Args:
         (list) Time period for city data.
         (csv) CSV Reader.
    Returns:
         none.
    '''
    dur = []
    for read in reader:
        # 2017-01-01 00:07:57
        if time_period[0] == "month":
            if datetime.strptime(read['Start Time'],
                                 "%Y-%m-%d %H:%M:%S").month != time_period[1]:
                continue
        if time_period[0] == "day" and time_period[1] != datetime.strptime(
                read['Start Time'],
                '%Y-%m-%d %H:%M:%S').weekday():
            continue
        start = datetime.strptime(read['Start Time'], "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(read['End Time'], "%Y-%m-%d %H:%M:%S")
        duration = end - start
        dur.append(duration.total_seconds())

    ans1 = int(max(dur) / 60)
    ans2 = int(sum(dur) / len(dur) / 60)

    print("Max Duration: {} minutes \n"
          "Average Duration: {} minutes".format(ans1, ans2))


def popular_stations(time_period, reader):
    '''Prints the most popular start and end station.

    Args:
         (list) Time period for city data.
         (csv) CSV Reader.
    Returns:
         none.
    '''
    popular_start = dict()
    popular_end = dict()
    for read in reader:
        if time_period[0] == "month":
            if datetime.strptime(read['Start Time'],
                                 "%Y-%m-%d %H:%M:%S").month != time_period[1]:
                continue
        if time_period[0] == "day" and time_period[1] != datetime.strptime(
                read['Start Time'],
                '%Y-%m-%d %H:%M:%S').weekday():
            continue
        a = read['Start Station']
        if a not in popular_start:
            popular_start[a] = 1
        else:
            popular_start[a] += 1
        a = read['End Station']
        if a not in popular_end:
            popular_end[a] = 1
        else:
            popular_end[a] += 1
    start_ans = max(popular_start, key=popular_start.get)
    end_ans = max(popular_end, key=popular_end.get)
    final_ans = "Popular Start Station: {} \nPopular End Station: {}".format(
        start_ans, end_ans)
    print(final_ans)


def popular_trip(time_period, reader):
    '''Prints the most popular trip made with bike trip.

    Args:
         (list) Time period for city data.
         (csv) CSV Reader.
    Returns:
         none.
    '''
    popular = dict()

    for read in reader:
        if time_period[0] == "month":
            if datetime.strptime(read['Start Time'],
                                 "%Y-%m-%d %H:%M:%S").month != time_period[1]:
                continue
        if time_period[0] == "day" and time_period[1] != datetime.strptime(
                read['Start Time'],
                '%Y-%m-%d %H:%M:%S').weekday():
            continue
        a = read['Start Station']
        a += " to " + read['End Station']
        if a not in popular:
            popular[a] = 1
        else:
            popular[a] += 1
    ans = max(popular, key=popular.get)

    print("Popular Trip: {}".format(ans))


def users(time_period, reader):
    '''Prints the user count for each user group. Excludes N/A from count

    Args:
         (list) Time period for city data.
         (csv) CSV Reader.
    Returns:
         none.
    '''
    group = dict()

    for read in reader:
        if time_period[0] == "month":
            if datetime.strptime(read['Start Time'],
                                 "%Y-%m-%d %H:%M:%S").month != time_period[1]:
                continue
        if time_period[0] == "day" and time_period[1] != datetime.strptime(
                read['Start Time'],
                '%Y-%m-%d %H:%M:%S').weekday():
            continue
        a = read['User Type']
        if a not in group:
            group[a] = 1
        else:
            group[a] += 1
    for user in group:
        print("Count for {}: {}".format(user, group[user]))


def gender(time_period, reader):
    '''Prints the gender count for each gender group. Excludes N/A from count

    Args:
         (list) Time period for city data.
         (csv) CSV Reader.
    Returns:
         none.
    '''
    gen = dict()

    for read in reader:
        if time_period[0] == "month":
            if datetime.strptime(read['Start Time'],
                                 "%Y-%m-%d %H:%M:%S").month != time_period[1]:
                continue
        if time_period[0] == "day" and time_period[1] != datetime.strptime(
                read['Start Time'],
                '%Y-%m-%d %H:%M:%S').weekday():
            continue
        a = read['Gender']
        if a == "":
            continue
        if a not in gen:
            gen[a] = 1
        else:
            gen[a] += 1
    for user in gen:
        print("Count for Gender {}: {}".format(user, gen[user]))


def birth_years(time_period, reader):
    '''Prints the youngest age, oldest age, and most frequent age group

    Args:
         (list) Time period for city data.
         (csv) CSV Reader.
    Returns:
         none.
    '''
    year = dict()

    for read in reader:
        if time_period[0] == "month":
            if datetime.strptime(read['Start Time'],
                                 "%Y-%m-%d %H:%M:%S").month != time_period[1]:
                continue
        if time_period[0] == "day" and time_period[1] != datetime.strptime(
                read['Start Time'],
                '%Y-%m-%d %H:%M:%S').weekday():
            continue
        a = read['Birth Year']
        if a == "":
            continue
        if a not in year:
            year[a] = 1
        else:
            year[a] += 1
    current = datetime.now().year
    max_age = current - int(float(min(year)))
    min_age = current - int(float(max(year)))
    pop_age = current - int(float(max(year, key=year.get)))
    print("Max Age: {}\nMin Age: {}\nMost Frequent Age: {}".format(max_age,
                                                                   min_age,
                                                                   pop_age))


def display_data(time_period, reader):
    '''Displays five lines of data if the user specifies that
    they would like to.After displaying five lines, ask the user
    if they would like to see five more,continuing asking until they say stop.


    Args:
         (list) Time period for city data.
         (csv) CSV Reader.
    Returns:
         none.
    '''

    display = input('\nWould you like to view individual trip data?'
                    ' Type \'yes\' or \'no\'.\n')
    if display.lower() != "yes":
        return ()

    count = 1
    for read in reader:
        if time_period[0] == "month":
            if datetime.strptime(read['Start Time'],
                                 "%Y-%m-%d %H:%M:%S").month != time_period[1]:
                continue
        if time_period[0] == "day" and time_period[1] != datetime.strptime(
                read['Start Time'],
                '%Y-%m-%d %H:%M:%S').weekday():
            continue
        for cat in read:
            if read[cat] == "":
                read[cat] = "N/A"
            print(cat + ": " + read[cat] + " ", end=" ")
        print("")
        if count % 5 == 0:
            more = input('\nWould you like to see 5 more? '
                         'Type \'yes\' or \'no\'.\n')
            if more == "no":
                break
        count += 1


def statistics():
    '''Calculates and prints out the descriptive statistics about a city
    and time period specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    # Filter by time period (month, day, none)
    time_period = [get_time_period()]
    if time_period[0] == "month":
        time_period.append(get_month())
    elif time_period[0] == "day":
        time_period.append(get_day())

    print('Calculating the first statistic...')
    csvfile = open(city, newline='')
    reader = csv.DictReader(csvfile)

    # What is the most popular month for start time?
    if time_period[0] == 'none':
        start_time = time.time()

        popular_month(time_period, reader)
        csvfile.seek(0)
        reader.__init__(csvfile, delimiter=",")

        print("That took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")

    # What is the most popular weekday for start time?
    if time_period[0] == 'none' or time_period[0] == 'month':
        start_time = time.time()

        popular_day(time_period, reader)
        csvfile.seek(0)
        reader.__init__(csvfile, delimiter=",")

        print("That took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")

    start_time = time.time()

    # What is the most popular hour of day for start time?

    popular_hour(time_period, reader)
    csvfile.seek(0)
    reader.__init__(csvfile, delimiter=",")

    print("That took %s seconds." % (time.time() - start_time))

    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    trip_duration(time_period, reader)
    csvfile.seek(0)
    reader.__init__(csvfile, delimiter=",")

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    popular_stations(time_period, reader)
    csvfile.seek(0)
    reader.__init__(csvfile, delimiter=",")

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    popular_trip(time_period, reader)
    csvfile.seek(0)
    reader.__init__(csvfile, delimiter=",")

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the counts of each user type?
    users(time_period, reader)
    csvfile.seek(0)
    reader.__init__(csvfile, delimiter=",")

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the counts of gender?
    gender(time_period, reader)
    csvfile.seek(0)
    reader.__init__(csvfile, delimiter=",")

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the earliest, most recent, and most popular birth years?
    birth_years(time_period, reader)
    csvfile.seek(0)
    reader.__init__(csvfile, delimiter=",")

    print("That took %s seconds." % (time.time() - start_time))

    # Display five lines of data at a time if user wants to.
    display_data(time_period, reader)
    csvfile.close()

    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        statistics()


if __name__ == "__main__":
    statistics()
