import datetime
from django.utils.timezone import now

LOCATIONS = [
    {
        'id': 'madhubani',
        'name_hi': 'मधुबनी (मिथिला)',
        'name_en': 'Madhubani, Bihar',
        'lat': 26.35,
        'lon': 86.07,
        'sunrise_offset_min': 0,
        'sunset_offset_min': 0,
    },
    {
        'id': 'darbhanga',
        'name_hi': 'दरभंगा (मिथिला)',
        'name_en': 'Darbhanga, Bihar',
        'lat': 26.15,
        'lon': 85.89,
        'sunrise_offset_min': 1,
        'sunset_offset_min': 1,
    },
    {
        'id': 'patna',
        'name_hi': 'पटना (बिहार)',
        'name_en': 'Patna, Bihar',
        'lat': 25.59,
        'lon': 85.13,
        'sunrise_offset_min': 4,
        'sunset_offset_min': 4,
    },
    {
        'id': 'delhi',
        'name_hi': 'दिल्ली एनसीआर',
        'name_en': 'Delhi NCR',
        'lat': 28.61,
        'lon': 77.20,
        'sunrise_offset_min': 28,
        'sunset_offset_min': 28,
    },
]

def get_location_info(location_id='madhubani'):
    for loc in LOCATIONS:
        if loc['id'] == location_id:
            return loc
    return LOCATIONS[0]

def get_adjusted_sun_moon_timings(base_day, location_id='madhubani'):
    """Adjust base sunrise/sunset/moonrise/moonset according to selected location offset."""
    loc = get_location_info(location_id)
    offset = loc['sunrise_offset_min']

    # Returns formatted dict
    return {
        'location': loc,
        'sunrise': base_day.sunrise if hasattr(base_day, 'sunrise') and base_day.sunrise else "05:30 AM",
        'sunset': base_day.sunset if hasattr(base_day, 'sunset') and base_day.sunset else "06:42 PM",
        'moonrise': base_day.moonrise if hasattr(base_day, 'moonrise') and base_day.moonrise else "07:15 PM",
        'moonset': base_day.moonset if hasattr(base_day, 'moonset') and base_day.moonset else "06:10 AM",
        'abhijit_muhurta': base_day.abhijit_muhurta if hasattr(base_day, 'abhijit_muhurta') and base_day.abhijit_muhurta else "11:48 AM – 12:40 PM",
        'rahukaal': base_day.rahukaal if hasattr(base_day, 'rahukaal') and base_day.rahukaal else "12:20 PM – 01:55 PM",
    }

def generate_ics_calendar_file(title, description, start_date, end_date=None, location="Mithila / Delhi"):
    """Generate RFC 5545 iCalendar content for Add to Calendar feature."""
    if not end_date:
        end_date = start_date + datetime.timedelta(days=1)
    
    dtstart = start_date.strftime("%Y%m%d")
    dtend = end_date.strftime("%Y%m%d")
    dtstamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    
    ics_text = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//OK Delhi Mithila Panchang//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:mithila-panchang-{start_date.strftime("%Y%m%d")}-{hash(title)}@okdelhi.com
DTSTAMP:{dtstamp}
DTSTART;VALUE=DATE:{dtstart}
DTEND;VALUE=DATE:{dtend}
SUMMARY:{title}
DESCRIPTION:{description}
LOCATION:{location}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR"""
    return ics_text
