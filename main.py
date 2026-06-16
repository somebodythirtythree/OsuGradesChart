from osu import Client
from tkinter import *
from tkinter import messagebox
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os, requests, datetime

colors = {
    'ssh': '#C0C0C0',
    'ss': '#FFD700',
    'sh': '#999B9B',
    's': '#FFFF00',
    'a': '#00FF00'
}

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
    if toggle.get():
        grades = {
            'ss': user_grades[0] + user_grades[1],
            's': user_grades[2] + user_grades[3],
            'a': user_grades[4]
        }
    else:
        grades = {
            'ssh': user_grades[0],
            'ss': user_grades[1],
            'sh': user_grades[2],
            's': user_grades[3],
            'a': user_grades[4]
        }

    today = datetime.date.today().strftime("%Y-%m-%d")

    for k, v in grades.items():
        print(f"{k}: {v} ({v / sum(grades.values()) * 100:.2f}%)")

    # Plot the grades
    plt.clf()
    wedges, _ = plt.pie(grades.values(),
            colors=[colors[grade] for grade in grades.keys()])
    plt.title(f"{username}'s grades for {mode_selection} ({today})")
    plt.legend(wedges, [f"{grade} ({grade_ct / sum(grades.values()) * 100:.2f}%)" for grade, grade_ct in grades.items()], loc="best")

    plt.show()

root = Tk()
root.title("osu! Grades Chart")
mode = StringVar()
toggle = BooleanVar()

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

toggle_button = Checkbutton(root, text="Combine regular SS/S with hidden SS/S", variable=toggle, onvalue=True, offvalue=False).grid(row=2, column=0)
button = Button(root, text="Get user grades", command=submit).grid(row=3, column=2)

root.mainloop()

