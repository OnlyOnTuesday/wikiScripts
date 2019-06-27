import sqlite3
import PIL
from datetime import datetime as dt
from getWiki import GetWiki

class WikiImage(GetWiki):

    def __init__(self, req):

        self.request = req
        self.path = str(dt.utcnow().year) + "-" + str(dt.utcnow().month) + \
            "-" + str(dt.utcnow().day) + "-" + "image.png"
        
        super().__init__(self.request, "wikiImage.db", "paths")

    def sendContent(self):
        """Sends the path of the image to the parent class so it can be saved to
        the database."""
        self.content = self.path


    def saveImage(self):
        """Save the image to a file located in a subdirectory.  The path is saved
        in the database by the parent class."""
        

    def findImage(self):
        """Fish out the image from the html and return it as a buffer"""

        if self.conn is None or self.conn != sqlite3.connect("wikiImage.db"):
            self.conn = sqlite3.connect("wikiImage.db")


    def findImageFromDatabase(self):
        """Find the path of the image from the database and use it to return the
        image as a buffer"""

        if self.conn is None or self.conn != sqlite3.connect("wikiImage.db"):
            self.conn = sqlite3.connect("wikiImage.db")

    
