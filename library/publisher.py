class publisher:

    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.publisherId = None

    def getName(self):
        return self.name

    def getAddress(self):
        return self.address

    def getPublisherId(self):
        return self.publisherId

    def setPublisherId(self, publisherId):
        self.publisherId = publisherId