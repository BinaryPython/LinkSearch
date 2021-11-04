import sqlite3 as sql
import re
import os
import os.path


def firefoxLinkSearch(regex):
    """
    Retrieves links from Firefox's history matching the provided regex

    *** Requires ***
    regex - A regular expression the returned URLs should match

    Returns a list of matching URLs
    """
    search_urls = []

    # These are just two different ways to get the same path; basically they both
    # evaluate the directory that the Windows constant %APPDATA% should map to
    #
    # firefoxDataDir = os.path.expandvars(r"%APPDATA%\Mozilla\Firefox\Profiles")
    firefoxDataDir = os.getenv('APPDATA') + r"\Mozilla\Firefox\Profiles"
    profileFolders = os.listdir(firefoxDataDir)

    for profile in profileFolders:
        db_path = os.path.join(firefoxDataDir,profile,"places.sqlite")

        conn = sql.connect(db_path)
        cursor = conn.cursor()

        for row in cursor.execute("SELECT url from moz_places"):
            curURL = row[0]

            if re.match(regex,curURL) and curURL not in search_urls:
                search_urls.append(curURL)
            #end if
        #end for

        conn.close()
    #end for

    return search_urls
#end def

if __name__ == "__main__":
    firefoxLinkSearch("https?://(www.)?reddit.com")
#end def