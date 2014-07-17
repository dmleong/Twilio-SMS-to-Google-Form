Receiving SMS messages in a Google Spreadsheet
===================================================

Use Twilio and Google Spreadsheets to build your own applications to do SMS polling / SMS voting, keyword marketing data collection, expense tracking, time tracking, and more.

No programming experience required.

Instructions:
-------------

![An example spreadsheet](http://i.imgur.com/9nTGWdc.png)

Get Started
-----------

1. [Create a Google Form](http://support.google.com/docs/bin/answer.py?hl=en&answer=87809):

	![Create > Form](http://i.imgur.com/YgMYILQ.png)
   
2. Name the form "TwilioSheet" (or any name of your choosing) and select a nice design.

3. Add a new Text question.  Set the Question Title to "SmsSid"

	![Create a Question](http://i.imgur.com/Um5n7pW.png)

4. Repeat step three, adding questions with Question Titles "To", "From" and "Body"  ([other parameters are available as well](http://www.twilio.com/docs/api/twiml/sms/twilio_request)).  This is what your Form should look like:

	![Add additional questions](http://i.imgur.com/N1ZCVvZ.png)

5. If you see an option that reads "Require [Company Name] login to view this form.", uncheck the box for that option.

	![Uncheck required login](http://i.imgur.com/AsBFLcS.png)

6. Once you are done building the form, click the "Send Form" button located in the upper right corner of the webpage:

	![Click Send Form](http://i.imgur.com/wYmlbgJ.png)
   
7. A dialog window will open. Copy the "Link to Share" URL from that window:

	![Copy the Form URL](http://i.imgur.com/VHogL7T.png)

8. Open [TwilioSheet](http://twiliosheet.azurewebsites.net) in a new window.

9. Paste that URL you copied in step 7 into the box on TwilioSheet, then click the "Submit" button.

10. You should get a response from the site saying "It worked!"

11. <a name="copy"></a>Copy that URL.

**Open another browser window.  In that new window:**

1. Log in and go to the "[Numbers](https://www.twilio.com/user/account/phone-numbers)" section of your Twilio account

2. Click on the number you want to set up to send SMS data to your Google Spreadsheet.

3. Paste the URL you [copied above](#copy) into the "SMS Request URL" box for the Twilio number you are configuring.

	![Voice Request URL](http://i.imgur.com/DPyOZ6r.png)

7. Click the "Save Changes" button.

8. Send a text message that says "test" to the number you just set up.

**In your Google Spreadsheet:**

1. Any text message you send to your Twilio number should show up in the Google Spreadsheet you set up after a delay of about 5-10 seconds.

2. Start writing formulas to process the incoming text messages.