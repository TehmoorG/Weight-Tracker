"""
This module is for tracking and visualizing weight changes over time.
It includes features for logging weight, setting weight goals, and more.
If you are new to this programme you should run "python project.py username"
If you have used this programme make sure you run the same username you have before to access your data and files.
"""


from datetime import date, datetime, timedelta
import csv
from sys import exit
import argparse
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from prettytable.colortable import ColorTable, Themes


class Weight:
    """
    This class provides methods to log weight, view weight history,
    set weight goals, and calculate the estimated time to reach a weight goal.
    """

    def __init__(self, name):
        """
        Initializes the Weight object with a weight log filename and a goal filename.

        Parameters:
        name (str): The users username. Case sensitive also.

        Returns:
        None
        """

        self.filename = name + "_log.csv"
        self.goal_filename = name + "_goal.txt"

    def log_weight(self):
        """
        Record the weight of the user in KG to csv file created using username specified in command line argument

        Paramters:
        None

        Returns:
        None
        """
        count = 0
        while count < 3:
            try:
                weight = float(input("Weight (in KG): "))
                if weight <= 0:
                    count += 1
                    raise ValueError
                break
            except ValueError:
                print("Invalid weight. Please enter a number.")

        # exit program if too many failed attempts
        if count == 3:
            exit("Too many attempts. Restart program")
        today = date.today()
        # determine whether the file is empty to write header

        with open(self.filename, "a") as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Weight"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow({"Date": today, "Weight": weight})

    def weight_history(self, days):
        """
        Allows the user to see previous weght logs for the number of days they specify.
        Creates a graph ong file showing the data graphically and prints a table in the terminal to show the data

        Paramters:
        str: the number of days the user wishes to view their "weight" history

        Returns:
        None
        """
        with open(self.filename, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)

        # calculate the date 'days' days ago
        cut_off_date = datetime.now() - timedelta(days=days)

        # filter the data to include only the rows within the desired date range
        data = [
            row
            for row in data
            if datetime.strptime(row["Date"], "%Y-%m-%d") >= cut_off_date
        ]
        # if there are not enough logs we will initialise the first date as zero
        if days > len(data):
            start_date = [{"Date": str(cut_off_date).split(" ")[0], "Weight": 0}]
            data = start_date + data

        # Separate dates and weights into lists
        dates = [entry["Date"] for entry in data]
        weights = [float(entry["Weight"]) for entry in data]

        # Plot the data in a graph
        plt.plot(dates, weights)
        plt.xlabel("Date")
        plt.ylabel("Weight (kg)")
        plt.title("Weight over time")
        plt.savefig("Weight_history.png")

        # create a table
        table = PrettyTable()
        table = ColorTable(theme=Themes.OCEAN)
        table.add_column("Date", dates)
        table.add_column("Weight(Kg)", weights)
        print(table)

    def set_goal(self):
        """
        Asks user for a specifc weight goal in Kilograms.Creats a text file with just the number and overwrites previous goal if this function has been used before

        Paramters:
        None

        Returns:
        None

        """
        while True:
            try:
                goal = float(input("What is your desired weight(in KG)? "))
                if goal <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid weight. Please enter a positive number.")
        # create/rewrite text file with desired weight goal
        with open(self.goal_filename, "w") as file_obj:
            file_obj.write(str(goal))

    def view_goal(self):
        """
        Allows the user to view goal if setgoal method has been used before.
        If there are enough weight logs it will output an esitmation of days needed for user to reach goal based on last 10 weight logs

        Parameters:
        None

        Returns:
        None
        """

        # 1. Read goal weight
        try:
            with open(self.goal_filename, "r") as file_obj:
                goal = float(file_obj.read())
        except FileNotFoundError:
            print("Goal weight not set.")
            return
        except ValueError:
            print("Invalid goal weight.")
            return

        # 2. Display goal weight
        print(f"Your goal weight is: {goal} kg")

        # 3. Calculate average weight loss rate
        with open(self.filename, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)

        if len(data) < 10:
            print("Not enough data to calculate the expected days to reach goal.")
            return

        last_10_entries = data[-10:]
        total_weight_loss = float(last_10_entries[0]["Weight"]) - float(
            last_10_entries[-1]["Weight"]
        )
        average_daily_weight_loss = total_weight_loss / len(last_10_entries)

        # 4. Calculate days to reach goal
        current_weight = float(data[-1]["Weight"])
        weight_needed_to_lose = current_weight - goal
        if average_daily_weight_loss <= 0:
            print("You're not losing weight on average. Keep trying!")
        else:
            days_to_reach_goal = weight_needed_to_lose / average_daily_weight_loss

            # 5. Display estimated days to reach goal
            print(f"Estimated days to reach goal: {days_to_reach_goal}")

    @staticmethod
    def get_days():
        """
        Static method that is called when user wishes to see weight history.
        Allows the user to select how far back they would like to see.

        Paramters:
        None

        Returns:
        int: The number of days the user wants to look back in their weight history.

        """
        print("Select time period")
        print("1. 7 days")
        print("2. 30 days")
        print("3. 90 days")
        print("4. 365 days")
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                return 7
            case "2":
                return 30
            case "3":
                return 90
            case "4":
                return 365
            case _:
                print("Invalid choice. Please select from 1 to 4.")
                return Weight.get_days()  # Recursive call if the choice is invalid


def main():
    """
    The main entry point of the application.

    It continuously prompts the user to choose an action: recording weight, viewing weight history, setting weight goal,
    viewing weight goal or ending the program, and uses the corresponding methods from the `Weight` class based on user input.

    Parameters:
    None

    Returns:
    None
    """
    name = parser()
    user = Weight(name)

    while True:
        print("\nWhat would you like to do?")
        print("1. Record your weight")
        print("2. View weight history")
        print("3. Set Weight Goal")
        print("4. View Goal/Target weight")
        print("5. End program")
        action = input()

        if action == "1":
            user.log_weight()
        elif action == "2":
            try:
                user.weight_history(Weight.get_days())
            except FileNotFoundError:
                exit("Error: Log your weight first")
        elif action == "3":
            user.set_goal()
        elif action == "4":
            user.view_goal()
        elif action == "5":
            exit()
        else:
            print("Invalid choice. Please select from 1 to 5.")


def parser():
    """
    Parse command-line arguments using argparse.

    The only command-line argument that should be added is the username of the user

    Returns:
    argparse.Namespace: The parsed command-line arguments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "username", help="Your username."
    )
    args = parser.parse_args()
    return args.username

if __name__ == "__main__":
    main()
