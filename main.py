import json
from tkinter import *
from tkinter import ttk

import requests

class ImportantData:
    USERNAME = ""
    USERID = ""
    USERTOKEN = ""
    class UserInfo:
        NICKNAME = ""
        EMAIL = ""
        AVATARURL = ""
        PLAYERID = 0
        COUNTRY = ""

class LoginState:
    def login_please(self):
        response = requests.post("https://api.tuforums.com/v2/auth/login", json={
            "emailOrUsername": self.username.get(), 
            "password": self.password.get(),
            "remember": self.remember_me.get()
        })

        match response.status_code:
            case 200:
                lastJsonData = json.loads(response.content.decode())

                ImportantData.USERTOKEN = lastJsonData["token"]
                ImportantData.USERNAME = lastJsonData["user"]["username"]
                ImportantData.USERID = lastJsonData["user"]["id"]

                self.status.set(f"Success! Welcome, {ImportantData.USERNAME}")
                user_data = json.loads(requests.get("https://api.tuforums.com/v2/auth/profile/me", headers={"Authorization": f"Bearer {ImportantData.USERTOKEN}"}).content.decode())
                # self.root.quit()
            
            case 400:
                self.status.set("Error: Wrong login info provided?")

            case 401:
                self.status.set("Error: Try again, seems to be internal.")
            
            case 404:
                self.status.set("Error: Site not found. Maybe check your network?")
            
            case _:
                self.status.set(f"Unknown response code.")
        
        self.status.set(self.status.get() + f"\nStatus code: {response.status_code}")
        print(response.content)
    
    def __init__(self):
        self.root = root = Tk()
        root.title("Login to The Universal Forums")

        self.mainframe = mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.username = StringVar()
        username_entry = ttk.Entry(mainframe, width=7, textvariable=self.username)
        username_entry.grid(column=2, row=1, sticky=(W, E))

        self.password = StringVar()
        password_entry = ttk.Entry(mainframe, width=7, textvariable=self.password)
        password_entry.grid(column=2, row=2, sticky=(W, E))

        self.remember_me = BooleanVar()
        ttk.Checkbutton(mainframe, text="Remember me (convenient in a trusted device)", variable=self.remember_me, onvalue=True, offvalue=False, ).grid(column=2, row=3, sticky=(W, E))

        ttk.Button(mainframe, text="Login to TUF", command=self.login_please).grid(column=3, row=4, sticky=W)

        ttk.Label(mainframe, text="Email/Username:").grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="Password:").grid(column=1, row=2, sticky=W)

        self.status = StringVar()
        self.status.set("Status of login will be provided here!")
        ttk.Label(mainframe, textvariable=self.status).grid(column=3, row=6, sticky=E)

        # ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        username_entry.focus()
        # root.bind("<Return>", calculate)

        root.mainloop()

LoginState()