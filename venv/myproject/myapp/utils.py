import datetime
from urllib.parse import urlencode

def create_google_meeting_link(appointment):
    """
    Create a Google Calendar event link for a given appointment.

    Args:
        appointment (Appointment): The appointment to create a link for.

    Returns:
        str: The Google Calendar event link.
    """
    base_url = "https://www.google.com/calendar/render"

    params = {
        "action": "TEMPLATE",
        "text": f"Appointment with {appointment.therapist.name}",
        "dates": format_dates(appointment.date),
        "details": "Join the meeting: <insert meeting link here>",
    }

    appointment.google_meet_link = base_url + "?" + urlencode(params)
    appointment.save()

def format_dates(date):
    """
    Format the date for a Google Calendar event link.

    Args:
        date (str or datetime.datetime): The date of the event as a string or a datetime object.

    Returns:
        str: The formatted date.
    """
    # Convert the date string to a datetime object if it's not already
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

    # Set a default time for the appointment
    date = date.replace(hour=9)

    # Google Calendar uses the format: 20220101T000000Z
    # Assuming the appointment lasts for 1 hour
    end_time = date + datetime.timedelta(hours=1)
    return date.strftime("%Y%m%dT%H%M%SZ") + "/" + end_time.strftime("%Y%m%dT%H%M%SZ")
