# This Code Was Partially Coded By Daniel Dobromylskyj (Ukrainian Immigrant)
# https://github.com/DanielDobromylskyj


class TimeTable:
    def __init__(self, timetable):
        DateEnd = timetable.find("\n")
        self.WeekDate = timetable[:DateEnd]
        timetable = timetable[DateEnd + 1:]

        Days = SplitIntoDays(timetable)

        SplitDays = []
        for i in range(len(Days)):
            Days[i] = Days[i].split("\n")
            SplitDays.append(FormatDayIntoPeriods(Days[i]))

        for i in range(len(SplitDays)):  # This Loop Modifies All The Time
            for j in range(len(SplitDays[i])):
                Start, End = SplitApartTimes(SplitDays[i][j])
                SplitDays[i][j].pop(0)
                SplitDays[i][j].insert(0, End)
                SplitDays[i][j].insert(0, Start)

        # Declare Vars
        self.data = {}
        self.Period_Table = {
            0: "08:35",
            1: "09:00",
            2: "10:00",
            3: "11:20",
            4: "12:20",
            5: "14:05",
            6: "15:05"
        }

        Days = ["mo", "tu", "we", "th", "fr"]

        i = 0
        for Day in SplitDays:
            self.data[Days[i]] = Day
            i += 1

    def Grab_Period_Data(self, Day, Period):  # maybe add week soon
        try:
            Day = self.data[Day.lower()]
            Time = self.Period_Table[Period]

            for period in Day:
                if Time == period[0]:
                    print(period)
                    return period

            return False
        except KeyError:
            pass
        return None


def SplitIntoDays(timetable):
    DayStarts = [
        timetable.find("Mo\n"),
        timetable.find("Tu\n"),
        timetable.find("We\n"),
        timetable.find("Th\n"),
        timetable.find("Fr\n"),
        len(timetable)
    ]
    Days = []
    # Splits timetable into 5 Days
    for i in range(len(DayStarts)):
        try:
            Days.append(timetable[DayStarts[i] + 3:DayStarts[i + 1] - 1])
        except:
            pass

    return Days


def FormatDayIntoPeriods(Day):
    # takes in each individual day as a 1d list
    data = Day
    Lessons = []
    tmp = []

    for Object in data:  # Goes Though Data
        if (Object.startswith("0") or Object.startswith("1")) and (not ":" in Object and not "/" in Object):
            # If It Starts With a 1 or a 0 & Does Not Contain ':' OR '/'

            tmp.append(Object)  # Add Last Section
            Lessons.append(tmp)  # Add It To The Lessons
            tmp = []  # Clear Tmp Var
        else:
            tmp.append(Object)

    return Lessons


def SplitApartTimes(Day):
    # Day[0] MUST BE THE TIME
    unsplittime = Day[0]
    starttime, endtime = unsplittime[:5], unsplittime[5:]
    return starttime, endtime

# print(Time_Table.Grab_Period_Data("Mo", 2)) # Test Line

# If The Period Is "Free" Or Has No Data It Will Return False If You wish to change the Formatting Of The Period Look
# at the self.Period_Table Dictionary and change the NUMBER (Not String) To Whatever You Want (Doesn't Need To Be
# Integer) And It Will Automatically Work For You

