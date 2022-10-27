from datetime import date

def getTodayDifference(dbDate):
    """
        Given a date object this funciton will find the amount of day between the given day and Todays date.
        If the date is less than one day it will return None.
    """
    convertDate = str(dbDate)
    intDateUpdates = convertDate.split('-')
    strToday = str(date.today())
    listToday = strToday.split('-')
    updatesDate = date(int(intDateUpdates[0]), int(intDateUpdates[1]), int(intDateUpdates[2]))
    currentDate = date(int(listToday[0]), int(listToday[1]), int(listToday[2]))

    if (currentDate-updatesDate).days > 1:
        return (currentDate-updatesDate).days
    else:
        return None
