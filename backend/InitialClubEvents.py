from bs4 import BeautifulSoup
import json

# Load and parse the HTML file
with open("formatted_output.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# List to store all event data
events = []

# Locate all event cards by targeting the specific style attribute
cards = soup.find_all("div", style=lambda value: value and "box-sizing: border-box; padding: 10px; width: 50%; height: auto;" in value)

print(f"Found {len(cards)} event cards.")

for card in cards:
    event = {}

    # Extract title
    title_tag = card.find("h3")
    event["title"] = title_tag.text.strip() if title_tag else "No Title Found"

    # Locate the parent div with date/time and location
    date_location_div = card.find("div", style=lambda value: value and "margin-right: 8px; padding: 0.5rem 0px 1rem 1rem; overflow: visible; color: rgb(68, 68, 68); font-size: 0.938rem;" in value)
    if date_location_div:
        # The first div inside this parent should contain the date and time
        date_time_div = date_location_div.find_all("div")[0]
        event["date_time"] = date_time_div.text.strip() if date_time_div else "No Date/Time Found"
        
        # The second div inside this parent should contain the location
        location_div = date_location_div.find_all("div")[1]
        event["location"] = location_div.text.strip() if location_div else "No Location Found"
    else:
        event["date_time"] = "No Date/Time Found"
        event["location"] = "No Location Found"

    # Extract organization name
    org_tag = card.find("span", style=lambda value: value and "width: 91%; display: inline-block;" in value)
    event["organization"] = org_tag.text.strip() if org_tag else "No Organization Found"

    # Extract event image from the background-image style in the div with role="img"
    event_img_tag = card.find("div", role="img")
    if event_img_tag and "background-image" in event_img_tag["style"]:
        style = event_img_tag["style"]
        img_url_start = style.find("url(") + 4
        img_url_end = style.find(")", img_url_start)
        event["event_image"] = style[img_url_start:img_url_end]
    else:
        event["event_image"] = "No Event Image Found"

    # Extract organization image
    org_img_tag = card.find("img", alt=True)
    event["organization_image"] = org_img_tag["src"] if org_img_tag else "No Org Image Found"

    # Append event data to the list
    events.append(event)

# Save data to JSON file
with open("events.json", "w", encoding="utf-8") as json_file:
    json.dump(events, json_file, indent=4)

print("Event data has been saved to events.json")
