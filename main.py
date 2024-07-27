import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip


# ---------------------------- SEARCH PASSWORD ---------------------------------- #
def find_password():
    user_website = website_entry.get()
    user_website = user_website.lower()
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found")
    else:
        try:
            website_details = data[user_website]
        except KeyError:
            messagebox.showerror(title="Error", message="No details for website exists")
        else:
            user_email = website_details["email"]
            user_password = website_details["password"]
            messagebox.showinfo(title=user_website.capitalize(), message=f"Email: {user_email} \nPassword: {user_password}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for i in range(nr_letters)]

    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().lower()
    email = user_entry.get().lower()
    password = password_entry.get().lower()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title=website_entry.get(), message=f"These are the details entered: "
                                                                          f"\nEmail: {user_entry.get()} \nPassword: {password_entry.get()} \nIs it ok to  save?")
        if is_ok:
            try:
                with open("passwords.json", "r") as file:
                    data = json.load(file)
                    data.update(new_data)
            except FileNotFoundError:
                with open("passwords.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                with open("passwords.json", "w") as file:
                    json.dump(data, file, indent=4)
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
website_entry = Entry(width=26)
website_entry.focus()
website_entry.grid(row=1, column=1)

user_label = Label(text="Email/Username:")
user_label.grid(row=2, column=0)
user_entry = Entry(width=42)
user_entry.insert(0, "alvindandeebo@gmail.com")
user_entry.grid(row=2, column=1, columnspan=2)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_entry = Entry(width=26)
password_entry.grid(row=3, column=1)
generate_password_button = Button(text="Generate Password", command=generate_password, width=12)
generate_password_button.grid(row=3, column=2)

add_button = Button(width=42, text="Add", command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=12, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
