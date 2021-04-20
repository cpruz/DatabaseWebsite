class member:

    def __init__(self, firstName, lastName, birthday, phoneNumber):
        self.firstName = firstName
        self.lastName = lastName
        self.birthday = birthday
        self.phoneNumber = phoneNumber
        self.memberId = None

    def getMemberFirstName(self):
        return self.firstName

    def getMemberLastName(self):
        return self.lastName

    def getBirthday(self):
        return self.birthday

    def getPhoneNumber(self):
        return self.phoneNumber

    def getMemberId(self):
        return self.memberId

    def setMemberId(self, memberId):
        self.memberId = memberId