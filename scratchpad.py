
elif choice == "2":
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    event_name = input("Enter event name to modify: ")
    start_date = input("Enter start date of event to modify (YYYY-MM-DD): ")
    end_date = input("Enter end date of event to modify (YYYY-MM-DD): ")
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date() + timedelta(days=1)

    events_result = service.events().list(calendarId=cal, timeMin=now, maxResults=50, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    matching_events = []
    for event in events:
        if event_name.lower() in event['summary'].lower():
            event_start = datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))).date()
            event_end = datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date'))).date()
            if event_start >= start and event_end <= end:
                matching_events.append(event)

    if not matching_events:
        print(f"No events found matching '{event_name}' between {start_date} and {end_date}.")
    else:
        print(f"Found {len(matching_events)} events matching '{event_name}' between {start_date} and {end_date}:")
        for i, event in enumerate(matching_events):
            event_start = datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))).strftime("%m/%d/%Y")
            event_end = datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date'))).strftime("%m/%d/%Y")
            print(f"{i+1}. {event['summary']} ({event_start} - {event_end})")

        event_numbers = input("Enter event numbers to modify (comma-separated): ")
        events_to_modify = []
        for number in event_numbers.split(','):
            event_number = int(number.strip()) - 1
            events_to_modify.append(matching_events[event_number])

        if not events_to_modify:
            print("No events selected to modify.")
        else:
            print("Selected events to modify:")
            for event in events_to_modify:
                event_start = datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))).strftime("%m/%d/%Y")
                event_end = datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date'))).strftime("%m/%d/%Y")
                print(f"- {event['summary']} ({event_start} - {event_end})")

            confirm = input("Are you sure you want to modify these events? (y/n): ")
            if confirm.lower() == 'y':
                new_event_name = input("Enter new event name: ")
                for event in events_to_modify:
                    event['summary'] = new_event_name
                    updated_event = service.events().update(calendarId=cal, eventId=event['id'], body=event).execute()
                    print(f"Event updated: {updated_event.get('htmlLink')}")
            else:
                print("Events not modified.")



if choice == "1":
    # Prompt user for number of weeks
    num_weeks = int(input("Enter the number of weeks to create the rotation for: "))

    # Get events from the last 4 weeks
    now = datetime.utcnow()
    weeks_ago = now - timedelta(weeks=num_weeks)
    now = now.isoformat() + 'Z'  # 'Z' indicates UTC time
    weeks_ago = weeks_ago.isoformat() + 'Z'

    events_result = service.events().list(calendarId=cal, timeMin=weeks_ago, timeMax=now, maxResults=50, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Create list of start and end dates for each week
    start_dates = []
    end_dates = []
    start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
    for i in range(num_weeks):
        start_dates.append((start_date + timedelta(weeks=i)).strftime('%Y-%m-%d'))
        end_dates.append((start_date + timedelta(days=6, weeks=i)).strftime('%Y-%m-%d'))

    # Create rotation list
    rotation = []
    for i in range(num_weeks):
        week = []
        for j in range(num_chores):
            chore = chores[j]
            person = family_members[(i + j) % num_family_members]
            week.append((chore, person))
        random.shuffle(week)  # Randomize order of chores for each week
        rotation.append(week)

    # Assign chores to dates
    for i, start_date in enumerate(start_dates):
        for j, chore_person in enumerate(rotation[i % len(rotation)]):
            chore, person = chore_person
            end_date = end_dates[i]
            event = {
                'summary': f"{chore} - {person}",
                'start': {'date': start_date},
                'end': {'date': end_date},
                'status': 'busy',
                'reminders': {'useDefault': True},
            }
            service.events().insert(calendarId=cal, body=event).execute()
			
			
			
#working

if choice == "1":
    # Prompt user for number of weeks
    num_weeks = int(input("Enter the number of weeks to create the rotation for: "))

    # Create list of start and end dates for each week
    start_dates = []
    end_dates = []
    start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
    for i in range(num_weeks):
        start_dates.append((start_date + timedelta(weeks=i)).strftime('%Y-%m-%d'))
        end_dates.append((start_date + timedelta(days=6, weeks=i)).strftime('%Y-%m-%d'))

    # Create rotation list
    rotation = []
    for i in range(num_weeks):
        week = []
        for j in range(num_chores):
            chore = chores[j]
            person = family_members[(i + j) % num_family_members]
            week.append((chore, person))
        random.shuffle(week)  # Randomize order of chores for each week
        rotation.append(week)

    # Assign chores to dates
    for i, start_date in enumerate(start_dates):
        for j, chore_person in enumerate(rotation[i % len(rotation)]):
            chore, person = chore_person
            end_date = end_dates[i]
            event = {
                'summary': f"{chore} - {person}",
                'start': {'dateTime': start_date + 'T00:00:00-00:00'},
                'end': {'dateTime': end_date + 'T23:59:59-00:00'},
                'reminders': {'useDefault': True},
            }
            service.events().insert(calendarId=cal, body=event).execute()

    print(f"Chores assigned for the next {num_weeks} weeks.")
	
	