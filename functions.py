from datetime import datetime 

def db_to_dateTime(string):

    if type(string) == str:
        if len(string)==10: # dan is het een date() object, ipv datetime()
            return datetime.strptime(string, '%Y-%m-%d')
        else:
            return datetime.strptime(string, '%Y-%m-%d_%H:%M')
    else: 
        return 0

def dateTime_to_db(datetimeObject):
    return datetimeObject.strftime('%Y-%m-%d_%H:%M')
