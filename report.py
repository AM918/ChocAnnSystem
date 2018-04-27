import datetime

class Report:

    def __init__(self, client):
        """"Initialize client"""
        self.client = client

    def header(self):
        """Gets the header for a report, generally used by subclasses."""
        return 'Name:\t\t' + self.client.name        + "\n" + \
               'Number:\t\t' + str(self.client.number) + "\n" + \
               'Street:\t\t' + self.client.street      + "\n" + \
               'City:\t\t' + self.client.city        + "\n" + \
               'Province:\t' + self.client.state       + "\n" + \
               'Zipcode:\t' + self.client.zip         + "\n"

class MemberReport(Report):

    def __init__(self, client):
        super().__init__(client)

    def generate(self):
        """Generates the member report."""
        body = self.header()

        for service in self.client.services:
            body += '\nService date:\t' + service.serviceDate   + "\n" + \
                    'Provider Name:\t' + service.providerName  + "\n" + \
                    'Service Name:\t' + service.serviceName   + "\n"

        return body

class ProviderReport(Report):

    def __init__(self, client):
        super().__init__(client)

    def generate(self):
        """Generates the provider report."""
        body = self.header()

        for service in self.client.services:
            body += '\nService Date:\t' + service.serviceDate        + "\n" + \
                    'Input Date:\t\t' + service.inputDate          + "\n" + \
                    'Member:\t\t\t' + service.memberName         + "\n" + \
                    'Number:\t\t\t' + str(service.memberNumber)  + "\n" + \
                    'Code:\t\t\t' + str(service.serviceCode)   + "\n" + \
                    'Fee:\t\t\t' + str(service.fee)           + "\n"

        return body + 'Total Services: ' + str(len(self.client.services)) + \
               "\nTotal fees: $" + str(self.client.getTotal())

class SummaryReport():
    """Summary report class, mostly a wrapper."""
    def __init__(self, providers):
        self.providers = providers

    def generate(self):
        """Generates a summary report."""
        summary = ""
        payout = 0
        for provider in self.providers:
            report = ProviderReport(provider)
            payout  += provider.getTotal()
            summary += report.generate() + "\n"
        return summary + "Total Fees in Report: $" + str(payout)

# Generate report to file
class ReportGeneration:
    """Class for generating reports."""
    def write(self, name, content):
        """Convenience sub-function for writing content to a file."""
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        file = open(name + "-" + date + ".txt", "w")
        file.write(content)
        file.close()

    def printMemberReport(self, member):
        """Prints a member report. member should be a member/client object."""
        report = MemberReport(member)
        self.write(member.name, report.generate()) 

    def printProviderReport(self, provider):
        """Prints a provider report. provider should be a provider/client object."""
        report = ProviderReport(provider)
        self.write(provider.name, report.generate()) 

    def printSummaryReport(self, providers):
        """Prints a summary report.
        Note: providers should be database.providers, the list of all providers.
        """
        report = SummaryReport(providers)
        self.write("Summary", report.generate()) 
