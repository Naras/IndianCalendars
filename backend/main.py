import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys, os, datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from basicFunctionsGraphsAnimations import basicDictsLists, mappables
import transliterate, config
import jyotish_ganit.panchanga as panchanga
from geopy.geocoders import Nominatim

summary = """
 Indian Calendars Backend API. 
    A REST API to analyse and animate Indian calendar time cycles
"""
description = """
## Features
    A calendar and date/time calculator, mapper and circular time cycles animator for Indian calendars
    i. Entities like days, weeks, months, seasons, zodiac signs, moon phases, asterisms(nakshatra), tithi (15 day cycles)
        with mathematical relationships among them.
    ii. circular rendering (Json) data for a web client to show as circles with segments/spokes. 
    iii. graphs with static and animated double circle depictions.
"""

app = FastAPI(title="Indian Calendars REST API Services",
              docs_url=None if config.settings.env == "production" else "/docs",
              redoc_url=None if config.settings.env == "production" else "/redoc",
              summary=summary, description=description,
              version="0.0.1",
              contact={
                  "name": "Narasimhan M.G",
                  "url": "https://app.iyengarlabs.org",
                  "email": "narasimhanmg@gmail.com",
              },
              license_info={
                  "name": "Apache 2.0",
                  "identifier": "MIT",
              })
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)
@app.get("/api/healthz")
def health_check(): return {"status": "available", "environment": config.settings.env}
@app.get("/api/cycles")
def get_cycles(script: str = "devanagari"):
    def trans(label, scr):
        if not isinstance(label, str): return label
        if scr.lower() != 'devanagari': return transliterate.transliterate(label, scr)
        return label
        
    res = {}
    for k, v in basicDictsLists.items():
        res[k] = {
            "name": trans(k, script),
            "items": [trans(item, script) for item in v]
        }
    return res
@app.get("/api/gears")
def get_gears(cycle1: str, cycle2: str, start1: str = "", start2: str = "", script: str = "devanagari", checkValidMatching: bool=False):
    if cycle1 not in basicDictsLists or cycle2 not in basicDictsLists: raise HTTPException(status_code=400, detail="Cycle not found")
    if checkValidMatching:
        valid, list1, list2 = mappables(cycle1, cycle2)
        if not valid: return {'valid': False, 'gear1': {}, 'gear2': {}}
    else:
        valid, list1, list2 = True, basicDictsLists[cycle1], basicDictsLists[cycle2]
    start1_idx = 0
    if start1 in list1:
        start1_idx = list1.index(start1)
    elif start1.isdigit():
        start1_idx = int(start1) % len(list1)
    start2_idx = 0
    if start2 in list2:
        start2_idx = list2.index(start2)
    elif start2.isdigit():
        start2_idx = int(start2) % len(list2)
    # Apply Transliteration
    def trans(label, scr):
        if not isinstance(label, str): return label
        if scr.lower() != 'devanagari': return transliterate.transliterate(label, scr)
        return label
    items1 = [trans(label, script) for label in list1]
    items2 = [trans(label, script) for label in list2]
    return {
        "valid": valid,
        "gear1": {
            "name": trans(cycle1, script),
            "items": items1,
            "size": len(items1)
        },
        "gear2": {
            "name": trans(cycle2, script),
            "items": items2,
            "size": len(items2)
        },
        "start1_index": start1_idx,
        "start2_index": start2_idx,
        "total_segments": max(len(list1), len(list2))
    }
@app.get('/api/panchanga')
def get_panchanga(name: str, place: str, dob: str):
    geolocator = Nominatim(user_agent=f"my_coordinate_finder_{abs(hash(name)) % 10000}")
    try:
        # Standardize dob format. Handle both space and ISO 'T' separators.
        normalized_dob = dob.replace('T', ' ')
        dob_parts = normalized_dob.split(' ')
        if len(dob_parts) != 2:
            raise ValueError("Expected format 'YYYY/MM/DD HH:MM'")
            
        dobDate, dobTime = dob_parts
        # Support both YYYY-MM-DD and YYYY/MM/DD formats
        dobDate = dobDate.replace('-', '/')
        yyyy, mm, dd = dobDate.split('/')
        hh, mn = dobTime.split(':')
        
        dob_dt = datetime.datetime(int(yyyy), int(mm), int(dd), int(hh), int(mn))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: '{dob}'. Expected 'YYYY/MM/DD HH:MM'. Detail: {str(e)}")

    try:
        chart, panchang = panchanga.chart_panchanga(geolocator, name, place, dob_dt)
        return {
            'name': name,
            'place': place,
            'date': dob,
            'ascendant': chart.d1_chart.houses[0].sign,
            'moon sign': chart.d1_chart.planets[1].sign,
            'nakshatra': chart.panchanga.nakshatra,
            'tithi': panchang.tithi,
            'yoga': panchang.yoga,
            'karana': panchang.karana,
            'vaara': panchang.vaara
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating panchanga: {str(e)}")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
