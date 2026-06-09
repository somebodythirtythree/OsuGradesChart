from osu import Client
from tkinter import *
from tkinter import messagebox
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os, requests

def submit():
    # get username and mode
    username = username_entry.get()
    mode_selection = mode.get()

    if len(username) == 0:
        messagebox.showwarning("Warning", "Username must not be blank")
        return

    try:
        user_get = client.get_user(username, mode_selection)

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            messagebox.showerror("User not found!", f"User {username} does not exist. Perhaps you made a typo?")
            return

    user_grades = user_get.statistics.grade_counts
    grades = {
        'ss': user_grades[0] + user_grades[1],
        's': user_grades[2] + user_grades[3],
        'a': user_grades[4]
    }  # SS and S include hidden SS/S

    for k, v in grades.items():
        print(f"{k}: {v} ({v / sum(grades.values()) * 100:.2f}%)")

    # Plot the grades
    plt.clf()
    plt.pie(grades.values(), labels=grades.keys(), autopct="%.2f%%",
            colors=['#FFD700', 'yellow', '#00FF00'])
    plt.title(f"{username}'s grades for {mode_selection}")

    plt.show()

root = Tk()
mode = StringVar()

# get API credentials
load_dotenv()
CLIENT_ID = int(os.getenv("CLIENT_ID"))
SECRET = os.getenv("SECRET")
client = Client.from_credentials(CLIENT_ID, SECRET, None)

username_label = Label(root, text="Enter username").grid(row=0, column=0)
username_entry = Entry(root)
username_entry.grid(row=0, column=1)

mode_label = Label(root, text="Select mode").grid(row=1, column=0)
mode_button1 = Radiobutton(root, text="Standard", variable=mode, value="osu").grid(row=1, column=1)
mode_button2 = Radiobutton(root, text="Taiko", variable=mode, value="taiko").grid(row=1, column=2)
mode_button3 = Radiobutton(root, text="Catch", variable=mode, value="fruits").grid(row=1, column=3)
mode_button4 = Radiobutton(root, text="Mania", variable=mode, value="mania").grid(row=1, column=4)

button = Button(root, text="Get user grades", command=submit).grid(row=2, column=2)

root.mainloop()

