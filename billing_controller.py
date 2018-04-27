import datetime
from provider_directory import ProviderDirectory 

class BillingController:
    """Takes care of billing-related concerns."""
    
    def __init__(self, db):
        """Grabs inforamtion from the database about the bill."""
        self.db = db
        self.pDir = ProviderDirectory()

    def verify(self, date, mNum, pNum, code):
        """Bills a service."""
        now = datetime.datetime.now()
        inp = now.strftime("%Y-%m-%d")
        self.db.addService(date, inp, mNum, pNum, code, self.pDir.codes[code][0], self.pDir.codes[code][1]) 




