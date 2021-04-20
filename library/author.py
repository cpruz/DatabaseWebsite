class author:

    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName
        self.authorId = None

    def getFirstName(self):
        return self.firstName

    def getLastName(self):
        return self.lastName

    def getAuthorId(self):
        return self.authorId

    def setAuthorId(self, authorId):
        self.authorId = authorId