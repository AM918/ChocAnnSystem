class Service:
    """Service wrapper class."""
    def __init__(self, serviceDate, inputDate, member, provider, code, name, fee):

        self.serviceDate    = serviceDate
        self.inputDate      = inputDate
        self.memberNumber   = member.number
        self.memberName     = member.name
        self.providerNumber = provider.number
        self.providerName   = provider.name
        self.serviceCode    = code
        self.serviceName    = name
        self.fee            = fee
