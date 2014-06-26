from flask import Flask, request, render_template, url_for, redirect
from urlparse import urlparse
from gform import GForm

app = Flask(__name__)
app.config['DEBUG'] = True

wsgi_app = app

# TO DO:
#   Given a public URL, give a Twilio URL
#   SentFromIP:     IP address that sent the request to this script

twilio_parameters = set(['SmsSid', 'AccountSid', 'From', 'To', 'Body',
                         'FromCity', 'FromState', 'FromZip', 'FromCountry',
                         'ToCity', 'ToState', 'ToZip', 'ToCountry'])

class NoURLException(Exception):
    pass

class NoGoogleInURLException(Exception):
    pass

class URLNotForGoogleFormException(Exception):
    pass

class URLForGoogleSpreadsheetNotFormException(Exception):
    pass

class GoogleFormDoesntExistException(Exception):
    pass

class NoTwilioParametersInFormException(Exception):
    pass

class TestURL:
    def __init__(self, url):

        self.parameters = None
        self.message = ""
        self.url = url
        
        parsed_url = urlparse(url)

        if not "https" in parsed_url.scheme:
            raise NoURLException("No input, expected URL.")

        if not "google.com" in parsed_url.netloc:
            message = "Input URL must contain 'google.com'."
            raise NoGoogleInURLException(message)

        path_parts = parsed_url.path.split('/')

        self.formkey = path_parts[len(path_parts)-2]
        
        try:
            gform = GForm(self.formkey)
        except Exception as inst:

            message = "Error form at URL, " \
                      "does the URL exist and point to a form?"
            raise GoogleFormDoesntExistException(message)

        intersection = twilio_parameters.intersection(gform.labels)
        if intersection == set():
            message = "Form at URL must contain at least " \
                      "one input with a label that matches a Twilio parameter."
            raise NoTwilioParametersInFormException(message)
        self.parameters = intersection


@app.route("/", methods=['GET'])
def index():
    return render_template('base.html', state="nothing-submitted")

@app.route("/", methods=['POST'])
def submit():

    if request.method == 'GET':
        return redirect(url_for('index'))

    valid = False
    message = ''
    form = None
    try:
        form = TestURL(request.form['url'])

        message = "Looks good! " \
                  "Here is the data that will be sent to your spreadsheet:"
        valid = True

        sms_request_url = url_for('form', formkey=form.formkey, _external=True)

    except NoURLException:
        message = "No URL entered. " \
                  'Maybe you just pressed the "Submit" button ' \
                  "without pasting a URL in the input field above?"
    except NoGoogleInURLException:
        message = "There was a problem with the URL, " \
                  "are you sure that you entered the URL " \
                  "for a Google Form?"
    except URLNotForGoogleFormException:
        message = "There was a problem with the URL, " \
                  "are you sure that you entered the URL " \
                  ' for a "live" Google Form?'
    except URLForGoogleSpreadsheetNotFormException:
        message = "That URL appears to be for a Google Spreadsheet, " \
                  "it needs to be for a Google Form."
    except GoogleFormDoesntExistException:
        message = "The URL you entered " \
                  "looks like a valid URL for a Google Form, " \
                  "I'm just having trouble validating it. " \
                  "Perhaps you entered the URL for an example form?"
    except NoTwilioParametersInFormException:
        message = "The URL you entered looks like a valid Google Form, " \
                  "but it doesn't have any inputs for Twilio data. " \
                  "Update your form to accept at least one Twilio parameter " \
                  "and try again."
    except Exception as inst:
        message = "Well, this is embarassing, something went wrong. " \
                  "Perhaps you can try again?" \
                  "{0}".format(inst)
    if valid:
        # Generate the URL that they need to paste on Twilio
        return render_template('base.html',
                               message=message,
                               state="valid-submission",
                               url=form.url,
                               parameters_found=form.parameters,
                               sms_request_url=sms_request_url)
    else:
        return render_template('base.html',
                               message=message,
                               state="error",
                               url=request.form['url'])


# https://docs.google.com
# /spreadsheet/viewform?formkey=aBCdEfG0hIJkLM1NoPQRStuvwxYZAbc2DE#git=0
@app.route("/form/<formkey>", methods=['GET', 'POST'])
def form(formkey):

    gform = GForm(formkey)

    # I could probably re-implement this with fewer lines using sets
    for key in request.values:
        if key in gform.labels:
            name = gform.labels[key]
            gform.parameters[name] = request.values[key]
   
    return gform.submit()

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    import os
    host = os.environ.get('SERVER_HOST', 'localhost')
    try:
        port = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        port = 5555
    app.run(host, port)