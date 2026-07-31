from osu import Client
from tkinter import *
from tkinter import messagebox, ttk
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
    load_dotenv()
    CLIENT_ID = int(os.getenv("CLIENT_ID"))
    SECRET = os.getenv("SECRET")
    client = Client.from_credentials(CLIENT_ID, SECRET, None)

    # get username and mode
    username = username_entry.get()
    mode_selection = mode.get()

    if len(username) == 0:
        messagebox.showwarning("Warning", "Username must not be blank")
        return

    try:
        user_get = client.get_user(username, mode_selection)

    except requests.exceptions.HTTPError as err:
        if err.response is not None:
            match err.response.status_code:
                case 404:
                    messagebox.showerror("User not found!", f"User {username} does not exist. Perhaps you made a typo?")
                    return
                case _:
                    messagebox.showerror("Unknown error", "An unknown error occurred. The server could be busy or down. Please try again later.")
                    return
        else:
            messagebox.showerror("Error", err)
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

    if sum(grades.values()) == 0:
        messagebox.showerror("Error", f"There is nothing to plot because user '{user_get.username}' has no SS, S, and A ranks for the selected mode.")
        return

    today = datetime.date.today().strftime("%Y-%m-%d")

    # For standard and ctb modes
    match mode_selection:
        case 'osu':
            mode_selection = 'standard'
        case 'fruits':
            mode_selection = 'ctb'

    # Plot the grades
    plt.clf()
    wedges, _ = plt.pie(grades.values(),
            colors=[colors[grade] for grade in grades.keys()])
    plt.title(f"{user_get.username}'s grades for {mode_selection} ({today})")
    plt.legend(wedges, [f"{grade} ({grade_ct / sum(grades.values()) * 100:.2f}%)" for grade, grade_ct in grades.items()], loc="best")

    plt.show()

def save_credentials():
    try:
        CLIENT_ID = int(id_entry.get().strip())
        SECRET = secret_entry.get().strip()

    except ValueError:
        messagebox.showerror("Error", "Client ID should be a number")
        return

    if len(str(CLIENT_ID)) == 0 or len(SECRET) == 0:
        messagebox.showerror("Error", "Client ID and secret must not be blank")
        return

    with open(".env", 'w') as f:
        f.write(f'''
        CLIENT_ID={CLIENT_ID}\n
        SECRET={SECRET}\n
        ''')

    load_dotenv(override=True)

    messagebox.showinfo("Success", "Credentials updated!")


def toggle_show():
    secret_entry.config(show="")

# create .env if it doesn't exist
if not os.path.exists('.env'):
    with open(".env", 'w') as f:
        f.write('''
        CLIENT_ID=00000\n
        SECRET=\n
        ''')

    messagebox.showinfo("Info", "Before using this app, configure your API credentials in the 'Configure API credentials' tab. You will need an osu! API key to use this app.\nhttps://osu.ppy.sh/wiki/en/osu!api")

root = Tk()
root.title("osu! Grades Chart")
mode = StringVar()
toggle = BooleanVar()

container = ttk.Notebook(root)
container.pack(side="top", fill="both", expand=True)

main_menu_tab = Frame(container)
configure_credentials_tab = Frame(container)
container.add(main_menu_tab, text="Main menu")
container.add(configure_credentials_tab, text="Configure API credentials")

# Main menu
username_label = Label(main_menu_tab, text="Enter username").grid(row=0, column=0)
username_entry = Entry(main_menu_tab)
username_entry.grid(row=0, column=1)

mode_label = Label(main_menu_tab, text="Select mode").grid(row=1, column=0)
mode_button1 = Radiobutton(main_menu_tab, text="Standard", variable=mode, value="osu").grid(row=1, column=1)
mode_button2 = Radiobutton(main_menu_tab, text="Taiko", variable=mode, value="taiko").grid(row=1, column=2)
mode_button3 = Radiobutton(main_menu_tab, text="Catch", variable=mode, value="fruits").grid(row=1, column=3)
mode_button4 = Radiobutton(main_menu_tab, text="Mania", variable=mode, value="mania").grid(row=1, column=4)

toggle_button = Checkbutton(main_menu_tab, text="Combine regular SS/S with hidden SS/S", variable=toggle, onvalue=True, offvalue=False).grid(row=2, column=0)
button = Button(main_menu_tab, text="Get user grades", command=submit).grid(row=3, column=2)

# Configure API credentials tab
id_label = Label(configure_credentials_tab, text="Client ID").grid(row=0, column=0)
id_entry = Entry(configure_credentials_tab)
id_entry.grid(row=0, column=1)

secret_label = Label(configure_credentials_tab, text="Secret key").grid(row=1, column=0)
secret_entry = Entry(configure_credentials_tab, show="*")
secret_entry.grid(row=1, column=1)

hide_button = Button(configure_credentials_tab, text="Show", command=toggle_show).grid(row=1, column=2)

save_button = Button(configure_credentials_tab, text="Save credentials", command=save_credentials).grid(row=2, column=2)
root.mainloop()

