from controller.dateLogic import getTodayDifference
from datetime import date, timedelta
from app import logInPage

## Test getting the dates for updates.
def test_getTodayDifference():
    greaterThanOne = date.today() - timedelta(days = 2)
    lessThanOne = getTodayDifference(date.today())
    notNone = getTodayDifference(greaterThanOne)

    assert notNone != None
    assert lessThanOne == None
