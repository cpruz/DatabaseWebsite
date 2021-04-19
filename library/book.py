class book:

    def __init__(self, title, length, availability):
        self.title = title
        self.length = length
        self.availability = availability
        self.bookId = None

    def getTitle(self):
        return self.title

    def getLength(self):
        return self.length

    def getAvailabilty(self):
        return self.availability

    def getBookId(self):
        return self.bookId

    def setBookId(self, bookId):
        self.bookId = bookId