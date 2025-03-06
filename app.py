from customtkinter import *
from PIL import ImageTk, Image as PILImage
from pyperclip import copy
import random
import os

BASE_DIR = os.path.dirname(__file__)

try:
    from ctypes import windll

    myappid = "passwordgenerator.passwordgenerator.subproduct.version"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class CustomImage(CTkImage):
    def __init__(self, name: str, size: tuple[int, int] = None):
        self.file = os.path.join(BASE_DIR, "icons", name)
        self.image = PILImage.open(self.file)

        if size:
            self.image = self.image.resize(size, PILImage.Resampling.LANCZOS)

        super().__init__(light_image=self.image, size=size or self.image.size)


class Window(CTk):

    def __init__(self, appearance_mode: str = "light", **kwargs):
        super().__init__(**kwargs)
        self.title("Passwort Generator")
        self.geometry("800x400")
        self.wm_iconbitmap()
        self.iconbitmap(os.path.join(BASE_DIR, "icons", "favicon.ico"))
        self.columnconfigure(0, weight=1)
        self._set_appearance_mode(appearance_mode)


class PasswordGenerator():

    def __init__(self):
        self.password = ""
        self.length = passwordConfigs.passwordLengthEntryVar.get()
        self.hasCapitalletters = passwordConfigs.hasCapitallettersVar.get()
        self.hasLowercaseletters = passwordConfigs.hasLowercaselettersVar.get()
        self.hasSpecialcharacters = passwordConfigs.hasSpecialcharactersVar.get()
        self.hasDigits = passwordConfigs.hasDigitsVar.get()

        self.capitalletters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.lowercaseletters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        self.specialcharacters = ["!", "\"", "§", "$", "%", "&", "/", "(", ")", "=", "?", "{", "}", "*", "'", "+", "#", "-", "^", "[", "]", "|", ";", "@", "<", ">", ":", "_", "°", "\\", "~"]
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def random(self):
        password = []
        if self.hasCapitalletters:
            password.append(random.choice(self.capitalletters))
        if self.hasLowercaseletters:
            password.append(random.choice(self.lowercaseletters))
        if self.hasSpecialcharacters:
            password.append(random.choice(self.specialcharacters))
        if self.hasDigits:
            password.append(random.choice(self.digits))

        all_chars = []
        if self.hasCapitalletters:
            all_chars += self.capitalletters
        if self.hasLowercaseletters:
            all_chars += self.lowercaseletters
        if self.hasSpecialcharacters:
            all_chars += self.specialcharacters
        if self.hasDigits:
            all_chars += self.digits

        while len(password) < self.length:
            password.append(random.choice(all_chars))

        random.shuffle(password)
        self.password = "".join(password)
        return "".join(password)


class PasswordEntry():

    def __init__(self):
        self.passwordEntryFrame = CTkFrame(window, fg_color=window.cget("bg"), corner_radius=0, border_color="#8c8e91", border_width=1)
        self.passwordEntryFrame.grid(row=0, column=0, padx=20, pady=20, sticky=EW)
        self.passwordEntryFrame.columnconfigure(0, weight=5)
        self.passwordEntryFrame.columnconfigure(1, weight=1) 

        self.password_var = StringVar()
        self.passwordEntry = CTkEntry(self.passwordEntryFrame, fg_color=window.cget("bg"), text_color="#27282b", placeholder_text="Random Password", font=('Arial', 20, 'bold'), corner_radius=2, border_width=0, height=35, textvariable=self.password_var)
        self.passwordEntry.grid(row=0, column=0, sticky=EW, padx=5, pady=5)

        self.passwordButtonsFrame = CTkFrame(self.passwordEntryFrame, fg_color=window.cget("bg"), corner_radius=0)
        self.passwordButtonsFrame.grid(row=0, column=1, sticky="e", padx=5)
        self.passwordButtonsFrame.columnconfigure((0, 1), weight=1)

        self.copyImage = CustomImage(name="copy.png", size=(20, 20))
        self.copyPasswordButton = CTkButton(self.passwordButtonsFrame, text="", image=self.copyImage, fg_color="#3299FF", hover_color="#3299FF", width=30, height=30, corner_radius=4, command=self.copyPassword)
        self.copyPasswordButton.grid(row=0, column=0, padx=(0, 5))

        self.reloadImage = CustomImage(name="reload.png", size=(20, 20))
        self.reloadPasswordButton = CTkButton(self.passwordButtonsFrame, text="", image=self.reloadImage, fg_color="#3299FF", hover_color="#3299FF", width=30, height=30, corner_radius=4, command=self.reloadPassword)
        self.reloadPasswordButton.grid(row=0, column=1)

    def reloadPassword(self):
        randomPassword = PasswordGenerator().random()
        self.password_var.set(value=randomPassword)

    def copyPassword(self):
        copy(self.password_var.get())


class CustomisePassword():

    def __init__(self):
        self.customisePasswordFrame = CTkFrame(window, fg_color=window.cget("bg"), corner_radius=0, border_color="#8c8e91", border_width=1)
        self.customisePasswordFrame.grid(row=1, column=0, pady=(20, 0), sticky=EW, padx=20)
        self.customisePasswordFrame.columnconfigure(0, weight=1)

        self.headingLabel = CTkLabel(self.customisePasswordFrame, text="Passwort anpassen", text_color="#27282b", font=('Arial', 25, 'bold'))
        self.headingLabel.grid(row=0, column=0, sticky=W, pady=10, padx=10)

        self.configsFrame = CTkFrame(self.customisePasswordFrame, fg_color=window.cget("bg"))
        self.configsFrame.grid(row=1, column=0, padx=10, pady=(10, 20), sticky=EW)
        self.configsFrame.columnconfigure(0, weight=1)
        self.configsFrame.columnconfigure(1, weight=1)

        # Password Length
        self.passwordLengthFrame = CTkFrame(self.configsFrame, fg_color=window.cget("bg"), corner_radius=0)
        self.passwordLengthFrame.grid(row=0, column=0, sticky=NSEW)

        self.passwordLengthLabel = CTkLabel(self.passwordLengthFrame, text="Passwortlänge", text_color="#27282b", font=('Arial', 15))
        self.passwordLengthLabel.grid(row=0, column=0)

        self.passwordLengthEntry = CTkEntry(self.passwordLengthFrame, fg_color=window.cget("bg"), text_color="#27282b", placeholder_text="Random Password", font=('Arial', 15), corner_radius=5, border_width=1, border_color="#8c8e91", height=35, width=50, textvariable=passwordConfigs.passwordLengthEntryVar)
        self.passwordLengthEntry.grid(row=1, column=0, pady=(5, 0))

        self.passwordLengthSlider = CTkSlider(self.passwordLengthFrame, from_=1, to=50, width=100, button_color="#3299FF", button_hover_color="#3299FF", fg_color="#3299FF", variable=passwordConfigs.passwordLengthEntryVar)
        self.passwordLengthSlider.grid(row=1, column=1, pady=(5, 0))

        # Password Requirements
        self.passwordRequirementsFrame = CTkFrame(self.configsFrame, fg_color=window.cget("bg"), corner_radius=0)
        self.passwordRequirementsFrame.grid(row=0, column=1, sticky=NSEW)

        self.passwordRequirementsCapitallettersCheckBox = CTkCheckBox(self.passwordRequirementsFrame, text="Großbuchstaben", text_color="#27282b", font=('Arial', 15), variable=passwordConfigs.hasCapitallettersVar, onvalue=True, offvalue=False, fg_color="#3299FF", hover_color="#3299FF", corner_radius=2, checkbox_height=20, checkbox_width=20)
        self.passwordRequirementsCapitallettersCheckBox.grid(row=0, column=0)
        
        self.passwordRequirementsLowercaselettersCheckBox = CTkCheckBox(self.passwordRequirementsFrame, text="Kleinbuchstaben", text_color="#27282b", font=('Arial', 15), variable=passwordConfigs.hasLowercaselettersVar, onvalue=True, offvalue=False, fg_color="#3299FF", hover_color="#3299FF", corner_radius=2, checkbox_height=20, checkbox_width=20)
        self.passwordRequirementsLowercaselettersCheckBox.grid(row=1, column=0, pady=(10, 0))
        
        self.passwordRequirementsDigitsCheckBox = CTkCheckBox(self.passwordRequirementsFrame, text="Ziffern", text_color="#27282b", font=('Arial', 15), variable=passwordConfigs.hasDigitsVar, onvalue=True, offvalue=False, fg_color="#3299FF", hover_color="#3299FF", corner_radius=2, checkbox_height=20, checkbox_width=20)
        self.passwordRequirementsDigitsCheckBox.grid(row=2, column=0, pady=(10, 0))
        
        self.passwordRequirementsSpecialcharactersCheckBox = CTkCheckBox(self.passwordRequirementsFrame, text="Sonderzeichen", text_color="#27282b", font=('Arial', 15), variable=passwordConfigs.hasSpecialcharactersVar, onvalue=True, offvalue=False, fg_color="#3299FF", hover_color="#3299FF", corner_radius=2, checkbox_height=20, checkbox_width=20)
        self.passwordRequirementsSpecialcharactersCheckBox.grid(row=3, column=0, pady=(10, 0))


class PasswordConfigs():

    def __init__(self):
        self.passwordLengthEntryVar = IntVar(value=12)
        self.hasCapitallettersVar = BooleanVar(value=True)
        self.hasLowercaselettersVar = BooleanVar(value=True)
        self.hasDigitsVar = BooleanVar(value=True)
        self.hasSpecialcharactersVar = BooleanVar(value=True)


window = Window()

passwordConfigs = PasswordConfigs()
passwordEntryBox = PasswordEntry()
customisePasswordBox = CustomisePassword()

window.mainloop()