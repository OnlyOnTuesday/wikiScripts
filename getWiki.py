from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime
import pdb

class GetWiki(BeautifulSoup):


    def __init__(self, req, dbConn, tableName):
        self.conn = None
        self.db = dbConn
        self.request = req
        self.tableName = tableName

    def getWebPage(self):
        """Use the internet to find content.  Use this when checkDB returns True"""

        request = requests.get(self.request)
        super().__init__(request.content, "html.parser")


    def checkDB(self):
        """Check the database to see if I need to gather information or if I've 
        already gotten it for the day.  Returns True if I need to gather it still,
        False otherwise"""

        #check teh connection to the database and get the latest entry (namely, the day)
        if self.conn is None or self.conn != sqlite3.connect(self.db):
            self.conn = sqlite3.connect(self.db)

        #filter out sql injection, create the sql statement
        #tableName = self.isalnum(self.db[:-3])
        statement = "SELECT * FROM {} ORDER BY date DESC LIMIT 1".format(self.tableName)

        curs = self.conn.cursor()
        curs.execute(statement)
        lastResult = curs.fetchone()
        curs.close()

        #gathers day from database and gets currentDay
        DBDay = int(lastResult[1][8:10])
        currentDay = datetime.datetime.utcnow().day

        # print(lastResult, datetime.datetime.utcnow(), currentDay, DBDay)

        #only need to know if the days are different, not if one's larger
        if currentDay != DBDay:
            print("returned True")
            return True
        else:
            print("returned False")
            return False


    def saveToDB(self):
        """Take the current quote and save it to the database. Checks regardless
        of checkDB to see if the quote already exists in the DB"""

        #check the connection to the database
        if self.conn is None or self.conn != sqlite3.connect(self.db):
            self.conn = sqlite3.connect(self.db)

        #tableName = self.isalnum(self.db[:-3])
        statement = """CREATE TABLE IF NOT EXISTS {}
                    (row1 TEXT, date TEXT)""".format(self.tableName)
        curs = self.conn.cursor()
        curs.execute(statement)

        #determine if the current quote needs to be added, or if it would be
        #redundant
        statement2 = "SELECT * FROM {} ORDER BY date DESC LIMIT 1".format(self.tableName)
        curs.execute(statement2)
        lastResult = curs.fetchone()

        nextResult = (self.content, datetime.datetime.utcnow())
        if lastResult[0] != nextResult[0]:
            addition = (self.content, datetime.datetime.utcnow())
            # statement3 = "INSERT INTO {} VALUES (?, ?), addition".format(self.tableName)
            # curs.execute(statement3, addition)
            curs.execute("INSERT INTO {} VALUES (?, ?)".format(self.tableName), addition)
            self.conn.commit()
            print("committed to database")
            print("Saved to database")

        curs.close()



    def getDB(self):
        """return the entire database's contents"""
        if self.conn is None or self.conn != sqlite3.connect(self.db):
            self.conn = sqlite3.connect(self.db)

        statement = "SELECT * FROM {} ORDER BY date".format(self.isalnum(self.tableName))

        curs = self.conn.cursor()
        curs.execute(statement)
        print(curs.fetchall())

        
    def isalnum(self, table):
        """Function to filter out sql injection.  Only allows alphanumeric characters
        to be returned."""
        badChars = [ "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-",\
                     "+", "=", "/", "?", ">", ".", "<", ",", "{", "}", "[", "]",\
                     ":", ";", "|", "\\", "\"", "'"]
        x = list(filter(lambda x : x not in badChars, list(table)))
        return ''.join(x)


    def getDetails(self):
        """Allows the parent class to find out what content it's dealing with 
        in the child class"""

        print(self.tableName)

        
