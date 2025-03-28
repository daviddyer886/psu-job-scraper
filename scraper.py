import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.calcareers.ca.gov"
LISTING_URL = BASE_URL + "/CalHrPublic/Jobs/JobPostingList.aspx"

def scrape_calcareers():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(LISTING_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    for row in soup.select("tr.DataRow"):
        try:
            title_link = row.select_one("a")
            title = title_link.text.strip()
            link = BASE_URL + title_link.get("href")

            dept = row.select_one("td:nth-child(2)").text.strip()
            location = row.select_one("td:nth-child(3)").text.strip()
            salary = row.select_one("td:nth-child(4)").text.strip()

            jobs.append({
                "title": title,
                "department": dept,
                "location": location,
                "salary": salary,
                "url": link
            })
        except Exception as e:
            print("Error parsing row:", e)

    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

if __name__ == "__main__":
    scrape_calcareers()
