# pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client httplib2
# python3 add_event.py --noauth_local_webserver

# Reference: https://developers.google.com/calendar/quickstart/python
# Documentation: https://developers.google.com/calendar/overview

# Be sure to enable the Google Calendar API on your Google account by following the reference link above and
# download the credentials.json file and place it in the same directory as this file.

from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime

class Calendar:
    
    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = "https://www.googleapis.com/auth/calendar"
        store = file.Storage("token.json")
        # creds = store.get()
        # if(not creds or creds.invalid):
        flow = client.flow_from_clientsecrets("client_secret.json", SCOPES)
        creds = tools.run_flow(flow, store)
        # flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        # credentials = flow.run_console()
        self.service = build("calendar", "v3", http=creds.authorize(Http()))

    def main(self):
        """
        Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user"s calendar.
        """
        # Call the Calendar API.
        now = datetime.utcnow().isoformat() + "Z" # "Z" indicates UTC time.
        print("Getting the upcoming 10 events.")
        events_result = self.service.events().list(calendarId = "primary", timeMin = now,
            maxResults = 10, singleEvents = True, orderBy = "startTime").execute()
        events = events_result.get("items", [])

        if(not events):
            print("No upcoming events found.")
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])
    
    def delete(self, eventID):
        event = self.service.events().get(calendarId='primary', eventId=eventID).execute()
        #If eventID is already deleted.
        if(event.get('status') == "cancelled"):
            print("True, already deleted")
        else:
            #Assume event exists then delete eventID.
            delete = self.service.events().delete(calendarId='primary', eventId=eventID)
            delete.execute()
            print("True, deleted just now")

    def insert(self, car, location, user, startDate, endDate):
        duration = endDate - startDate
        event = {
            "summary": "Car: {} ,booked for {}".format(car, user),
            "location": "{}".format(location),
            "description": "Booked a {} for {} days".format(car, str(duration.days)),
            "start": {
                "date": str(startDate),
                "timeZone": "Australia/Melbourne", 
            },
            "end": {
                "date": str(endDate),
                "timeZone": "Australia/Melbourne",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    { "method": "email", "minutes": 5 },
                    { "method": "popup", "minutes": 10 },
                ],
            }
        }
        event = self.service.events().insert(calendarId = "primary", body = event).execute()
        print("Event created: {}".format(event.get("htmlLink")))
        status = event.get("status")
        print("Event ID: {}".format(status))
        eventID = event.get("id")
        print("Event ID: {}".format(eventID))
        return status, eventID
