import requests
import json

API_URL = "https://www.calcareers.ca.gov/CalHrPublic/Search/JobSearchResults"

def fetch_jobs():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://www.calcareers.ca.gov",
        "Referer": "https://www.calcareers.ca.gov/",
        "Connection": "keep-alive"
    }

    payload = {
        "page": 1,
        "rpp": 50,
        "sortField": "postingDate",
        "sortOrder": "descending",
        "searchTerm": "",
        "jobType": "all"
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    print("Status code:", response.status_code)
    print("Content preview:", response.text[:500])

    try:
        data = response.json()
    except Exception as e:
        print("Failed to decode JSON:", e)
        return

    jobs = []
    for job in data.get("Results", []):
        jobs.append({
            "title": job.get("JobTitle", "").strip(),
            "department": job.get("Department", "").strip(),
            "location": job.get("JobLocation", "").strip(),
            "salary": job.get("SalaryRange", "").strip(),
            "url": f"https://www.calcareers.ca.gov/CalHrPublic/Jobs/JobPosting.aspx?JobControlId={job.get('JobControlNumber')}",
            "description": job.get("FinalFilingDate", "See posting")
        })

    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

if __name__ == "__main__":
    fetch_jobs()
