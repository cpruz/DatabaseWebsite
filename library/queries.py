import sqlite3

class queries:

    def __init__():
        return

    def connect():
        global con 
        try:
            con = sqlite3.connect("book.db")
        except:
            print("Could no connect")

    def disconnect():
        con.close()

    def addBook(book):
        cur = con.cursor()
        info = [book.getTitle(), book.getLength(), book.getAvailabilty()]
        cur.execute("INSERT into Book (title, length, availability) values (?,?,?)",info)
        con.commit()

    def makeBookId(book):
        cur = con.cursor()
        cur.execute('SELECT bookId FROM Book WHERE title =:tit AND length =:len', {"tit": book.getTitle(), "len": book.getLength()})
        data = cur.fetchall()
        for d in data:
            book.setBookId(d[0])

    def checkBook(book):
        cur = con.cursor()
        cur.execute('Select count(*) FROM Book WHERE bookId =:num', {"num": book.getBookId()})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False

    def addAuthor(author):
        cur = con.cursor()
        info = [author.getFirstName(), book.getLastName()]
        cur.execute("INSERT into Author (firstName, lastName) values (?,?)",(info))
        con.commit()

    def makeAuthorId(author):
        cur = con.cursor()
        cur.execute('SELECT authorId FROM Author WHERE firstName =:first AND lastName =:last', {"first": author.getFirstName(), "last": author.getLastName()})
        data = cur.fetchall()
        for d in data:
            author.setAuthorId(d[0])

    def checkAuthor(author):
        cur = con.cursor()
        cur.execute('Select count(*) FROM Author WHERE firstName =:first AND lastName =:last', {"first": author.getFirstName(), "last": author.getLastName()})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False

    def addPublisher(publisher):
        cur = con.cursor()
        info = [publisher.getName(), publisher.getAddress()]
        cur.execute("INSERT into Publisher (name, address) values (?,?)",(info))
        con.commit()

    def makePublisherId(publisher):
        cur = con.cursor()
        cur.execute('SELECT publisherId FROM Publisher WHERE name =:pname AND address =:addr', {"pname": publisher.getName(), "addr": publisher.getAddress()})
        data = cur.fetchall()
        for d in data:
            publisher.setPublisherId(d[0])

    def checkPublisher(publisher):
        cur = con.cursor()
        cur.execute('Select count(*) FROM Publisher WHERE publisherId =:num', {"num": publisher.getPublisherId()})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False

    def addMember(member):
        cur = con.cursor()
        info = [member.getMemberFirstName(), member.getMemberLastName()]
        cur.execute("INSERT into Member (firstName, lastName) values (?,?)",(info))
        con.commit()

    def makeMemberId(publisher):
        cur = con.cursor()
        cur.execute('SELECT memberId FROM Member WHERE firstName =:fname AND lastName =:lname', \
            {"fname": member.getMemberFirstName(), "lname": member.getMemberLastName()})
        data = cur.fetchall()
        for d in data:
            publisher.setPublisherId(d[0])

    def addWrittenBy(book, author):
        cur = con.cursor()
        info = [book.getBookId(), author.getAuthorId()]
        cur.execute('INSERT INTO WrittenBy (bookId, authorId) values (?,?)', info)
        con.commit()

    def addPublishedBy(book, publisher, datePublished):
        cur = con.cursor()
        info = [book.getBookId(), publisher.getPublisherId()]
        cur.execute('INSERT INTO PublishedBy (bookId, publisherId, datePublished) values (?,?,?)', info, datePublished)
        con.commit()

    def addBorrowedBy(book, member, issueDate):
        cur = con.cursor()
        info = [book.getBookId(), member.getMemberId()]
        cur.execute('INSERT INTO BorrowedBy (bookId, memberId, issueDate) values (?,?,?)', info, issueDate)
        con.commit()