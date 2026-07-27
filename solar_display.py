"""
Vestaboard Solar Production Display
====================================

What this script does, in plain English:
1. Figures out how much solar power is being generated right now
   (currently FAKE/simulated data - see simulate_solar_production() below)
2. Formats that into 3 short lines of text (your Vestaboard Note is
   3 rows x 15 characters)
3. Sends it to your Vestaboard using Vestaboard's Cloud API

This script is designed to run ONCE per execution (fetch data, send to
board, exit). GitHub Actions will call this script automatically every
5 minutes - see .github/workflows/update_board.yml for that part.

WHEN YOU GET YOUR SOLIS API KEY:
Replace the body of simulate_solar_production() with a real call to the
Solis API. Everything else in this file stays the same - build_message()
and send_to_vestaboard() don't care where the numbers came from.
"""

import os
import sys
import math
import random
import datetime
import requests

# The Vestaboard Cloud API always uses this same URL, regardless of
# which board you own.
VESTABOARD_API_URL = "https://cloud.vestaboard.com/"


def get_env_var(name):
    """
    Reads a value out of the environment (never hard-code secrets in
    the script itself). If it's missing, stop with a clear error
    instead of failing in a confusing way later.
    """
    value = os.environ.get(name)
    if not value:
        print(f"ERROR: Missing required environment variable: {name}")
        print("This should be set as a GitHub Secret (see README.md).")
        sys.exit(1)
    return value


def simulate_solar_production():
    """
    FAKE DATA - stands in for the real Solis inverter until you have
    an API key for it.

    Returns a tuple: (current_kw, today_kwh)
      current_kw  - how many kilowatts are being generated right now
      today_kwh   - a rough running total of kilowatt-hours generated today

    The simulation: zero power before sunrise / after sunset, and a
    smooth curve that peaks around solar noon in between, with a
    little random "cloud" noise thrown in so it doesn't look robotic.

    >>> This entire function is what you'll replace later. Everything
    >>> below this function does not need to change. <<<
    """
    now = datetime.datetime.now()
    hour = now.hour + now.minute / 60

    sunrise_hour = 6.5   # 6:30 AM
    sunset_hour = 20.0   # 8:00 PM
    peak_kw = 6.5         # pretend system size, adjust to taste

    if hour < sunrise_hour or hour > sunset_hour:
        current_kw = 0.0
    else:
        day_length = sunset_hour - sunrise_hour
        position_in_day = (hour - sunrise_hour) / day_length  # 0.0 -> 1.0
        current_kw = peak_kw * math.sin(position_in_day * math.pi)
        current_kw *= random.uniform(0.90, 1.0)  # simulate passing clouds
        current_kw = max(current_kw, 0.0)

    # Rough running total for "today" - not a precise integral, just
    # enough to make the second line look realistic.
    if hour <= sunrise_hour:
        today_kwh = 0.0
    else:
        elapsed_fraction = min((hour - sunrise_hour) / (sunset_hour - sunrise_hour), 1.0)
        today_kwh = peak_kw * (sunset_hour - sunrise_hour) * 0.55 * elapsed_fraction

    return round(current_kw, 2), round(today_kwh, 1)


def build_message(current_kw, today_kwh):
    """
    Builds the text that will appear on the board.
    Vestaboard Note = 3 rows, 15 characters each. Keep every line
    at or under 15 characters or Vestaboard will cut it off.
    """
    line1 = "SOLAR OUTPUT"
    line2 = f"NOW: {current_kw}KW"
    line3 = f"TODAY:{today_kwh}KWH"

    for line in (line1, line2, line3):
        if len(line) > 15:
            print(f"WARNING: line exceeds 15 characters and may be cut off: '{line}'")

    return "\n".join([line1, line2, line3])


def send_to_vestaboard(message_text, api_key):
    """
    Sends the message to the Vestaboard Cloud API.
    Docs: https://docs.vestaboard.com/docs/read-write-api/endpoints
    """
    headers = {
        "X-Vestaboard-Token": api_key,
        "Content-Type": "application/json",
    }
    payload = {"text": message_text}

    response = requests.post(
        VESTABOARD_API_URL, json=payload, headers=headers, timeout=15
    )

    if response.status_code == 200:
        print("Success! Message sent to Vestaboard:")
        print(message_text)
    else:
        print(f"ERROR: Vestaboard API returned status {response.status_code}")
        print(response.text)
        sys.exit(1)


def main():
    vestaboard_api_key = get_env_var("VESTABOARD_API_KEY")

    current_kw, today_kwh = simulate_solar_production()
    message = build_message(current_kw, today_kwh)

    print("Prepared message:")
    print(message)
    print("---")

    send_to_vestaboard(message, vestaboard_api_key)


if __name__ == "__main__":
    main()
