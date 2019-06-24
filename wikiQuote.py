from getWiki import GetWiki

class GetQuote(GetWiki):

    def __init__(self, req):

        self.request = req

        #TODO: determine if I need to use the internet or not.
        #maybe set the third param in the parent to a default.

        super().__init__(self.request, "wikiQuote.db", "quotes")


    def sendContent(self):
        """Sends the quote to the parent class, so that it can be saved to the 
        database."""
        self.content = self.quote
        

    def findQuote(self):
        """Fish out the quote from inside the html and return it"""
        
        #how do I access the request from the super class in here?
        l = []
        #find all inherited from BeautifulSoup in GetWiki
        localQuote = self.find_all("table", style="text-align:center; width:100%")
        for i in localQuote:
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
x.getDetails()
#ssx.getDB()
if x.checkDB():
    x.getWebPage()
    print(x.findQuote())
    x.sendContent()
    x.saveToDB()
else:
    print(x.findQuoteFromDatabase())
