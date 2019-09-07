'''
This file is for the database manipulator for Tenda
	General layout of script:
		First: function to verify password.
		Second: functions to commit new data to the database.
		Third: functions to get data from the database.
'''

'''
Name: verifyPassword
Description: Function to verify that the password given matches the password in the database.
Inputs: email, password, database cursor.
Outputs: 1 if true, 0 if false.
'''


def verifyPassword(email, testpassword, cur):
    email = "\'"+email+"\'"
    print("Email Check: "+email)
    query = "Select password from User where email="+email+";"
    queryId = "Select user_id from User where email="+email+";"
    cur.execute(query)
    password = str(cur.fetchone())
    cur.execute(queryId)
    userId = str(cur.fetchone())
    password = password.split('\'',2)
    userId = userId[userId.find('(')+1:userId.find(',')]
    print(password[1]+"=="+testpassword)
    print("User ID: "+userId)
    if testpassword == password[1]:
        return userId
    else:
        return 0


def commitAttendenceRecord(user_id, event_id, response, cur, db):
    query = "insert into Event_Statistics(event_id, user_id, response) values('" + \
        event_id+"', '"+user_id+"', \'"+response+"\');"
    cur.execute(query)
    db.commit()


'''
Name: commitInvitationResponse
Description: Function for user to commit a response for event.
Inputs: event_id, user_id, response (either yes or no), database cursor, and database creditals (needed for a commit) 
Outputs: None.
'''


def commitInvitationResponse(event_id, user_id, response, cur, db):
    sql = "Insert Into Events_to_Attendees(event_id, user_id, response) values (" + \
        event_id+", "+user_id+", \'"+response+"\');"
    cur.execute(sql)
    db.commit()


'''
Name: commitEvent
Description: Function for user to commit an event to the database.
Inputs: manager_id, event name, date, time, duration, radius, description, database cursor, db creditials.
Outputs: None.
'''


def commitEvent(manager_id, eventName, eventDate, eventTime, eventDuration, eventRadius, eventDescription, latitude, longitude, cur, db):
    sql = "insert into Event(manager_id, eventName, eventDate, eventTime, eventDuration, eventRadius, eventDescription, latitude, longitude) values (" + \
        manager_id+",'"+eventName+"','"+eventDate+"','"+eventTime+"','"+eventDuration + \
        "','"+eventRadius+"','"+eventDescription+"',"+latitude+","+longitude+");"
    cur.execute(sql)
    db.commit()


'''
Name: getUserID
Description: Function will return userID for the specified email.
Inputs: email and database cursor.
Outputs: returns the user_id belonging to the email.
'''


def getUserID(email, cur):
    query = "Select user_id from User where email=\'"+email+"\';"
    cur.execute(query)
    row = cur.fetchall()
    num = str(row)
    num = num.replace(",", "")
    num = num.replace("(", "")
    num = num.replace(")", "")
    num = num.replace("L", "")
    return num


'''
Name: getUserData
Description: Function gets account data for the specified user_id
Inputs: user_id and database cursor
Outputs: json with firstname, lastname, email address
'''


def getUserData(user_id, cur):
    query = "Select Name, email from User where user_id=" + \
        str(user_id)+";"
    cur.execute(query)
    val = cur.fetchone()
    returnVal = {}
    returnVal["name"] = val[0]
    returnVal["email"] = val[1]
    #returnVal["email"] = val[2]
    return returnVal


'''
Name: getAssociatedEvents
Description: Function gets all events that the specified user_id plans on attending
Inputs: user_id and database cursor.
Outputs: list of event_id
'''


def getAssociatedEvents(user_id, cur):
    query = "Select distinct event_id from Events_to_Attendees where user_id=" + \
        user_id+";"
    cur.execute(query)
    val = cur.fetchall()
    returnVal = {}
    final = []
    for i in val:
        value = str(i[0])
        test = returnVal["event_id"] = value
        final.append(test)
    return final


'''
Name: getManagerAssociatedEvents
Description: Function gets all associated events where the user_id given is the event creator.
Inputs: Manager's user_id and the database cursor.
Outputs: List of events that the user is response for creating.
'''


def getManagerAssociatedEvents(user_id, cur):
    query = "Select distinct event_id from Event where manager_id="+user_id+";"
    cur.execute(query)
    result = cur.fetchall()
    returnVal = {}
    final = []
    for i in result:
        value = str(i[0])
        test = returnVal["event_id"] = value
        final.append(test)
    return final


'''
Name: getEventDetails
Description: Function to get the event details for specified event.
Inputs: event_id and database cursor.
Outputs: json of data for the event.
'''


def getEventDetails(event_id, cur):
    query = "Select eventName, eventDate, eventTime, eventDuration, eventRadius, eventDescription, event_id, longitude, latitude from Event where event_id=" + \
        str(event_id)+";"
    cur.execute(query)
    event = cur.fetchone()
    returnVal = {}
    returnVal["name"] = event[0]
    returnVal["date"] = str(event[1])
    returnVal["time"] = str(event[2])
    returnVal["duration"] = str(event[3])
    returnVal["radius"] = str(event[4])
    returnVal["description"] = str(event[5])
    returnVal["event_id"] = str(event[6])
    returnVal["longitude"] = str(event[7])
    returnVal["latitude"] = str(event[8])
    startTime = returnVal["time"]
    duration = returnVal["duration"]
    return returnVal


def getUsersForEvent(cur, event_id):
    query = "Select distinct(user_id) from Events_to_Attendees where event_id="+event_id+";"
    cur.execute(query)
    users = cur.fetchall()
    returnVal = []
    for user in users:
        returnVal.append(user[0])
    return returnVal


def getUserAttendenceData(cur, event_id, user_id):
    query = "Select max(responseTime) from Events_to_Attendees where user_id=" + \
        str(user_id)+" and event_id="+str(event_id)+";"
    cur.execute(query)
    lastResponseTime = cur.fetchone()
    lastResponseTime = lastResponseTime[0]
    print(lastResponseTime)
    query = "Select Count(*) from Events_to_Attendees where user_id=" + \
        str(user_id)+" and event_id="+str(event_id)+" and response='yes';"

    cur.execute(query)
    numOfResponse = cur.fetchone()
    print(numOfResponse[0])
    duration = numOfResponse[0]-1
    
    #difference = endTime - startTime
    attendenceData = {}
    #attendenceData["start_time"] = str(startTime)
    attendenceData["last_response_time"] = str(lastResponseTime)
    attendenceData["duration"] = str(duration)
    userName = getUserData(user_id, cur)
    attendenceData["user"] = userName
    return attendenceData
