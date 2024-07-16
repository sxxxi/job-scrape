import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.mime.text import MIMEText

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

HTML_CONTENT = """
<html>
  <body>
    <script type="application/ld+json">
    {
      "@context":              "http://schema.org",
      "@type":                 "EventReservation",
      "reservationNumber":     "IO12345",
      "underName": {
        "@type":               "Person",
        "name":                "John Smith"
      },
      "reservationFor": {
        "@type":               "Event",
        "name":                "Google I/O 2013",
        "startDate":           "2013-05-15T08:30:00-08:00",
        "location": {
          "@type":             "Place",
          "name":              "Moscone Center",
          "address": {
            "@type":           "PostalAddress",
            "streetAddress":   "800 Howard St.",
            "addressLocality": "San Francisco",
            "addressRegion":   "CA",
            "postalCode":      "94103",
            "addressCountry":  "US"
          }
        }
      }
    }
    </script>
    <p>
      Dear John, thanks for booking your Google I/O ticket with us.
    </p>
    <p>
      BOOKING DETAILS<br/>
      Reservation number: IO12345<br/>
      Order for: John Smith<br/>
      Event: Google I/O 2013<br/>
      Start time: May 15th 2013 8:00am PST<br/>
      Venue: Moscone Center, 800 Howard St., San Francisco, CA 94103<br/>
    </p>
  </body>
</html>

"""

def main():
  return

def send_mail(title, body, mime, to):
  creds = auth("token.json")

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = send_message(service, title, body, to, mime); 
    print(results)

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


def auth(tokenPath: str) -> Credentials: 
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(tokenPath):
    creds = Credentials.from_authorized_user_file(tokenPath, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      flow.redirect_uri = "http://localhost/"
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(tokenPath, "w") as token:
      token.write(creds.to_json())
  return creds


def send_message(service: any, subj: str, msg: str, to: str, frm: str = "dev.sxxxi@gmail.com", mime="html") -> any:
  try:
    message = MIMEText(msg, mime)
    message["To"] = to
    message["From"] = frm
    message["Subject"] = subj

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode() 
    create_message = {"raw": encoded_message}

    send_message = (
      service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')

  except HttpError as err:
    print(f"An error occurred: {err}")
    send_message = None
  return send_message




if __name__ == "__main__":
  main()