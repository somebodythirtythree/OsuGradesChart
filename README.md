# About this program

This simple Python program uses osu!api v2 and the `matplotlib` library to create a pie chart of a user's SS, S, and A ranks.

## How does it work?

When the program is run, a GUI is created, asking the user to enter a username and select the desired mode. 
Once the user has clicked the submit button, the program will get the grade counts (SS, S, A) for the username and mode specified
and create a pie chart consisting of those grades. *The pie chart is displayed in a separate window.*

*(Note: if `Combine regular SS/S with hidden SS/S` is not toggled, hidden SS/S will be separated from regular ones.)*

## Sample plots

![mrekk's grades in standard](https://i.ibb.co/9HL8R7tn/Figure-1.png "mrekk's grades in standard")
![mrekk's grades in standard, hidden ranks combined](https://i.ibb.co/NcLR5g3/Figure-2.png "mrekk's grades in standard, hidden ranks combined")
![Vallejo's (somebody_33's) grades in taiko](https://i.ibb.co/QjhczJHg/Figure-3.png "Vallejo's (somebody_33's) grades in taiko")

# Usage of this program

**IMPORTANT: Before running `main.py`, ensure that you have created an `.env` file 
with your API credentials! You will need a valid osu! API key to use this program.**

The following modules are required for running this program:

- [osu.py](https://github.com/sheppsu/osu.py)
- [matplotlib](https://matplotlib.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Please view each link for installation instructions if you do not have them.
Once you have installed all the dependencies, run `main.py`.

