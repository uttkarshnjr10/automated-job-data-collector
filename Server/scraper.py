import requests
from bs4 import BeautifulSoup
import urllib3
import mysql.connector
from db_config import db_config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# SAVE TO DATABASE 
def save_to_db(job):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM jobs WHERE job_link = %s", (job['link'],))
        if cursor.fetchone():
            print(f"  [Skip] Already exists → {job['title']}")
            return

        cursor.execute("""
            INSERT INTO jobs (title, company, location, job_link)
            VALUES (%s, %s, %s, %s)
        """, (job['title'], job['company'], job['location'], job['link']))

        conn.commit()
        print(f"  [Saved] {job['title']}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print("  [MySQL Error]", err)


#  SCRAPER 
URL = "https://weworkremotely.com/categories/remote-python-jobs"

print(f"Connecting to {URL}...")
response = requests.get(URL, verify=False)
print("Connected. Parsing...\n")

soup = BeautifulSoup(response.text, "lxml")

# selector 
job_cards = soup.select("li.new-listing-container")

print(f"Found {len(job_cards)} jobs.\n")

saved = 0

for card in job_cards:

    try:
        # Title
        title_tag = card.find("h3", class_="new-listing__header__title")
        # Company
        company_tag = card.find("p", class_="new-listing__company-name")
        # Location
        location_tag = card.find("p", class_="new-listing__company-headquarters")
        # Job link
        link_tag = card.find("a", class_="listing-link--unlocked")

        if not (title_tag and company_tag and link_tag):
            continue

        job = {
            "title": title_tag.get_text(strip=True),
            "company": company_tag.get_text(strip=True),
            "location": location_tag.get_text(strip=True) if location_tag else "Remote",
            "link": "https://weworkremotely.com" + link_tag.get("href")
        }

        save_to_db(job)
        saved += 1

    except Exception as e:
        print("  [Error] parsing job:", e)
        continue

print(f"\nFinished! Jobs saved to DB: {saved}")
