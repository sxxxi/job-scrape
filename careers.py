from os.path import exists
from pathlib import Path
from typing import Dict
from requests import get
from yaml import safe_load, dump
import yaml
from objects import Company, ParseInfo, CompanyJobMap
from chat import eval_jobs


CONFIG    = "config.yaml"
JOB_CACHE = "cache/jobs.yaml"
HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US',
  'Connection': 'keep-alive',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
}
  
def fetch_new_jobs() -> CompanyJobMap:
  companies = load_companies(CONFIG) 
  jobs = {}
  for company in companies:
    response = get(company.url, headers=HEADERS)
    
    if not response.status_code == 200:
      print(f"Cannot fetch from {company.name} [{response.status_code}]")
      continue

    html = response.content
    jobs[company.name] = company.parse_jobs(html)

  return jobs

def load_companies(path: str) -> list[Company]: 
  with open(path, "r") as y:
    config = yaml.safe_load(y)

  companies = config["companies"]
  oCompanies = []

  for company in companies:
    parser = company['parser']
    target = parser["target"]
    try:
      attributes = parser["attributes"]
    except:
      attributes = {}
    oCompany = Company(company["name"], company["url"], ParseInfo(target, attributes))
    oCompanies.append(oCompany)

  return oCompanies

def compare_job_dictionaries(old: CompanyJobMap, new: CompanyJobMap ) -> CompanyJobMap:
  """Return new entries from new dict"""
  old_keys = list(old.keys())
  new_keys = list(new.keys())
  all_keys = set(old_keys + new_keys)
  delta = {}

  """if new key not in old keys, -> user added a new company so just write"""
  for key in all_keys:
    if (key in new_keys and not key in old_keys):
      delta[key] = new[key]
    elif (key in old_keys and not key in new_keys):
      continue
    else:
      if (key == 'bar'):
        print(f"old: {old[key]}\tnew: {new[key]}")
      delta[key] = get_new_entries(old[key], new[key])
  
  return delta

def get_new_entries(old: list, new: list) -> list[any]:
  return list(set(new) - set(old))


def write_job_dictionary(jobs: CompanyJobMap) -> str: 
  yamlContent = dump({
    "jobs": jobs
  })

  Path(JOB_CACHE).parent.mkdir(exist_ok=True, parents=True)
  with open(JOB_CACHE, "w") as file:
    file.write(yamlContent) 

  return yamlContent

def load_old_jobs() -> CompanyJobMap: 
  try:
    with open(JOB_CACHE, "r") as file:
      return safe_load(file)['jobs']
  except FileNotFoundError as err:
    return {}