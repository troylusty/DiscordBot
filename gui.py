import sqlite3
from tkinter import *

DBFILENAME = "bot.db"

#USE JOIN STATEMENT
#NAME AND ALL MESSAGES

def runGUI():
    window = Tk()
    #window.title(f"{self.bot.user.name} - {self.bot.user.id}")
    window.title("Discord")
    window.geometry("600x200")

    txt = Entry(window, width=10)
    txt.grid(column=0, row=0)

    txt2 = Entry(window, width=10)
    txt2.grid(column=3, row=0)

    def clicked():
        db = sqlite3.connect(DBFILENAME)
        cursor = db.cursor()
        try:
            cursor.execute("SELECT total FROM users WHERE user=?", (txt.get(),))
            totalResult = cursor.fetchone()
            totalResult = int(totalResult[0])
        except:
            totalResult = "error"
        try:
            cursor.execute("SELECT profanity FROM users WHERE user=?", (txt.get(),))
            profanityResult = cursor.fetchone()
            profanityResult = int(profanityResult[0])
            try:
                percentageProfanity = round((profanityResult / totalResult * 100), 2)
            except:
                percentageProfanity = "error"
        except:
            profanityResult = "error"
            percentageProfanity = "error"
        try:
            cursor.execute("SELECT message FROM messages WHERE bool=? AND user=?", (1, txt.get(),))
            profanityMessagesResult = cursor.fetchall()
            profanityMessagesResult = profanityMessagesResult[-5:]
            allMessages = ""
            for i in range(0, len(profanityMessagesResult)):
                allMessages += str(profanityMessagesResult[i])
            allMessages = allMessages.replace("(", "")
            allMessages = allMessages.replace(")", "")
            allMessages = allMessages.replace(",", " ")
        except:
            allMessages = "error"
        db.close()
        resT = f"Total: {totalResult}"
        total.configure(text=resT)
        resP = f"Profanity: {profanityResult}"
        profanity.configure(text=resP)
        resPERC = f"Percentage: {percentageProfanity}%"
        percentage.configure(text=resPERC)
        resTPM = f"Recent profanity: {allMessages}"
        recentprofanity.configure(text=resTPM)

    def clicked2():
        db = sqlite3.connect(DBFILENAME)
        cursor = db.cursor()
        try:
            cursor.execute("SELECT total FROM users WHERE user=?", (txt2.get(),))
            totalResult = cursor.fetchone()
            totalResult = int(totalResult[0])
        except:
            totalResult = "error"
        try:
            cursor.execute("SELECT profanity FROM users WHERE user=?", (txt2.get(),))
            profanityResult = cursor.fetchone()
            profanityResult = int(profanityResult[0])
            try:
                percentageProfanity = round((profanityResult / totalResult * 100), 2)
            except:
                percentageProfanity = "error"
        except:
            profanityResult = "error"
            percentageProfanity = "error"
        try:
            cursor.execute("SELECT message FROM messages WHERE bool=? AND user=?", (1, txt2.get(),))
            profanityMessagesResult = cursor.fetchall()
            profanityMessagesResult = profanityMessagesResult[-5:]
            allMessages = ""
            for i in range(0, len(profanityMessagesResult)):
                allMessages += str(profanityMessagesResult[i])
            allMessages = allMessages.replace("(", "")
            allMessages = allMessages.replace(")", "")
            allMessages = allMessages.replace(",", " ")
        except:
            allMessages = "error"
        db.close()
        resT = f"Total: {totalResult}"
        total2.configure(text=resT)
        resP = f"Profanity: {profanityResult}"
        profanity2.configure(text=resP)
        resPERC = f"Percentage: {percentageProfanity}%"
        percentage2.configure(text=resPERC)
        resTPM = f"Recent profanity: {allMessages}"
        recentprofanity2.configure(text=resTPM)

    btn = Button(window, text="Search", command=clicked)
    btn.grid(column=1, row=0)

    btn2 = Button(window, text="Search", command=clicked2)
    btn2.grid(column=4, row=0)

    total = Label(window, text="Total:")
    total.grid(column=0, row=1)

    total2 = Label(window, text="Total:")
    total2.grid(column=3, row=1)

    profanity = Label(window, text=f"Profanity:")
    profanity.grid(column=0, row=2)

    profanity2 = Label(window, text=f"Profanity:")
    profanity2.grid(column=3, row=2)

    percentage = Label(window, text=f"Percentage:")
    percentage.grid(column=0, row=3)

    percentage2 = Label(window, text=f"Percentage:")
    percentage2.grid(column=3, row=3)

    recentprofanity = Label(window, text=f"Recent profanity:")
    recentprofanity.grid(column=0, row=4)

    recentprofanity2 = Label(window, text=f"Recent profanity:")
    recentprofanity2.grid(column=3, row=4)

    window.iconbitmap("discord.ico")

    window.mainloop()

runGUI()
