#from bs4 import BeautifulSoup
#import requests
#import sqlite3
#import datetime
#import pdb

# class GetQuote(BeautifulSoup):

#     #TODO: add a gui component of some sort (e.g. open in a separate window (not really a gui))

#     #TODO: check to see if we need to fetch the latest quote or if we already have the
#     #latest quote.  

#     #TODO: Figure out why the class always uses findQuote, instead of findQuoteFromDatabase

#     def __init__(self, req):
#         self.quote = None #used after the quote has been obtained        
#         self.conn = None #used when connecting to the database
#         if self.checkDB():
#             self.request = requests.get(req)
#             super().__init__(self.request.content, "html.parser")
#             print(self.findQuote()) #does putting everything inside the class defeat the 
#         else: #purpose of a class?  Should I re-write this to rely more on the user code?
#             print(self.findQuoteFromDatabase())

#     def findQuote(self):
#         """Finds quote in downloaded html and prettyprints it"""

#         #wrap the return statement in a print in user code 
#         l = []
#         quote = self.find_all("table", style="text-align:center; width:100%")
#         for i in quote:
#             l.append(i.get_text())
#         self.quote = ' '.join(l)
#         print("Used internet")
#         return self.quote

#     def findQuoteFromDatabase(self):
#         """Find the quote if it hasn't been at least a day since the last 
#         quote was gotten from wikiquote"""

#         if self.conn is None or self.conn != sqlite3.connect("wikiQuote.db"):
#             self.conn = sqlite3.connect("wikiQuote.db")

#         curs = self.conn.cursor()
#         curs.execute("SELECT * FROM quotes ORDER BY date DESC LIMIT 1")
#         lastResult = curs.fetchone()
#         print("Used Database")
#         return lastResult[0]

#     def saveToDB(self):
#         """Take the current quote and save it to the database.  checks regardless 
#         of checkDB to see if the quote already exists in the DB"""

#         #pdb.set_trace()

#         #check the connection to the database
#         if self.conn is None or self.conn != sqlite3.connect("wikiQuote.db"):
#             self.conn = sqlite3.connect("wikiQuote.db")

#         #probably not necessary anymore, came from user code mistake
#         if self.quote is None:
#             raise Exception("self.quote is None", self.quote)

#         curs = self.conn.cursor()
#         curs.execute("""CREATE TABLE IF NOT EXISTS quotes
#                     (quote TEXT, date TEXT)""")

#         #determine if the current quote needs to be added, or if it would be
#         #redundant
#         curs.execute("SELECT * FROM quotes ORDER BY date DESC LIMIT 1")
#         lastResult = curs.fetchone()
        
#         nextResult = (self.quote, datetime.datetime.utcnow())
#         if lastResult[0] != nextResult[0]:
#             addition = (self.quote, datetime.datetime.utcnow())
#             curs.execute("INSERT INTO quotes VALUES (?, ?)", addition)
#             self.conn.commit()
#             print("committed to database")
#         #used for testing
#         # else:
#         #     print("results are same")
#         curs.close()
#         print("Saved to DataBase")


#     def checkDB(self):
#         """Check the database to see if I need to gather the quote or if I've 
#         already gotten it for the day.  Returns True if I need to go to wikiquote,
#         False if I don't."""

        

#         currentDay = datetime.datetime.utcnow().day

#         #check the connection to the database and get latest quote and time
#         if self.conn is None or self.conn != sqlite3.connect("wikiQuote.db"):
#             self.conn = sqlite3.connect("wikiQuote.db")
        
#         curs = self.conn.cursor()
#         curs.execute("SELECT * FROM quotes ORDER BY date DESC LIMIT 1")
#         lastResult = curs.fetchone() #DOESN'T FETCH THE LATEST RESULT, ONLY THE TOP ONE (THE FIRST ONE?)
#         curs.close() #lastResult should persist past the closing of the db

#         #gathers the day from the database
#         DBDay = int(lastResult[1][8:10])

#         print(lastResult, datetime.datetime.utcnow(), currentDay, DBDay)
        
#         #only need to know if the days are different, not if one's larger
#         if currentDay != DBDay:
#             print("returned true")
#             return True
#         else:
#             print("returned false")
#             return False

#     def getDB(self):
#         #check the connection to the database
#         if self.conn is None or self.conn != sqlite3.connect("wikiQuote.db"):
#             self.conn = sqlite3.connect("wikiQuote.db")

#         curs = self.conn.cursor()
#         curs.execute("SELECT * FROM quotes ORDER BY date DESC LIMIT 1")
#         for i in curs.fetchall():
#             print(i)

        

# x = GetQuote("https://en.wikiquote.org/wiki/Main_Page")

from getWiki import GetWiki

class GetQuote(GetWiki):

    def __init__(self, req):

        self.request = req

        #TODO: determine if I need to use the internet or not.
        #maybe set the third param in the parent to a default.

        super().__init__(self.request, "wikiQuote.db")


    def sendContent(self):
        self.content = None #when should this be sent to the parent?
        self.tableName = "quotes"

    def findQuote(self):
        """Fish out the quote from inside the html and return it"""
        
        #how do I access the request from the super class in here?
        l = []
        #find all inherited from BeautifulSoup in GetWiki
        quote = self.find_all("table", style="text-align:center; width:100%")
        for i in quote:
            l.append(i.get_text())
        self.quote = ' '.join(l)
        print("Used internet")
        return self.quote
        

    def findQuoteFromDatabase(self):
        """Find the quote if it hasn't been at least a day since the last 
        quote was gotten from wikiquote"""

        #should this method be in the parent class?

        if self.conn is None or self.conn != sqlite3.connect("wikiQuote.db"):
            self.conn = sqlite3.connect("wikiQuote.db")

        curs = self.conn.cursor()
        curs.execute("SELECT * FROM quotes ORDER BY date DESC LIMIT 1")
        lastResult = curs.fetchone()
        print("Used Database")
        return lastResult[0]



x = GetQuote("https://en.wikiquote.org/wiki/Main_Page")
x.sendContent()
x.getDetails()
if x.checkDB():
    x.getWebPage()
    print(x.findQuote())
    x.saveToDB()
else:
    print(x.findQuoteFromDatabase())
