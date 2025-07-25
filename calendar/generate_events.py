
import random
from datetime import datetime, timedelta
from ics import Calendar, Event
import os
import pytz
import argparse

def is_overlapping(start_time, end_time, existing_events):
    """Check if a new event overlaps with any existing events."""
    new_event_range = (start_time, end_time)
    for existing_event in existing_events:
        existing_range = (existing_event['begin'], existing_event['end'])
        if (max(new_event_range[0], existing_range[0]) < 
                min(new_event_range[1], existing_range[1])):
            return True
    return False

def get_domains(args_domains):
    """Gets domains from command-line args or an interactive prompt."""
    if args_domains:
        return [d.strip() for d in args_domains.split(',') if d.strip()]
    
    domains_str = input("Enter a comma-separated list of domains (e.g., domain1.com,domain2.net): ")
    domains = [d.strip() for d in domains_str.split(',') if d.strip()]
    if not domains:
        print("Error: At least one domain must be provided.")
        return None
    return domains

def generate_event_definitions(users, months=6, num_events_range=(20, 40)):
    """Generates a list of event definitions for the given users."""
    user_keys = list(users.keys())
    shared_event_types = [
        "Council Meeting", "Journey Debrief", "Fireworks Planning", "Eagle Summit",
        "Reviewing the Map", "Second Breakfast Strategy"
    ]
    solo_event_types = [
        "Pipe-weed Contemplation", "Reading Ancient Scrolls", "Practicing Smoke Rings", 
        "Mushroom Hunting", "Writing memoirs", "Avoiding Sackville-Bagginses"
    ]
    
    pacific = pytz.timezone('US/Pacific')
    start_date = datetime.now(pacific)
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

            attendee_keys = []
            if len(user_keys) > 1 and random.random() < 0.5:
                attendee_keys = random.sample(user_keys, 2)
                user1_name = users[attendee_keys[0]][0]
                user2_name = users[attendee_keys[1]][0]
                name = random.choice(shared_event_types)
                description = f"{name} for {user1_name} and {user2_name}"
            else:
                solo_user_key = random.choice(user_keys)
                user_name = users[solo_user_key][0]
                name = random.choice(solo_event_types)
                description = f"{name} for {user_name}"
                attendee_keys = [solo_user_key]

            event_definitions.append({
                "name": name, "description": description, "begin": start_time,
                "end": end_time, "location": "Middle-earth", "attendees": attendee_keys
            })
            break
        else:
            print("Warning: Could not find a free slot after max attempts.")
    
    return event_definitions

def create_calendar_from_definitions(event_definitions, domain, users):
    """Creates an ics.Calendar object from event definitions for a specific domain."""
    cal = Calendar()
    for definition in event_definitions:
        e = Event()
        e.name = definition["name"]
        e.description = definition["description"]
        e.begin = definition["begin"]
        e.end = definition["end"]
        e.location = definition["location"]
        
        for attendee_key in definition["attendees"]:
            full_name, prefix = users[attendee_key]
            full_address = f"{full_name} <{prefix}@{domain}>"
            e.add_attendee(full_address)
            
        cal.events.add(e)
        
    return cal

def write_to_ics(calendar, filename):
    """Writes the calendar to a specified .ics file."""
    if not calendar.events:
        print(f"No events to write for {filename}.")
        return
        
    with open(filename, 'w') as f:
        f.write(calendar.serialize())
    print(f"Generated {len(calendar.events)} non-overlapping events and saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fake calendar events.")
    parser.add_argument(
        '--domains', 
        type=str, 
        help='A comma-separated list of domains to generate calendars for (e.g., "example.com,test.org").'
    )
    args = parser.parse_args()

    default_users = {
        "gandalf": ("gandalf the grey", "gandalf"),
        "frodo": ("frodo baggins", "frodo.baggins")
    }

    domains = get_domains(args.domains)
    
    if domains:
        user_names = " and ".join([info[0] for info in default_users.values()])
        print(f"\nGenerating one master list of events for {user_names}...")
        all_event_defs = generate_event_definitions(default_users)
        
        print("\nCreating a personalized calendar file for each user and domain...")
        for domain in domains:
            for user_key, user_info in default_users.items():
                # Filter the event list to only include events for the current user
                user_event_defs = [
                    event for event in all_event_defs if user_key in event["attendees"]
                ]
                
                if not user_event_defs:
                    print(f"No events for {user_info[0]} in domain {domain}. Skipping.")
                    continue

                calendar = create_calendar_from_definitions(user_event_defs, domain, default_users)
                
                script_dir = os.path.dirname(os.path.abspath(__file__))
                os.makedirs(script_dir, exist_ok=True)
                filename = os.path.join(script_dir, f"{user_key}_{domain}.ics")
                write_to_ics(calendar, filename)
                
        print("\nProcess complete.")
