import http.client
import urllib
import time
import json

class Notifier:
    """
    pushoverconfig.json in this directory has to look like this:
    {
        "user_key": "YOURUSERKEY",
        "token": "YOURPW"
    }
    """

    def __init__(self, logger: object):
        self.logger = logger
        with open("./notifier/pushoverconfig.json", "r") as configfile:
            data = json.load(configfile)
            self.user_key = data['user_key']
            self.token = data['token']

    def notify_about_new_element_via_pushover(self, site, element_to_write):
        self.logger.log.info("now notifying via pushover api about " + site + " with new element " + element_to_write)
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
        "token": self.token,
        "user": self.user_key,
        "message": "New element on site '" + site + "' found: '" + element_to_write + "'",
        "priority": 0
        }), { "Content-type": "application/x-www-form-urlencoded" })
        resp = conn.getresponse()
        self.logger.log.info("Response to POST to Pushover is: " + resp.read().decode() + "")
        # sleep a second to not overload the api..
        time.sleep(1)

    def notify_about_exception_via_pushover(self, site, exception):
        self.logger.log.info("now notifying via pushover api about exception while processing new element at " + site)
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
        "token": self.token,
        "user": self.user_key,
        "message": "Exception occurred while processing new element on site '" + site + "' : '" + exception + "'",
        "priority": 0
        }), { "Content-type": "application/x-www-form-urlencoded" })
        resp = conn.getresponse()
        self.logger.log.info("Response to POST to Pushover is: " + resp.read().decode() + "")
        # sleep a second to not overload the api..
        time.sleep(1)
