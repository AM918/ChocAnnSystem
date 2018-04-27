import re as regex
import client
import deb
from service import Service

class DatabaseManager:
    """Handles things pertaining to the stored information."""

    def __init__(self):
        """Initiate clients"""
        self.initClients()
        self.nextMember = 0
        for member in self.members:
            if int(member.number) > self.nextMember:
                self.nextMember = int(member.number)+1
        self.nextProvider = 0

    def getMember(self, number):
        """Returns a member as requested."""
        for member in self.members:
            if member.number == number:
                return member
        return None
    
    def addMember(self, name, street, city, state, zip, email, number = -1):
        """Adds member to database"""
        if number == -1:
            number = self.nextMember
            self.nextMember += 1
        member = client.ChocAnMember(name, number, street, city, state, zip, email, 'Good')
    
    def removeMember(self, number):
        """Removes a member as per the number."""
        # List comprehension:
        # If member number is not equal to a member, remains in list
        self.members = [member for member in self.members if not member.number == number]

    def editMember(self, name, street, city, state, zip, email, number):
        """Edits a member, adds if it doesn't exist."""
        newMember = client.ChocAnClient(name, number, street, city, state, zip, email, 'Good')
        f = True
        for index, member in enumerate(self.members):
        #for member in self.providers:
            if member.number == newMember.number:
                self.members[index] = newMember
                #print('found, updating')
                f = False
                break
        if f == True:
            self.addMember(name, street, city, state, zip, email, number)

    def getProvider(self, number):
        """Gets provider's information"""
       
        # print(number)
        for provider in self.providers:
            # print(provider.number)
            if provider.number == number:
                return provider
        return None

    def addProvider(self, name, street, city, state, zip, email, number = -1):
        """Adds provider."""
        if number == -1:
            number = self.nextProvider
            self.nextProvider += 1
        provider = client.ChocAnProvider(name, number, street, city, state, zip, email, 'Good')
        self.providers.append(provider)

    def removeProvider(self, number):
        """Removes a provider from the database."""
        # List comprehension:
        # If member number is not equal to a member, remains in list
        self.providers = [member for member in self.providers if not member.number == number]

    def editProvider(self, name, street, city, state, zip, email, number):
        """Edits a provider's information or adds a new one if nonexistent."""
        newMember = client.ChocAnProvider(name, number, street, city, state, zip, email, 'Good')
        f = True
        for index, member in enumerate(self.providers):
        #for member in self.providers:
            if member.number == newMember.number:
                self.providers[index] = newMember
                #print('found, updating')
                f = False
                break
        if f == True:
            self.addProvider(name, street, city, state, zip, email, number)

    def addService(self, sDate, iDate, mNum, pNum, code, name, fee):
        """Adds a service to the appropriate member and provider."""
        print ('Adding service with' + 
                ' \nService date: ' + sDate + 
                ' \nInput date: ' + iDate + 
                ' \nMember Number: ' + mNum + 
                ' \nProvider Number: ' + pNum + 
                ' \nCode: ' + str(code) + 
                ', Name: ' + str(name) +
                ', Fee: ' + str(fee))
        mem = self.getMember(mNum)
        prov = self.getProvider(pNum)

        if mem is None:
            deb.warn('Member number was none.')

        if prov is None:
            deb.warn('Provider number was none.')

        service = Service(sDate, iDate, mem, prov, code, name, fee)

        for member in self.members:
            
            if member.number == mNum:
                member.services.append(service)

        for provider in self.providers:
            if provider.number == pNum:
                provider.services.append(service)

    def saveClients(self):
        """Saves clients."""
        deb.debp('Saving all clients.')
        with open("clients.txt", "w") as file:
            for member in self.members:
                # print(member.email)
                file.write('$NAME ' + member.name + '|' +
                '$STATUS ' + 'Member|' + 
                '$NUMBER ' + member.number + '|' + 
                '$STREET ' + member.street + '|' + 
                '$CITY ' + member.city + '|' + 				 
                '$PROV ' + member.state + '|' + 
                '$ZIPCODE ' + member.zip + '|' + 				
                '$EMAIL ' + member.email + '|' +
                '$STAND ' + member.standing + '|\n'
                )
            for member in self.providers:
                file.write('$NAME ' + member.name + '|' +
                '$STATUS ' + 'Provider|' + 
                '$NUMBER ' + member.number + '|' + 
                '$STREET ' + member.street + '|' + 
                '$CITY ' + member.city + '|' + 				 
                '$PROV ' + member.state + '|' + 
                '$ZIPCODE ' + member.zip + '|' + 				
                '$EMAIL ' + member.email + '|' +
                '$STAND ' + member.standing + '|\n'
                )
				
    def initClients(self):
        """Loads clients from clients.txt"""
        self.members = []
        self.providers = []
        # self.undefined = []

        """
        name, number, street, city, state, zip, email
        """
        with open("clients.txt", 'r') as file:
            for line in file: # Another great reason to use Python.
                status = regex.search(r'(\$STATUS[ ]{0,})([^\|]+)', line)
                if status is None:
                    deb.warn('Status was None.')
                    continue
                status = status.groups()[1]
                name = regex.search(r'(\$NAME[ ]{0,})([^\|]+)', line)
                if name is None:
                    deb.warn('Name was None.')
                    continue
                name = name.groups()[1]
                number = regex.search(r'(\$NUMBER[ ]{0,})([^\|]+)', line)
                street = regex.search(r'(\$STREET[ ]{0,})([^\|]+)', line)
                city = regex.search(r'(\$CITY[ ]{0,})([^\|]+)', line)
                province = regex.search(r'(\$PROV[ ]{0,})([^\|]+)', line)
                zipcode = regex.search(r'(\$ZIPCODE[ ]{0,})([^\|]+)', line)
                email_m = regex.search(r'(\$EMAIL[ ]{0,})([^\|]+)', line)
                standing = regex.search(r'(\$STAND[ ]{0,})([^\|]+)', line)
                if number is None:
                    number = 'Undefined'
                else:
                    number = number.groups()[1]
                if street is None:
                    street = 'Undefined'
                else:
                    street = street.groups()[1]
                if city is None:
                    city = 'Undefined'
                else:
                    city = city.groups()[1]
                if province is None:
                    province = 'Undefined'
                else:
                    province = province.groups()[1]
                if zipcode is None:
                    zipcode = 'Undefined'
                else:
                    zipcode = zipcode.groups()[1]
                if email_m is None:
                    email = 'Undefined'
                else:
                    email = (str)(email_m.groups()[1])
                if standing is None:
                    standing = 'Undefined'
                else:
                    standing = standing.groups()[1]
                #deb.debp(number)
                #deb.debp(street)
                #deb.debp(city)
                #deb.debp(province)
                #deb.debp(zipcode)
                #deb.debp(email)
                if regex.search(r'Provider', status, regex.IGNORECASE):
                    self.providers.append(client.ChocAnProvider(name, number, street, city, province, zipcode, email, standing))
                elif regex.search(r'Member', status, regex.IGNORECASE):
                    self.members.append(client.ChocAnMember(name, number, street, city, province, zipcode, email, standing))

    def save():
        """Deprecated. But need this anyways in case of Internet Explorer v3 issues."""
        body=""
        for member in self.members:
            body+="$NAME " + member.name + "|" + \
                  "$STATUS Member|" + \
                  "$NUMBER "  + member.number   + "|" + \
                  "$STREET "  + member.street   + "|" + \
                  "$CITY "    + member.city     + "|" + \
                  "$PROV "    + member.prov     + "|" + \
                  "$ZIPCODE " + member.zip      + "|" + \
                  "$EMAIL "   + member.email    + "|" + \
                  "$STAND "   + member.standing + "|" + "\n"

        for provider in self.providers:
            body+="$NAME " + member.name + "|" + \
                  "$STATUS Provider|" + \
                  "$NUMBER "  + member.number   + "|" + \
                  "$STREET "  + member.street   + "|" + \
                  "$CITY "    + member.city     + "|" + \
                  "$PROV "    + member.prov     + "|" + \
                  "$ZIPCODE " + member.zip      + "|" + \
                  "$EMAIL "   + member.email    + "|" + \
                  "$STAND "   + member.standing + "|" + "\n"

        file = open("clients.txt", "w")
        file.write(body)
        file.close()
