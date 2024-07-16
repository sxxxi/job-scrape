from typing import Dict
from careers import fetch_new_jobs, load_old_jobs, compare_job_dictionaries, write_job_dictionary
from chat import eval_jobs, get_email_greeting
from objects import CompanyJobMap
from gmail import send_mail
from yaml import safe_load


RESUME = """
SKILLS
Languages\: Kotlin, Java, TypeScript
Frameworks\: Spring,
Databases\: PostgreSQL, MongoDB
Infrastructures\: Terraform, AWS, Docker, Git, Linux, RabbitMQ Other: Data Structures, Algorithms, Microservices, JWT
"""

def main():
  newList = fetch_new_jobs()
  oldList = load_old_jobs()
  newCompanyJobs = compare_job_dictionaries(oldList, newList)

  if not list_map_empty(newCompanyJobs):
    greeting = get_email_greeting()
    matched = eval_jobs(newCompanyJobs, RESUME)

    matchedJobs = safe_load(matched)

    jobListHtml = ""

    for company in matchedJobs:
      jobListHtml += f"<h3>{company}</h3>"

      jobListHtml += "<ul>"
      for job in matchedJobs[company]:
        jobListHtml += f"<li>{job}</li>"
      jobListHtml += "</ul>"

    contentBody = f"<h2>{greeting}</h2><hr/>{jobListHtml}"

    send_mail("Your Job Alert", contentBody, "html", "akakabeseiji0@gmail.com")
  
  else:
    print("No new jobs found")

  write_job_dictionary(newCompanyJobs)
    

def list_map_empty(lists: CompanyJobMap) -> bool:
  allListEmpty = True
  for listKey in lists:
    if len(lists[listKey]) > 0:
      allListEmpty = False
      break
  return allListEmpty

if __name__ == "__main__":
  main()