import random
from datetime import datetime, timedelta, timezone
from ics import Calendar, Event
import os

def is_overlapping(start_time, end_time, existing_events):
    """Check if a new event overlaps with any existing events."""
    new_event_range = (start_time, end_time)
    for existing_event in existing_events:
        existing_range = (existing_event['begin'], existing_event['end'])
        if (max(new_event_range[0], existing_range[0]) < 
                min(new_event_range[1], existing_range[1])):
            return True
    return False

def get_user_input():
    """Gets domains and users from interactive prompts."""
    domains_str = input("Enter a comma-separated list of domains (e.g., domain1.com,domain2.net): ")
    domains = [d.strip() for d in domains_str.split(',') if d.strip()]
    
    users = {}
    print("Enter user details. Press Enter on an empty name when finished.")
    while True:
        name = input("Enter user's full name (e.g., Gandalf the Grey): ")
        if not name:
            break
        prefix = input(f"Enter email prefix for {name} (e.g., gandalf): ")
        if not prefix:
            print("Prefix cannot be empty. Please try again.")
            continue
        users[name] = prefix
        
    if not domains or not users:
        print("Error: Both domains and users must be provided.")
        return None, None

    return domains, users

def generate_event_definitions(users, months=6, num_events_range=(20, 40)):
    """Generates a list of event definitions using the provided user list."""
    user_keys = list(users.keys())
    shared_event_types = [
        "Project Sync", "Team Meeting", "Planning Session", "Review", "Brainstorming"
    ]
    solo_event_types = [
        "Focus Time", "Prep for meeting", "Task Work", "Code Review", "Documentation"
    ]
    start_date = datetime.now(timezone.utc)
    end_date = start_date + timedelta(days=30 * months)
    business_hours = (9, 17)
    
    event_definitions = []
    max_attempts = 1000

    for _ in range(random.randint(*num_events_range) * months):
        for attempt in range(max_attempts):
            event_day = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            if event_day.weekday() >= 5: continue

            start_hour = random.randint(business_hours[0], business_hours[1] - 2)
            start_time = event_day.replace(hour=start_hour, minute=random.choice([0, 15, 30, 45]), second=0, microsecond=0)
            duration = random.choice([30, 60, 90, 120])
            end_time = start_time + timedelta(minutes=duration)

            if end_time.hour >= business_hours[1]:
                end_time = event_day.replace(hour=business_hours[1], minute=0, second=0, microsecond=0)

            if is_overlapping(start_time, end_time, event_definitions): continue

            # Decide if the event is for a single user or shared
            if len(user_keys) > 1 and random.random() > 0.3: # 70% chance of shared event if possible
                event_type = "shared"
                attendee_keys = random.sample(user_keys, 2) # Pick 2 users for the meeting
            else:
                event_type = "solo"
                attendee_keys = [random.choice(user_keys)]

            if event_type == "shared":
                name = random.choice(shared_event_types)
                description = f"{name} for {attendee_keys[0]} and {attendee_keys[1]}"
            else: # solo
                name = random.choice(solo_event_types)
                description = f"{name} for {attendee_keys[0]}"

            event_definitions.append({
                "name": name, "description": description, "begin": start_time,
                "end": end_time, "location": "Virtual", "attendees": attendee_keys
            })
            break
        else:
            print("Warning: Could not find a free slot after max attempts.")
    
    return event_definitions

def create_calendar_from_definitions(event_definitions, domain, users):
    """Creates an ics.Calendar object from event definitions for a specific domain and user set."""
    cal = Calendar()
    for definition in event_definitions:
        e = Event()
        e.name = definition["name"]
        e.description = definition["description"]
        e.begin = definition["begin"]
        e.end = definition["end"]
        e.location = definition["location"]
        
        for user_name in definition["attendees"]:
            email_prefix = users[user_name]
            full_address = f"{user_name} <{email_prefix}@{domain}>"
            e.add_attendee(full_address)
            
        cal.events.add(e)
        
    return cal

def write_to_ics(calendar, filename):
    """Writes the calendar to a specified .ics file."""
    if not calendar.events:
        print(f"No events to write for {filename}.")
        return
        
    with open(filename, 'w') as f:
        f.write(str(calendar))
    print(f"Generated {len(calendar.events)} non-overlapping events and saved to {filename}")

if __name__ == "__main__":
    domains, users = get_user_input()
    
    if domains and users:
        # 1. Generate a single set of event definitions based on the users
        print("\nGenerating event definitions...")
        event_defs = generate_event_definitions(users)
        
        # 2. Create and write a calendar for each domain
        print("\nCreating calendar files for each domain...")
        for domain in domains:
            calendar = create_calendar_from_definitions(event_defs, domain, users)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            os.makedirs(script_dir, exist_ok=True)
            filename = os.path.join(script_dir, f"events_{domain}.ics")
            write_to_ics(calendar, filename)
        print("\nProcess complete.")