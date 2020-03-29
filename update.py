import requests
import maya
import datetime
from os import environ
from dotenv import load_dotenv
load_dotenv()

def get_updates():
  FIGMA_PERSONAL_ACCESS_TOKEN = environ.get('FIGMA_PERSONAL_ACCESS_TOKEN')
  FIGMA_FILE_KEY = environ.get('FIGMA_FILE_KEY')
  FIGMA_API_URL = "https://api.figma.com/v1/files/" + FIGMA_FILE_KEY + "/versions"
  FIGMA_API_HEADERS = { 'X-FIGMA-TOKEN': FIGMA_PERSONAL_ACCESS_TOKEN }

  r = requests.get(url = FIGMA_API_URL, headers = FIGMA_API_HEADERS)
  data = r.json()
  versions = data["versions"]

  filter_function = lambda x: maya.parse(x['created_at']).datetime().date() == datetime.date.today() and x['description'] is not None and len(x['description']) > 0
  todays_versions = list(filter(filter_function, versions))
  if len(todays_versions) > 0:
    message = format_message(todays_versions)
    post_message(message)

def format_message(todays_versions):
  date = datetime.datetime.today()
  message = str(date.month) + "/" + str(date.day) + "\n"

  for version in todays_versions:
    description = version["description"]
    message += "\n" + description

  return message

def post_message(message):
  SLACK_TEAM_ID = environ.get('SLACK_TEAM_ID')
  SLACK_USER_ID = environ.get('SLACK_USER_ID')
  SLACK_CHANNEL_ID = environ.get('SLACK_CHANNEL_ID')
  SLACK_API_URL = "https://hooks.slack.com/services/" + SLACK_TEAM_ID + "/" + SLACK_USER_ID + "/" + SLACK_CHANNEL_ID

  data = { "text": message }
  r = requests.post(url = SLACK_API_URL, json = data)
  print(message)

get_updates()
