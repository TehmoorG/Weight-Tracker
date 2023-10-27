# Weight-tracker command-line programme

## Overview
Weight Tracker is a Python command-line application for tracking and visualizing weight changes over time. It provides features for logging weight, setting weight goals, and providing estimations on when these goals will be reached.

## Features
- Log daily weight.
- Set a weight goal.
- View progress towards weight goal.
- Calculate expected time to reach the goal based on recent trends.
- Generate a graph showing weight changes over a specified period.

## Dependencies
The Weight Tracker requires Python 3.8 or later and uses the following Python libraries:
- matplotlib
- prettytable
- argparse
These can be installed using pip:
pip install matplotlib prettytable argparse

## Usage
### First time users
For first time users, you need to run the following command:
"python project.py <username>
Please replace "username" with your own username or any identifier of your choice. This creates helps create the necessary files for logging your weight and setting a weight goal.

### Returning users
If you have used this programme before, please ensure you use the same username used previously case sensitively otherwise your previous data wont be accessible.

### Application Menu:
After starting the application, you'll be presented with the following options:
1. Record your weight
2. View weight history
3. Set Weight Goal
4. View Goal/Target weight
5. End program

You can enter the number associated with each option to carry out that action.