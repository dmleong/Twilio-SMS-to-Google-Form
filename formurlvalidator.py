from urlparse import urlparse
from gform import GoogleForm
from enum import Enum

class ValidationFailureReason(Enum):
    NoUrl = 0
    NoGoogleInUrl = 1
    UrlNotForGoogleForm = 2
    UrlForGoogleSpreadsheetNotForm = 3
    GoogleFormDoesntExist = 4
    NoTwilioParametersInForm = 5


twilio_parameters = set(['SmsSid', 'AccountSid', 'From', 'To', 'Body',
                         'FromCity', 'FromState', 'FromZip', 'FromCountry',
                         'ToCity', 'ToState', 'ToZip', 'ToCountry'])

class FormUrlValidator:

    parameters = None
    message = ""
    url = ""
    failureReason = None

    def __init__(self, url):

        self.parameters = None
        self.failureReason = None
        self.message = ""
        self.url = url

    def Validate(self):

        if not self.url:
            self.failureReason = ValidationFailureReason.NoUrl
            return False

        parsed_url = urlparse(self.url)

        if not "https" in parsed_url.scheme:
            self.failureReason = ValidationFailureReason.NoGoogleInUrl
            return False

        if not "google.com" in parsed_url.netloc:
            self.failureReason = ValidationFailureReason.NoGoogleInUrl
            return False

        path_parts = parsed_url.path.split('/')

        self.formkey = path_parts[len(path_parts)-2]
        
        try:
            gform = GoogleForm(self.formkey)

            intersection = twilio_parameters.intersection(gform.labels)
            if intersection == set():
                self.failureReason = ValidationFailureReason.NoTwilioParametersInForm
                return False

            self.parameters = intersection

        except Exception as inst:
            self.failureReason = ValidationFailureReason.GoogleFormDoesntExist
            return False

        return True