import requests
from bs4 import BeautifulSoup
from LoginDriver import LoginDriver
import json
import time

class UTClassScraper:
    def __init__(self, cookies):
        self.cookies = {cookie['name']: cookie['value'] for cookie in cookies}
        self.session = requests.Session()
        self.session.cookies.update(self.cookies)

    def get_field_of_study_values(self):
        # Load the main course schedule page to get all field of study (fos_fl) values
        url = "https://utdirect.utexas.edu/apps/registrar/course_schedule/20249/"
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the field of study dropdown
        select = soup.find("select", {"name": "fos_fl"})
        fos_values = [option["value"] for option in select.find_all("option") if option["value"]]
        
        return fos_values

    def scrape_courses(self, fos, level):
        # Start URL for the specific field of study and level
        url = f"https://utdirect.utexas.edu/apps/registrar/course_schedule/20249/results/?fos_fl={fos}&level={level}&search_type_main=FIELD"
        course_data = []

        while url:
            print(f"Scraping URL: {url}")
            response = self.session.get(url)
            if response.status_code != 200:
                print("Failed to fetch the page.")
                break

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the table body containing course schedule data
            table_body = soup.find("tbody")
            if not table_body:
                print("No table body found.")
                break

            rows = table_body.find_all("tr")
            current_course_name = None

            for row in rows:
                # Check if this is a course header row
                course_header = row.find("td", class_="course_header")
                if course_header:
                    # Update current course name
                    current_course_name = course_header.find("h2").text.strip()
                    continue
                
                # Check if the row has standard course data
                unique_td = row.find("td", {"data-th": "Unique"})
                if unique_td:
                    # Primary meeting details with safe access to avoid NoneType errors
                    unique_number = unique_td.text.strip()
                    days = [span.text.strip() for span in row.find("td", {"data-th": "Days"}).find_all("span")] if row.find("td", {"data-th": "Days"}) else []
                    hours = [span.text.strip() for span in row.find("td", {"data-th": "Hour"}).find_all("span")] if row.find("td", {"data-th": "Hour"}) else []
                    rooms = [span.text.strip() for span in row.find("td", {"data-th": "Room"}).find_all("span")] if row.find("td", {"data-th": "Room"}) else []
                    instruction_mode = row.find("td", {"data-th": "Instruction Mode"}).text.strip() if row.find("td", {"data-th": "Instruction Mode"}) else None
                    instructor = row.find("td", {"data-th": "Instructor"}).text.strip() if row.find("td", {"data-th": "Instructor"}) else None
                    status = row.find("td", {"data-th": "Status"}).text.strip() if row.find("td", {"data-th": "Status"}) else None
                    flags = row.find("td", {"data-th": "Flags"}).text.strip() if row.find("td", {"data-th": "Flags"}) else None
                    core = row.find("td", {"data-th": "Core"}).text.strip() if row.find("td", {"data-th": "Core"}) else None

                    # Store the primary meeting details
                    primary_data = {
                        "course_name": current_course_name,
                        "unique_number": unique_number,
                        "days": days[0] if len(days) > 0 else None,
                        "hours": hours[0] if len(hours) > 0 else None,
                        "rooms": rooms[0] if len(rooms) > 0 else None,
                        "instruction_mode": instruction_mode,
                        "instructor": instructor,
                        "status": status,
                        "flags": flags,
                        "core": core
                    }
                    course_data.append(primary_data)

                    # Store additional meeting times if they exist
                    for i in range(1, len(days)):
                        additional_data = primary_data.copy()
                        additional_data["days"] = days[i]
                        additional_data["hours"] = hours[i] if i < len(hours) else None
                        additional_data["rooms"] = rooms[i] if i < len(rooms) else None
                        course_data.append(additional_data)

            # Find the "next" link to continue to the next page if it exists
            next_link = soup.find("a", id="next_nav_link")
            if next_link:
                url = "https://utdirect.utexas.edu" + next_link["href"]
                time.sleep(1)  # Pause to avoid overwhelming the server
            else:
                # No more pages
                url = None

        return course_data

    def save_data(self, all_course_data):
        # Save the data to a JSON file
        with open("ut_courses.json", "w") as f:
            json.dump(all_course_data, f, indent=4)
        print("Data saved to ut_courses.json")

if __name__ == "__main__":
    # Step 1: Log in and get cookies
    login_driver = LoginDriver()
    cookies = login_driver.login()

    # Step 2: Initialize scraper
    scraper = UTClassScraper(cookies)
    
    # Step 3: Get list of field of study values
    field_of_study_values = scraper.get_field_of_study_values()
    
    # Step 4: Iterate over each field of study and level, collect data
    all_course_data = []
    for fos in field_of_study_values:
        for level in ["L", "U", "G"]:
            course_data = scraper.scrape_courses(fos, level)
            all_course_data.extend(course_data)

    # Step 5: Save all collected data
    scraper.save_data(all_course_data)
