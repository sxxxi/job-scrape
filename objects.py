
from dataclasses import dataclass
from typing import Callable, Dict
from bs4 import BeautifulSoup

"""Map<CompanyName, JobTitle[]>"""
CompanyJobMap = Dict[str, list[str]]

@dataclass
class ParseInfo:
  target: str
  attributes: Dict[str, str]

  # def __init__(self, target: str, attributes: Dict[str, str]):
  #   self.target = target
  #   self.attributes = attributes

@dataclass
class Company: 
  name: str
  url: str
  parseInfo: ParseInfo

  # def __init__(self, name: str, url: str, parseInfo: ParseInfo):
  #   self.name = name
  #   self.url = url
  #   self.parseInfo = parseInfo

  def parse_jobs(self, html) -> list[str]:
    soup = BeautifulSoup(html, "lxml")


    if (not self.parseInfo.target.__contains__('>')):
      result = map(lambda x: x.text, soup.find_all('div', attrs=self.parseInfo.attributes))
    
    else:
      result = map(lambda x: x.text, soup.select(self.parseInfo.target))
    
    return list(result)

@dataclass
class Configuration:
  companies: list[Company]

