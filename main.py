import tkinter as tk
import sqlite3

def login(signupwindow):
    signupwindow.destroy()
    def checkLogin():
        con = sqlite3.connect("database.db")
        cursor = con.cursor()

        cursor.execute("SELECT * FROM organisation WHERE id = ? AND email = ? AND password = ?",(organisationEntry.get(), emailEntry.get(), passwordEntry.get()))

        checkDetails = cursor.fetchall()

        if checkDetails:
            loginWindow.destroy()
        else:
            palcehodlerStringVar.set("Invalid details")

    loginWindow = tk.Tk()

    palcehodlerStringVar = tk.StringVar()

    title = tk.Label(loginWindow, text="Stock Management Log In", font=('Helvetica', 12))
    title.pack()
    organisationLabel = tk.Label(loginWindow, text="Enter organisation ID")
    organisationLabel.pack()
    organisationEntry = tk.Entry(loginWindow)
    organisationEntry.pack()
    emailLabel = tk.Label(loginWindow, text="Enter your email")
    emailLabel.pack()
    emailEntry = tk.Entry(loginWindow)
    emailEntry.pack()
    passwordLabel = tk.Label(loginWindow, text="Enter your password")
    passwordLabel.pack()
    passwordEntry = tk.Entry(loginWindow, show="*")
    passwordEntry.pack()
    placeholderLabel = tk.Label(loginWindow, textvariable=palcehodlerStringVar)
    placeholderLabel.pack()
    submitBtn = tk.Button(loginWindow, text="Submit", command=checkLogin)
    submitBtn.pack()

    loginWindow.mainloop()

def signup():
    def checkSignup():
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        givenOrganisation = organisationEntry.get()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS organisation (" \
        "id STRING PRIMARY KEY," \
        "email STRING," \
        "password STRING)")

        cursor.execute("SELECT * FROM organisation WHERE id=?", (givenOrganisation,))

        checkForOrganisation = cursor.fetchall()

        if checkForOrganisation:
            palcehodlerStringVar.set("That organisation ID is already taken")
        else:
            cursor.execute("INSERT INTO organisation (id, email, password) VALUES (?, ?, ?)",
                           (givenOrganisation, emailEntry.get(), passwordEntry.get())
)   
            con.commit()
            con.close()
            signupWindow.destroy()


    signupWindow = tk.Tk()

    palcehodlerStringVar = tk.StringVar()

    title = tk.Label(signupWindow, text="Stock Management Sign Up", font=('Helvetica', 12))
    title.pack()
    organisationLabel = tk.Label(signupWindow, text="Enter organisation ID")
    organisationLabel.pack()
    organisationEntry = tk.Entry(signupWindow)
    organisationEntry.pack()
    emailLabel = tk.Label(signupWindow, text="Enter your email")
    emailLabel.pack()
    emailEntry = tk.Entry(signupWindow)
    emailEntry.pack()
    passwordLabel = tk.Label(signupWindow, text="Enter your password")
    passwordLabel.pack()
    passwordEntry = tk.Entry(signupWindow, show="*")
    passwordEntry.pack()
    placeholderLabel = tk.Label(signupWindow, textvariable=palcehodlerStringVar)
    placeholderLabel.pack()
    submitBtn = tk.Button(signupWindow, text="Submit", command=checkSignup)
    submitBtn.pack()
    loginBtn = tk.Button(signupWindow, text="Already have an account? Log in", command=lambda: login(signupWindow))
    loginBtn.pack()

    signupWindow.mainloop()

signup()