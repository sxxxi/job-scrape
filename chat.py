from openai import OpenAI

from objects import CompanyJobMap
from yaml import dump



def main():
  return

def chat(system: str = "", user: str = "") -> str: 
  return OpenAI().chat.completions.create(
    messages=[
      {
        "role": "system", 
        "content": system      
      },
      {
        "role": "user", 
        "content": user
      },
    ],
    model="gpt-3.5-turbo",
  ).choices[-1].message.content


def get_email_greeting() -> str: 
  return chat(
    system="""You are a sadistic cringe weaboo. Whatever you say are always filthy. Respond with a greeting about 2 sententces long"""
  )



def eval_jobs(companyJobMap: CompanyJobMap, resume: str):
  client = OpenAI()

  dataDump = dump(companyJobMap)

  response = client.chat.completions.create(
    messages=[
      {
        "role": "system", 
        "content": """You are a cringe sadistic weaboo assistant so make your responses as filthy as you can.
        You will be provided the following:
          - A YAML file with the following format:
            <company-1>:
              - Job title 1
              - Job title n
            <company-n>:
              - Job title 1
              - Job title n
          - A resume
        Your response with the YAML file with the format as the input YAML, only containing the job titles that matches the resume. 
        Do not include the company and job at all if you cant find mathching jobs
        """
      },
      {
        "role": "user", 
        "content": f"{dataDump}\n{resume}"
      },
    ],
    model="gpt-3.5-turbo",
  )
  return response.choices[-1].message.content

if __name__ == "__main__":
  main()