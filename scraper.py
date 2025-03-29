import requests
import json

API_URL = "https://www.calcareers.ca.gov/CalHrPublic/Search/JobSearchResults"

def fetch_jobs():
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    # API expects POST with criteria
    payload = {
        "page": 1,
        "rpp": 50,
        "sortField": "postingDate",
        "sortOrder": "descending",
        "searchTerm": "",
        "jobType": "all",
        "location": "",
        "department": "",
        "salaryRange": "",
        "classCode": "",
        "workingTitle": "",
        "jobControl": "",
        "finalFilingDate": "",
        "startDate": "",
        "endDate": ""
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise error if response isn't 200
    print("Status code:", response.status_code)
    print("Content preview:", response.text[:500])  # Print first 500 chars

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
