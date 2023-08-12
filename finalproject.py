"""

    CS051P Lab Assignments: Final Project

    Author: Bailey Williams, Verrels Eugeneo

    Date:   12/09/2022


    The goal of this assignment is to gather information from a dataset containing
    NCAA stats for D1 Basketball teams and answer questions on how NCAA basketball
    has changed from 2013 to 2019. We will use our knowledge on data analysis and
    visualization to create results that will then lead us to a conclusion. To run
    this code, you will need csv, matplotlib, and pandas.

"""
import matplotlib.pyplot as plt
import csv
import pandas as pd

# sets the font size of the x ticks to 4.3
SMALL_SIZE = 4.3
plt.rc('xtick', labelsize=SMALL_SIZE)


def conference_points(file_name):
    """
    Goes through the csv file_name to create a dictionary where the key is
    the name of the conference and the value is the average offensive efficiency (ADJOE)
    by teams in that conference from 2013 to 2019
    :param file_name: csv file that has NCAA stats for every D1 team from 2013 to 2019
    :return: dictionary with conferences as keys and the average offensive efficiency scored as values
    also prints a list with the conference name and average offensive efficiency of the team that has
    the highest average stat
    """

    # open the file for reading
    file_in = open(file_name, "r")

    # initialize empty dict so that it can be used later
    dictionary = {}
    conference_stat_list = []
    csvreader = csv.reader(file_in)
    next(csvreader)

    highest_adjoe = ["", 0]

    # use a for loop to go through each line of the csv file
    for row in csvreader:

        # boolean to keep track of if conference_in_list (false by default)
        conference_in_list = False
        if len(row) > 0:

            # if the conference stats are in the list, we just add to that list instead of creating a new one
            for lists in conference_stat_list:
                if lists[0] == row[1]:
                    conference_in_list = True
                    lists[1] += float(row[4])
                    lists[2] += 1

            # if the conference is not in the conference stats list,
            # we create a nested list that is appended to the conference_stat_list
            if not conference_in_list:
                temp_list = [row[1], float(row[4]), 1]
                conference_stat_list.append(temp_list)

    # use a for loop to go through the nested list and add it to our dictionary
    for lists in conference_stat_list:
        dictionary[lists[0]] = round(lists[1] / lists[2], 3)

        # checks if the adjusted efficiency is higher than the current highest
        if dictionary[lists[0]] > highest_adjoe[1]:
            highest_adjoe = [lists[0], dictionary[lists[0]]]

    print(highest_adjoe)

    file_in.close()
    return dictionary


# Talked to prof. Birrell, and she said using the same graphing function for two visualizations is better style
# so that is what we did.
def comparison_graph(dictionary, n):
    """
    takes the dictionary of conferences and ADJOE and graphs them on a bar graph for comparison
    :param n: int: indicates whether we are doing a comparison graph of ADJOE or three point percentage
    :param dictionary: dictionary with conference names as keys and ADJOE as values
    :return: none: creates a bar graph that compares the ADJOE of every team
    """

    # initializing our graph values of x and y
    x = []
    y = []

    # for loop to go through the keys of our dictionary
    for keys in dictionary.keys():
        x.append(keys)
        y.append(dictionary[keys])

    plt.bar(x, y)
    plt.subplots_adjust(left=.045, right=1)

    # if n == 0, we are graphing visualization 1 (average efficiency)
    if n == 0:
        plt.title("Average Offensive Efficiency of All NCAA D1 Conferences (2013-2019)")
        plt.xlabel("Conference")
        plt.ylabel("Average Points per 100 Possessions")

        # sets size and helps reformat the figure before saving
        plt.savefig("visualization1.png", bbox_inches="tight", dpi=175)

    # if n != 0, we are graphing visualisation 3 (3pt %)
    else:
        plt.title("Average Three Point Percentage of All NCAA D1 Teams (2013-2019)")
        plt.xlabel("Year")
        plt.ylabel("Average Three Point Percentage (%)")
        plt.savefig("visualization3.png", bbox_inches="tight", dpi=175)

    plt.close()


def tempo_and_wins(file_name, conference):
    """
    goes through the rows in file_name and gathers the adjusted tempo
    (possessions per 40 minutes) and number of wins per game for every team in the big 10.
    returns a nested list with the team name, it's number of wins, adjusted tempo, and
    the year
    :param file_name: csv file that has NCAA stats for every D1 team from 2013 to 2019
    :param conference: conference name
    :return: list: nested list with the team name, it's adjusted tempo, win percentage,
    and the year
    """

    # open file for reading
    file_in = open(file_name, "r")

    # initializing the nested list that will include the team name, adjusted tempo, win %, and year
    return_list = []
    csvreader = csv.reader(file_in)
    next(csvreader)

    # for loop to go through each row of the csv
    for row in csvreader:

        if len(row) > 0:

            # if the row is in the desired conference, we add a list
            # for that row that has the desired stats
            if row[1] == conference:

                return_list.append([row[0], float(row[19]), round(float(row[3]) / float(row[2]), 3), row[23]])

    file_in.close()
    return return_list


def scatter_plot(data):
    """
    Takes in the list of lists data and plots them on a scatter plot using
    plt
    :param data: list: list of lists that include what will soon be corresponding x and y values and the years
    :return: none: plots the data using plt
    """

    # sets the font size for x ticks to 10
    plt.rc('xtick', labelsize=10)
    year = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
    format_strings = ["ro", "bo", "co", "go", "mo", "ko", "yo", "kD", "b*"]

    # goes through data and checks if the list has stats for the desired
    # year before adding corresponding x and y values to the x and y lists
    # and plotting them
    for num in range(7):
        x = []
        y = []
        for lists in data:
            if int(lists[3]) == year[num]:
                x.append(lists[1])
                y.append(lists[2])
        plt.plot(x, y, format_strings.pop())

    # shows the plot and completes the graph

    plt.title("Adjusted Tempo vs. Win Percentage in B10 Conference")
    plt.xlabel("Adjusted Tempo (Possession per 40 minutes) For Every Team in B10 Conference")
    plt.ylabel("Win Percentage For Every Team in B10 Conference")

    # positions the legend in upper right and slightly outside the plot
    plt.legend(year, loc='upper right', bbox_to_anchor=(1.1, 1))

    plt.savefig("visualization2.png")
    plt.close()


def three_point_percentage(file_name):
    """
    goes through the csv and creates a dictionary where the key is the year and the value is the three point
    percentage of all NCAA D1 teams of that year.
    :param file_name: csv file that has NCAA stats for every D1 team from 2013 to 2019
    :return: dictionary: dictionary where the key is the year and the value is the three point
    percentage of all NCAA D1 teams of that year
    """

    highest_three_point_percentage = ["", 0]
    dictionary = {}
    three_point_percentage_data_frame = pd.read_csv(file_name)

    # gets every unique year value in year column of csv and sorting by chronological order
    for years in sorted(three_point_percentage_data_frame['YEAR'].unique()):

        # selects rows in csv with the corresponding year (variables years) then takes
        # the mean of the three point percentage values for each corresponding year (variable years)
        # creates the dictionary that will be returned
        dictionary[years] = \
            three_point_percentage_data_frame[three_point_percentage_data_frame['YEAR'] == years]["3P_O"].mean()
        dictionary[years] = round(dictionary[years], 3)

    # goes through the dictionary and sets a list that has the year and three point
    # percentage
    for keys in dictionary.keys():
        if dictionary[keys] > highest_three_point_percentage[1]:
            highest_three_point_percentage = [keys, dictionary[keys]]

    print(highest_three_point_percentage)

    return dictionary


def main():

    comparison_graph(conference_points("NCAA_Stats/cbb.csv"), 0)
    scatter_plot(tempo_and_wins("NCAA_Stats/cbb.csv", "B10"))
    comparison_graph(three_point_percentage("NCAA_Stats/cbb.csv"), 1)


if __name__ == '__main__':
    main()
