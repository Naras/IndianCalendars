import jyotishganit as jg
from datetime import datetime, timezone
from geopy.geocoders import Nominatim
# For improved performance and control, create and reuse an instance:
from timezonefinder import TimezoneFinder
import zoneinfo

def timzone(place):
    tf = TimezoneFinder(in_memory=True)  # reuse
    query_points = [(13.358, 52.5061), ...]
    for lng, lat in query_points:
        tz = tf.timezone_at(lng=lng, lat=lat)  # 'Europe/Paris'
    return tf, tz
def lat_long(geolocator, address):
    location =  geolocator.geocode(address)
    return location
def ny():
    # 1. Starting with a UTC-aware datetime
    original_dt = datetime(2026, 6, 18, 12, 0, tzinfo=timezone.utc)

    # 2. Convert it to New York time using astimezone
    new_tz = zoneinfo.ZoneInfo("America/New_York")
    modified_dt = original_dt.astimezone(new_tz)

    print(original_dt)  # 2026-06-18 12:00:00+00:00
    print(modified_dt)  # 2026-06-18 08:00:00-04:00 (Time shifts to match the zone)
def zones():
    # Get all available IANA time zones as a set
    zones = zoneinfo.available_timezones()
    # region, city = [zone.split('/')[0] for zone in zones], [zone.split('/')[-1] for zone in zones]
    # Convert to a sorted list
    zone_list = sorted(list(zones))
    print([zone for zone in zone_list if zone in ['Europe/Oslo', 'Asia/Kolkata']])  # Prints the first 10 time zones
def chart_panchanga(geolocator, name, place, dob):
    # Determine the timezone. Default to Asia/Kolkata if lookup/parsing fails.
    zone = "Asia/Kolkata"
    timezone_resolved = False

    # 1. Try to parse timezone string directly from the place input using replacements
    if place:
        try:
            import re
            # Normalize country/state keywords to continent/regions
            parsed_place = place
            replacements = {
                'Norway': 'Europe',
                'Sweden': 'Europe',
                'Denmark': 'Europe',
                'Finland': 'Europe',
                'UK': 'Europe',
                'United Kingdom': 'Europe',
                'Germany': 'Europe',
                'France': 'Europe',
                'Italy': 'Europe',
                'Spain': 'Europe',
                'USA': 'America',
                'United States': 'America',
                'Canada': 'America',
                'Mexico': 'America',
                'Brazil': 'America',
                'Argentina': 'America',
                'India': 'Kolkata, Asia',
                'Australia': 'Australia',
                'Japan': 'Asia',
                'China': 'Asia',
                'Singapore': 'Asia'
            }
            for original, target in replacements.items():
                # Perform case-insensitive replacement
                parsed_place = re.sub(r'\b' + re.escape(original) + r'\b', target, parsed_place, flags=re.I)

            items = [item.strip() for item in parsed_place.split(',')]
            if len(items) >= 2:
                # Replace spaces in city and continent/region with underscores
                continent = items[-1].replace(' ', '_')
                city = items[-2].replace(' ', '_')
                candidate_zone = f'{continent}/{city}'
                
                # Check for standard timezone alternatives if the direct parse is invalid
                timezone_alternatives = {
                    'America/San_Diego': 'America/Los_Angeles',
                    'America/Pittsburgh': 'America/New_York',
                    'America/San_Francisco': 'America/Los_Angeles',
                    'America/Seattle': 'America/Los_Angeles',
                    'America/Boston': 'America/New_York',
                    'America/Washington': 'America/New_York',
                    'America/Houston': 'America/Chicago',
                    'America/Dallas': 'America/Chicago',
                    'America/Atlanta': 'America/New_York',
                    'America/Miami': 'America/New_York',
                    'America/Philadelphia': 'America/New_York',
                }
                
                if candidate_zone in timezone_alternatives:
                    candidate_zone = timezone_alternatives[candidate_zone]
                
                # Validate zone
                zoneinfo.ZoneInfo(candidate_zone)
                zone = candidate_zone
                timezone_resolved = True
        except Exception:
            pass

    # 2. Geolocator query with retries
    location = None
    for attempt in range(3):
        try:
            # We try to geocode the original place input (or zone if place is empty)
            location = geolocator.geocode(place if place else zone, timeout=5)
            if location is not None:
                break
        except Exception as e:
            print(f"Geolocator timed out/failed for {place} (attempt {attempt+1}): {e}")
            if attempt < 2:
                time.sleep(3)

    # 3. Use TimezoneFinder on geocoded coordinates to get precise timezone
    if location is not None:
        latitude, longitude = location.latitude, location.longitude
        try:
            tf = TimezoneFinder(in_memory=True)
            found_zone = tf.timezone_at(lng=longitude, lat=latitude)
            if found_zone:
                zone = found_zone
                timezone_resolved = True
        except Exception as e:
            print(f"TimezoneFinder failed: {e}")
    else:
        # Fallback coordinates for default zone if geocoding failed
        fallback_location = None
        for attempt in range(3):
            try:
                fallback_location = geolocator.geocode(zone, timeout=5)
                if fallback_location is not None:
                    break
            except Exception:
                if attempt < 2:
                    time.sleep(3)
        if fallback_location is not None:
            latitude, longitude = fallback_location.latitude, fallback_location.longitude
        else:
            latitude, longitude = 22.5726, 88.3639

    # 4. Final safety check on zone
    try:
        tz_info = zoneinfo.ZoneInfo(zone)
    except Exception:
        zone = "Asia/Kolkata"
        tz_info = zoneinfo.ZoneInfo(zone)

    # Calculate UTC offset at that local time in the resolved timezone
    try:
        td = tz_info.utcoffset(dob)
        offset = td.total_seconds() / 3600.0
    except Exception:
        offset = 5.5

    chart = jg.calculate_birth_chart(birth_date=dob, latitude=latitude, longitude=longitude, timezone_offset=offset, name=name)
    panchanga = chart.panchanga
    return chart, panchanga
import time
if __name__ == "__main__":
    # zones();ny()
    # Initialize Nominatim API (Set a custom user_agent name)
    geolocator = Nominatim(user_agent="my_coordinate_finder")
    # Enter the address or city name
    names, places = ['Prarthana/Sangeetha', 'Nalini', 'Chim', 'Ramanj', 'Sridhar', 'Pushpa', 'Srinivasan', 'Surya', 'Angeni' ], \
    ['Baerum District, Oslo, Europe', 'Nagarjunakonda, Andhra Pradesh, India', 'Melkote, Mandya, India',
     'Mysore, India', 'Mysore, India', 'Mysore, India', 'Mysore, India',
     'New_York, America', 'Los_Angeles, America']
    dobs = [datetime(1992,4,13, 16, 28), datetime(1960,5,28, 10, 10),
            datetime(1955,12,14, 15, 32),  datetime(1958,4,27,11,12), datetime(1964,10,10,9,34),
            datetime(1933,9,18, 13, 6), datetime(1924,5,25, 11, 5),
            datetime(1996,10,28,14,23), datetime(1999,4,16,10,17)]
    tf = TimezoneFinder(in_memory=True)  # reuse
    print(f'name{' '*19}date of birth{' '*9}place{' '*34}Ascendant{' '*6}Moon Sign{' '*6}Nakshatra{' '*9}Tithi{' '*12}Yoga{' '*7}Karana{' '*6}Vaara')
    # json_writes = {}
    for place, name, dob in zip(places,names,dobs):
        chart, panchanga = chart_panchanga(geolocator, name, place, dob)
        # print(f"{name} {dob} {place} Ascendant: {chart.d1_chart.houses[0].sign} Moon Sign: {chart.d1_chart.planets[1].sign} Nakshatra: {chart.panchanga.nakshatra} Tithi: {panchanga.tithi} Nakshatra: {panchanga.nakshatra} Yoga: {panchanga.yoga} Karana: {panchanga.karana} Vaara: {panchanga.vaara}")
        print(f"{name:19s} {dob}   {place:45s} {chart.d1_chart.houses[0].sign:12s} {chart.d1_chart.planets[1].sign:12s} {chart.panchanga.nakshatra:15s} {panchanga.tithi:19s} {panchanga.yoga:10s} {panchanga.karana:11s} {panchanga.vaara}")
        # json_writes[name] = jg.get_birth_chart_json_string(chart)
    # Save the entire chart as JSON
    # with open("birth_charts.json", "w") as json_file:
    #     for k, v in json_writes.items(): json_file.write(v)