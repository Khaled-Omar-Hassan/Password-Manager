import json
from random import randint
from tkinter import messagebox, PhotoImage
from customtkinter import *
from password_manager import PasswordManager
from PIL import Image
import re

USER_DATA_PATH = "User_Credentials/user_credentials.json"
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def check(email):
    """Check if email matches the expected regex."""
    return re.fullmatch(EMAIL_REGEX, email) is not None


class LoginRegisterWindow(CTk):
    def __init__(self):
        super().__init__()
        self.title("Sign In")
        self.resizable(False, False)
        self.user_data_path = USER_DATA_PATH
        self.create_ui()

    def create_ui(self):
        self.canvas = CTkCanvas(self, width=400, height=566, highlightthickness=0)
        self.background = PhotoImage(file="Images/sign_in.png")
        self.canvas.create_image(200, 283, image=self.background)

        self.create_entries()
        self.create_buttons()
        self.canvas.pack()

    def create_entries(self):

        def create_entry(bg_color='#132339', fg_color='white', width=160, text_color='black', show=None):
            return CTkEntry(self.canvas, corner_radius=50, bg_color=bg_color, fg_color=fg_color,
                            width=width, text_color=text_color, show=show)

        self.email_entry = create_entry()
        self.pw_entry = create_entry(show='*')

        self.canvas.create_window(267, 257, window=self.email_entry)
        self.canvas.create_window(267, 320, window=self.pw_entry)

        self.canvas.create_text(55, 254, text="Email", font="calibri 20 bold", fill="white", anchor="w")
        self.canvas.create_text(55, 317, text="Password", font="calibri 20 bold", fill="white", anchor="w")

    def create_buttons(self):
        def create_button(text, command, width=100, height=30):
            return CTkButton(self, text=text, command=command, fg_color="#132339",
                             corner_radius=32, hover_color='#7CA0BF', border_color='#7CA0BF', border_width=2,
                             width=width, height=height)

        self.generate_button = create_button("Login", self.login)
        self.random_button = create_button("Register", self.register_user)

        eye_image = Image.open('Images/eye_icon.png')
        self.eye_image = CTkImage(eye_image, size=(35, 20))
        self.toggle_button = CTkButton(self, command=self.toggle_password_visibility, fg_color="#132339", width=35,
                                       hover=False,
                                       text='', image=self.eye_image)

        self.canvas.create_window(140, 440, window=self.generate_button)
        self.canvas.create_window(260, 440, window=self.random_button)
        self.canvas.create_window(373, 320, window=self.toggle_button)

    def load_user_data(self):
        """Load user data from file or return an empty dictionary."""
        if os.path.exists(self.user_data_path):
            with open(self.user_data_path, "r") as file:
                return json.load(file)
        return {}

    def save_user_data(self, user_data):
        """Save user data to a JSON file."""
        with open(self.user_data_path, "w") as file:
            json.dump(user_data, file, indent=4)

    def login(self):
        username = self.email_entry.get()
        password = self.pw_entry.get()
        user_data = self.load_user_data()

        if username == "":
            messagebox.showinfo("Error", "Please Enter Email")
            return

        if username not in user_data:
            messagebox.showinfo("Error", "User Does Not Exist")
            return

        if password == "":
            messagebox.showinfo("Error", "Please Enter Password")
            return

        if user_data[username]["password"] != password:
            messagebox.showinfo("Error", "Incorrect Password")
            return

        messagebox.showinfo("Success", "Login successful!")
        self.open_main_app(username)

    def register_user(self):
        username = self.email_entry.get()
        password = self.pw_entry.get()

        user_data = self.load_user_data()

        if username in user_data:
            messagebox.showinfo("Error", "Username already exists.")
            return

        if not username:
            messagebox.showinfo("Error", "Please Enter Email")
            return

        if not password:
            messagebox.showinfo("Error", "Please Enter Password")
            return

        if not check(username.strip()):
            messagebox.showinfo("Error", "Invalid Email")
            return

        user_data[username] = {"password": password}
        self.save_user_data(user_data)

        messagebox.showinfo("Success", "Registration successful!")
        self.open_main_app(username)

    def toggle_password_visibility(self):
        """Toggle password visibility."""
        if self.pw_entry.cget("show") == "*":
            self.pw_entry.configure(show="")
        else:
            self.pw_entry.configure(show="*")

    def open_main_app(self, username):
        self.destroy()
        app = App(username)
        app.mainloop()


class ToplevelWindow(CTkToplevel):
    def __init__(self, password_manager):
        super().__init__()
        self.title("Password Generator")
        self.resizable(False, False)
        self.password_manager = password_manager
        self.create_ui()
        self.grab_set()
        self.set_password_callback = None

    def create_ui(self):
        self.canvas = CTkCanvas(self, width=400, height=566, highlightthickness=0)
        self.background = PhotoImage(file="Images/generate_templete.png")
        self.canvas.create_image(200, 283, image=self.background)
        self.create_entries()
        self.create_buttons()
        self.canvas.pack()

    def create_entries(self, ):
        def create_entry():
            return CTkEntry(self.canvas, bg_color='#B7BAC4', fg_color='white', width=50,
                            border_color='#B7BAC4', text_color='black')

        self.upper_case_entry = create_entry()
        self.lower_case_entry = create_entry()
        self.numbers_entry = create_entry()
        self.symbols_entry = create_entry()

        entry_positions = {
            "upper_case": (300, 170),
            "lower_case": (300, 222),
            "numbers": (300, 274),
            "symbols": (300, 326),
        }

        entry_labels = {
            "upper_case": "Uppercase",
            "lower_case": "Lowercase",
            "numbers": "Numbers",
            "symbols": "Symbols",
        }

        for name, pos in entry_positions.items():
            self.canvas.create_window(pos[0], pos[1], window=getattr(self, f"{name}_entry"))
            self.canvas.create_text(95, pos[1] - 3, text=entry_labels[name],
                                    font="calibri 20 bold", fill="white", anchor="w")

    def create_buttons(self):
        def create_button(text, command):
            return CTkButton(self, text=text, command=command, fg_color="#132339",
                             width=100, height=30, corner_radius=32, hover_color='#7CA0BF',
                             border_color='#7CA0BF', border_width=2)

        self.generate_button = create_button("Generate", self.generate_password)
        self.random_button = create_button("Randomize!", self.generate_random_password)

        self.canvas.create_window(260, 460, window=self.generate_button)
        self.canvas.create_window(140, 460, window=self.random_button)

    def generate_password(self):
        values = {
            "upper": int(self.upper_case_entry.get() or 0),
            "lower": int(self.lower_case_entry.get() or 0),
            "number": int(self.numbers_entry.get() or 0),
            "symbol": int(self.symbols_entry.get() or 0),
        }
        password = self.password_manager.generate(**values)
        if self.set_password_callback:
            self.set_password_callback(password)  # Call the callback with the generated password
        self.destroy()

    def generate_random_password(self):
        # Randomly generate numbers for upper/lower/number/symbol
        random_values = {
            "upper": randint(3, 5),
            "lower": randint(3, 5),
            "number": randint(1, 3),
            "symbol": randint(1, 3),
        }

        password = self.password_manager.generate(**random_values)
        if self.set_password_callback:
            self.set_password_callback(password)  # Call the callback with the generated password
        self.destroy()


class App(CTk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title("Password Manager")
        self.resizable(False, False)
        self.password_manager = PasswordManager(username)
        self.create_ui()
        self.toplevel_window = None
        self.email_entry.insert(0, username)  # Insert the username into the email field

    def create_ui(self):
        self.canvas = CTkCanvas(width=500, height=707, highlightthickness=0)
        self.create_images()
        self.canvas.create_image(250, 353, image=self.img)
        self.create_entries()
        self.create_buttons()
        self.canvas.pack()

    def create_images(self):
        self.img = PhotoImage(file="Images/main_window.png")
        database_image = Image.open('Images/database.png')
        self.database_image = CTkImage(database_image, size=(52, 50))

    def create_entries(self):
        # Function to create an entry with default settings
        def create_entry(show=None):
            return CTkEntry(self.canvas, corner_radius=50, bg_color='#132339', fg_color='white',
                            width=180, text_color='black', show=show)

        # Create main entries for the application
        self.website_entry = create_entry()
        self.email_entry = create_entry()
        self.password_entry = create_entry(show='*')  # Password field
        self.comments_entry = create_entry()

        entry_positions = {
            "website": (330, 300),
            "email": (330, 340),
            "password": (330, 380),
            "comments": (330, 420),
        }

        # Set text labels for the entries
        entry_labels = {
            "website": "Application",
            "email": "Email",
            "password": "Password",
            "comments": "Comment",
        }

        for name, pos in entry_positions.items():
            self.canvas.create_window(pos[0], pos[1], window=getattr(self, f"{name}_entry"))
            self.canvas.create_text(95, pos[1] - 3, text=entry_labels[name],
                                    font="calibri 20 bold", fill="white", anchor="w")

    def create_buttons(self):
        # Reusable button function
        def create_button(text, command):
            return CTkButton(self, text=text, command=command, fg_color="#132339",
                             width=100, height=30, corner_radius=32, hover_color='#7CA0BF',
                             border_color='#7CA0BF', border_width=2)

        self.search_button = create_button("Search", self.search_password)
        self.generate_button = create_button("Generate", self.open_toplevel)
        self.save_button = create_button("Save", self.save_password)

        self.data_button = CTkButton(self, command=self.show_data,
                                     fg_color="#132339", width=50, hover=False,
                                     text='', image=self.database_image)

        self.sign_out_button = create_button("Sign Out", self.sign_out)

        eye_image = Image.open('Images/eye_icon.png')
        self.eye_image = CTkImage(eye_image, size=(35, 20))
        self.toggle_password_button = CTkButton(self, command=self.toggle_password_visibility, width=35,
                                                fg_color="#132339", hover=False,
                                                text='', image=self.eye_image)

        button_positions = {
            "search": (130, 520),
            "generate": (250, 520),
            "save": (370, 520),
            "data": (60, 660),
            "sign_out": (420, 665),
            "toggle_password": (460, 380),
        }

        for name, pos in button_positions.items():
            self.canvas.create_window(pos[0], pos[1], window=getattr(self, f"{name}_button"))

    def clear_entries(self):
        """Clear all entries in the application."""
        for entry in [self.website_entry, self.password_entry, self.comments_entry]:
            entry.delete(0, 'end')

    def save_password(self):
        """Save password data."""
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        comment = self.comments_entry.get()

        if not all([website, email, password]):
            messagebox.showinfo("Oops", "Please fill all required fields.")
            return

        self.password_manager.save_password(website, email, password, comment)
        messagebox.showinfo("Saved", "Password has been saved.")
        self.clear_entries()

    def toggle_password_visibility(self):
        """Toggle password visibility."""
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def search_password(self):
        """Search for a password by website/application name."""
        website = self.website_entry.get()
        result = self.password_manager.search_password(website)

        if result:
            comment_text = f"\nComment: {result['comment']}" if result["comment"] else ""
            messagebox.showinfo(
                website,
                f"Application: {website}\nEmail: {result['email']}\nPassword: {result['password']}{comment_text}"
            )
        else:
            messagebox.showinfo("Not Found", "No data found.")

    def open_toplevel(self):
        """Open the password generation window."""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self.password_manager)
            self.toplevel_window.set_password_callback = self.set_generated_password
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

    def set_generated_password(self, password):
        """Set the generated password in the password field."""
        self.password_entry.delete(0, 'end')
        self.password_entry.insert(0, password)

    def show_data(self):
        """Display the stored data."""
        self.password_manager.show_database()

    def sign_out(self):
        """Sign out from the application."""
        self.destroy()  # Close the current window

        # Reopen the login/register window
        login_window = LoginRegisterWindow()
        login_window.mainloop()  # Open the login window
