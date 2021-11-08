import sqlite3 as sql
import re
import os
import os.path


def firefoxLinkSearch(regex,urlArray=[]):
    """
    Retrieves links from Firefox's history matching the provided regex. Does check for
    duplicates as it assembles the final list. If you have an existing list that you want
    the function to check for duplicates in and append it's results to, add it in the 
    urlArray argument

    *** Requires ***
    regex - A regular expression the returned URLs should match
    urlArray - A list of already existing URLs for the function to use
    for duplicate control

    *** Returns a list of matching URLs ***
    """

    # !!! Need a solution for UNIX systems, instead of just Windows systems
    firefoxDataDir = os.getenv('APPDATA') + r"\Mozilla\Firefox\Profiles"
    profileFolders = os.listdir(firefoxDataDir)

    for profile in profileFolders:
        db_path = os.path.join(firefoxDataDir,profile,"places.sqlite")

        conn = sql.connect(db_path)
        cursor = conn.cursor()

        for row in cursor.execute("SELECT url from moz_places"):
            curURL = row[0]

            if re.match(regex,curURL) and curURL not in urlArray:
                urlArray.append(curURL)
            #end if
        #end for

        conn.close()
    #end for

    return urlArray
#end def

if __name__ == "__main__":
    print( firefoxLinkSearch("https?://(www.)?reddit.com") )
#end def