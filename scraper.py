import requests
import json

API_URL = "https://www.calcareers.ca.gov/CalHrPublic/Search/JobSearchResults"

def fetch_jobs():
    params = {
        "page": 1,
        "rpp": 50,
        "sortField": "postingDate",
        "sortOrder": "descending"
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(API_URL, params=params, headers=headers)
    data = response.json()

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
