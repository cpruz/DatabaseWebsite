import sqlite3
from datetime import datetime, date, timezone

class queries:

    def __init__():
        return

    def connect():
        global con 
        try:
            con = sqlite3.connect("book.db", detect_types=sqlite3.PARSE_DECLTYPES)
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

    def updateBookTitle(bookId, title):
        cur = con.cursor()
        cur.execute("UPDATE Book SET title = :val WHERE bookId = :id", {"val": title, "id": bookId})
        con.commit()
        
    def updateBookLength(bookId, length):
        cur = con.cursor()
        cur.execute("UPDATE Book SET length = :val WHERE bookId = :id", {"val": length, "id": bookId})
        con.commit()

    def updateMember(memberId, phoneNumber):
        cur = con.cursor()
        cur.execute("UPDATE Member SET phoneNumber = :val WHERE memberId = :id", {"val": phoneNumber, "id": memberId})
        con.commit()

    def addAuthor(author):
        cur = con.cursor()
        info = [author.getFirstName(), author.getLastName()]
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
        info = [member.getMemberFirstName(), member.getMemberLastName(), member.getBirthday(), member.getPhoneNumber()]
        cur.execute("INSERT into Member (firstName, lastName, birthday, phoneNumber) values (?,?,?,?)",(info))
        con.commit()

    def makeMemberId(publisher):
        cur = con.cursor()
        cur.execute('SELECT memberId FROM Member WHERE firstName =:fname AND lastName =:lname', \
            {"fname": member.getMemberFirstName(), "lname": member.getMemberLastName()})
        data = cur.fetchall()
        for d in data:
            member.setMemberId(d[0])

    def checkMember(member):
        cur = con.cursor()
        cur.execute('Select count(*) FROM Member WHERE memberId =:num', {"num": member.getMemberId()})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False

    def addWrittenBy(book, author):
        cur = con.cursor()
        info = [book.getBookId(), author.getAuthorId()]
        cur.execute('INSERT into WrittenBy (bookId, authorId) values (?,?)', info)
        con.commit()

    def alreadyWritten(book, author):
        cur = con.cursor()
        cur.execute('SELECT count(*) FROM WrittenBy WHERE bookId=:first AND authorId =:second',\
             {"first": book.getBookId(), "second": author.getAuthorId()})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            print("in else in queries")
            return False

    def addPublishedBy(book, publisher, datePublished):
        cur = con.cursor()
        info = [book.getBookId(), publisher.getPublisherId(), datePublished]
        cur.execute('INSERT into PublishedBy (bookId, publisherId, datePublished) values (?,?,?)', info)
        con.commit()

    def alreadyPublished(book, publisher):
        cur = con.cursor()
        cur.execute('SELECT count(*) FROM PublishedBy WHERE bookId=:first AND publisherId =:second',\
             {"first": book.getBookId(), "second": publisher.getPublisherId()})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False

    def addBorrowedBy(bookId, memberId):
        cur = con.cursor()
        mydate = date.today()
        info = [bookId, memberId, mydate]
        cur.execute('INSERT into BorrowedBy (bookId, memberId, issueDate) values (?,?,?)', info)
        con.commit()

    def removeBorrowedBy(bookId):
        cur = con.cursor()
        info = [bookId]
        cur.execute('DELETE from BorrowedBy WHERE bookId=:first', info)
        con.commit()

    def alreadyBorrowed(bookId):
        cur = con.cursor()
        cur.execute('SELECT count(*) FROM BorrowedBy WHERE bookId=:first',\
             {"first": bookId})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False

    def deleteBook(bookId):
        cur = con.cursor()
        cur.execute("DELETE FROM Book WHERE bookId = ?",bookId)
        con.commit()

    def checkoutBook(bookId):
        cur = con.cursor()
        cur.execute('UPDATE Book SET availability = 0 WHERE bookId=:first', {"first": bookId})
        con.commit()

    def checkinBook(bookId):
        cur = con.cursor()
        cur.execute('UPDATE Book SET availability = 1 WHERE bookId=:first', {"first": bookId})
        con.commit()
    