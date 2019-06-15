from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime
import pdb

class GetQuote(BeautifulSoup):

    #TODO: add a gui component of some sort (e.g. open in a separate window    

    #TODO: check to see if we need to fetch the latest quote or if we already have the
    #latest quote.  

    def __init__(self, req):
        self.request = requests.get(req)
        super().__init__(self.request.content, "html.parser")
        self.quote = None #used after the quote has been obtained        
        self.conn = None #used when connecting to the database

    def findQuote(self):
        """Finds the quote in the html and makes it pretty"""

        #wrap the return statement in a print in user code 
        l = []
        quote = self.find_all("table", style="text-align:center; width:100%")
        for i in quote:
            l.append(i.get_text())
        self.quote = ' '.join(l)
        return self.quote

    def saveToDB(self):
        """Take the current quote and save it to the database.  checks regardless 
        of checkDB to see if the quote already exists in the DB"""

        #check the connection to the database
        if self.conn is None or self.conn != sqlite3.connect("wikiQuote.db"):
            self.conn = sqlite3.connect("wikiQuote.db")

        #probably not necessary anymore, came from user code mistake
        if self.quote is None:
            raise Exception("self.quote is None", self.quote)

        curs = self.conn.cursor()
        curs.execute("""CREATE TABLE IF NOT EXISTS quotes
                    (quote TEXT, date TEXT)""")

        #determine if the current quote needs to be added, or if it would be
        #redundant
        curs.execute("SELECT * FROM quotes")
        lastResult = curs.fetchone()
        
        nextResult = (self.quote, datetime.datetime.now())
        if lastResult[0] != nextResult[0]:
            addition = (self.quote, datetime.datetime.now())
            curs.execute("INSERT INTO quotes VALUES (?, ?)", addition)
            self.conn.commit()
        #used for testing
        # else:
        #     print("results are same")
        curs.close()


    def checkDB(self):
        """Check the database to see if I need to gather the quote or if I've 
        already gotten it for the day"""

        #TODO: refactor init code
        #TODO: change the database entries to use utc time

        currentDay = datetime.datetime.utcnow().day

        #check the connection to the database and get latest quote and time
        if self.conn is None or self.conn != sqlite3.connect("wikiQuote.db"):
            self.conn = sqlite3.connect("wikiQuote.db")
        
        curs = self.conn.cursor()
        curs.execute("SELECT * FROM quotes")
        lastResult = curs.fetchone()
        curs.close() #lastResult should persist past the closing of the db

        #gathers the day from the database
        DBDay = lastResult[1].day

        #only need to know if the days are different, not if one's larger
        if currentDay != DBDay:
            return True
        else:
            return False
        
        

x = GetQuote("https://en.wikiquote.org/wiki/Main_Page")
print(x.findQuote())
x.saveToDB()

