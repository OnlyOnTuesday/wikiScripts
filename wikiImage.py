import sqlite3
import io
from PIL import Image, ImageChops
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
        in the database by the parent class.  This should only be used after 
        findImage has been called"""

        #something doesn't seem right about this code

        image = PIL.Image.frombytes(io.BytesIO(self.image))
        #TODO: add a directory to the beginning of the path
        image.save(path)


    def findImage(self):
        """Fish out the image from the html and return it as a buffer"""

        #go through the tree, ending with a url that can download the image
        imageList = self.find_all("a", {"class" : "image"})
        localImageTag = imageList[2]
        localImageURL = "https:" + localImageTag.contents[0]["src"]

        #the image downloaded as bytes
        self.image = requests.get(localImageURL)
        print("Used Internet")
        return self.image


    def findImageFromDatabase(self):
        """Find the path of the image from the database and use it to return the
        image as a buffer"""

        if self.conn is None or self.conn != sqlite3.connect("wikiImage.db"):
            self.conn = sqlite3.connect("wikiImage.db")

        curs = self.conn.cursor()
        curs.execute("SELECT * FROM paths ORDER BY date DESC LIMIT 1")
        lastResult = curs.fetchone()
        print("Used Database")
        return lastResult[0]
