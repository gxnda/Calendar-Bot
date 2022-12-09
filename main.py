import tkinter
from Go4Schools_Calendar_Fetcher import *
from cal_setup import get_calendar_service
from datetime import datetime, time, timedelta
import customtkinter as ctk
from tkinter import *
from os import remove


global timetable
root = ctk.CTk()
text_var = tkinter.StringVar()



def ConvertDate(WeekDate):
    # WeekDate = G4S_TimeTable.WeekDate
    StartDate, EndDate = WeekDate.split(" - ")
    StartDate = StartDate.split(", ")[1]
    EndDate = EndDate.split(", ")[1]
    StartDate = StartDate.split()
    EndDate = EndDate.split()
    Months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    for i in range(len(Months)):
        if Months[i] == StartDate[1]:
            StartDate[1] = str(i + 1)
        if Months[i] == EndDate[1]:
            EndDate[1] = str(i + 1)
    StartDate = " ".join(StartDate)
    EndDate = " ".join(EndDate)
    print(StartDate, EndDate)
    # Convert date into DD/M/YYYY
    Converted_StartDate = datetime.strptime(StartDate, "%d %m %Y")
    # print(Converted_StartDate)
    Converted_EndDate = datetime.strptime(EndDate, "%d %m %Y")
    # print(Converted_EndDate)
    return Converted_StartDate, Converted_EndDate


def ConvertTime(Time):
    ConvertedTime = time(int(Time[:2]), int(Time[3:]))
    return ConvertedTime


def DefineColour(title):
    title = str(title)  # idk what integer titles ppl be making but yk
    print((ord(title[0]) % 11) + 1)
    return str(ord(title[0]) % 11 + 1)


def CreateEvent(title, description, start, end, service):
    event_result = service.events().insert(calendarId='primary',
                                           body={"summary": title,
                                                 "description": description,
                                                 "colorId": DefineColour(title),
                                                 "start": {"dateTime": start, "timeZone": 'Greenwich'},
                                                 "end": {"dateTime": end, "timeZone": 'Greenwich'}, }).execute()
    print("created event")
    print(event_result)


def ReplaceToken():  # If this doesn't work, it might be to do with a non-functioning credentials.json
    print("ReplaceToken called")
    try:
        remove("token.pickle")
        print("token.pickle removed")
    except:
        print("token.pickle not found")
    get_calendar_service()  # creates token.pickle (prompts user sign-in)


def Main():

    global timetable
    G4S_TimeTable = TimeTable(timetable)
    print("Fetching calendar service")
    service = get_calendar_service()
    print("Service Fetched")
    WeekDate = G4S_TimeTable.WeekDate
    EventStartDate, EndDate = ConvertDate(WeekDate)
    Days = ["mo", "tu", "we", "th", "fr"]
    for day in range(len(Days)):  # loops through all 5 days
        StartDate = EventStartDate + timedelta(
            days=day)  # adds the correct offset to the start of the week (idk how to word it)
        for period in range(0, 7):  # loops through all 7 periods (0 is form)
            Lesson_Data = G4S_TimeTable.Grab_Period_Data(Days[day], period)  # grabs lesson data
            try:  # adds "null lesson" to form & period 1s bc its broken
                if len(Lesson_Data) == 4:
                    for i in range(2):
                        Lesson_Data.insert(2, "Form")  # adds null lesson names for broken instances
            except:  # will fail if Lesson_Data != List
                pass
            try:  # will fail if not a list (fail if no lesson)
                StartEventTime = ConvertTime(Lesson_Data[0])  # this returns 2 dates
                EndEventTime = ConvertTime(Lesson_Data[1])
                StartCombinedTimeStamp = datetime.combine(StartDate, StartEventTime)  # combines date and time
                EndCombinedTimeStamp = datetime.combine(StartDate, EndEventTime)
                StartCombinedTimeStamp = StartCombinedTimeStamp.isoformat()
                EndCombinedTimeStamp = EndCombinedTimeStamp.isoformat()
                CreateEvent(Lesson_Data[2], Lesson_Data[3] + "\n" + Lesson_Data[4] + "\n" + Lesson_Data[5],
                            StartCombinedTimeStamp, EndCombinedTimeStamp, service)
            except:
                # print("no lesson")
                pass


def CreateWindow():  # This probably should be a class, but I don't wanna have to learn them so deal with it

    def SubmitText():
        global timetable
        timetable = entry.get()
        print(timetable)

    root.title("Go4Schools Timetable Converter")
    photo = PhotoImage(file="g4sicon.png")  # I can't be bothered to put it on the taskbar at the moment
    root.iconphoto(False, photo)

    title = ctk.CTkLabel(root, text="Paste Timetable Below:")
    title.pack(padx=10,pady=10)

    entry = ctk.CTkEntry(root,height=28,width=200)
    entry.pack(padx=60, pady=5)

    label = ctk.CTkLabel(root, text="")
    label.pack(padx=5, pady=5)

    def DoBoth():
        SubmitText()
        try:
            Main()
            label.configure(text="Done!")
        except:
            label.configure(text="Error :(")

    submit = ctk.CTkButton(root, text="Create Events", command=DoBoth)
    submit.pack(padx=60, pady=20,side=BOTTOM)

    Token = ctk.CTkButton(root, text="Regenerate token.pickle", command=ReplaceToken)
    Token.pack(padx=5,pady=5)



    root.mainloop()


CreateWindow()