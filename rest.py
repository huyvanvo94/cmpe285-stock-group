POST = 'POST'
GET = 'GET'

ERROR_200 = 200

API_KEY = "SZYE6UUHJIHBIKQ8"
URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"

class RestURL:
    def __init__(self, elem):
        self.elem = elem

    def build(self):

        return "{}&symbol={}&apikey={}".format(URL, self.elem, API_KEY)

def build(elem):

    return "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey=SZYE6UUHJIHBIKQ8".format(elem)
