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

        Requires
            regex(string) - A regular expression the returned URLs should match
            
            urlArray(array) - A list of already existing URLs for the function to use
            for duplicate control; defaults to an empty array

        Returns
            urlArray(array) - A list of URLs that is extracted from the Firefox bookmarks
            and history (plus any additional urls passed in via the urlArray argument)

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

    # The database has the URLs in oldest to newest order. I wanted newest to oldest,
    # so we reverse it for that purpose
    urlArray.reverse()

    return urlArray
#end def


def chromeLinkSearch(regex,urlArray=[]):
    """
    Retrieves links from Google Chrome's history matching the provided regex. Does check 
    for duplicates as it assembles the final list. If you have an existing list that you 
    want the function to check for duplicates in and append it's results to, add it in the 
    urlArray argument

        Requires
            regex(string) - A regular expression the returned URLs should match
            
            urlArray(array) - A list of already existing URLs for the function to use
            for duplicate control; defaults to an empty array

        Returns
            urlArray(array) - A list of URLs that is extracted from the Chrome bookmarks
            and history (plus any additional urls passed in via the urlArray argument)

    *** Returns a list of matching URLs ***
    """
    chromeHistoryFile = os.getenv("LocalAppData") + r"\Google\Chrome\User Data\Default\History"

    conn = sql.connect(chromeHistoryFile)
    cursor = conn.cursor()

    for row in cursor.execute("SELECT * from urls"):
        curURL = row[1]

        if re.match(regex,curURL) and curURL not in urlArray:
            urlArray.append(curURL)
        #endif
    #end for

    conn.close()

    # The database has the URLs in oldest to newest order. I wanted newest to oldest,
    # so we reverse it for that purpose
    urlArray.reverse()

    return urlArray
#end def


def ircLogFilesLinkSearch(log_folder,regex,urlArray=[]):
    """
    Searches through a folder of downloaded IRC log files (.txt files) for 
    links matching a certain regex

        Requires
            log_folder - A folder full of .txt files containing downloaded IRC logs

            regex - A regular expression the returned URLs should match
            
            urlArray - A list of already existing URLs for the function to use
            for duplicate control

        Returns
            urlArray (array) - A list of URLs that is extracted from the provided
            IRC logs (plus any additional urls passed in via the urlArray argument)
    """
    file_list = os.listdir(log_folder)

    for file in file_list:
        curFile = os.path.join(log_folder,file)

        if os.path.isfile(curFile):
            file_text = open(curFile,'r',encoding="utf-8")
            index = 0

            for line in file_text:
                # (FUTURE FEATURE???) automatically add [^ \n]+ to the end of the provided regex?
                # This will search for all links in between lines of other tet (???)
                searchIndex = re.search(regex,line) 

                if searchIndex:
                    found_url = line[searchIndex.start():searchIndex.end()]

                    if found_url not in urlArray:
                        urlArray.append(found_url)
                    #endif
                index+=1
            #end for

            # break;
        #endif

    #end for

    # We actually collect the URLs from oldest to newest, and we want the array in
    # the reverse order (nwewest to oldest), so we reverse that array!
    urlArray.reverse()

    return urlArray

#end def

if __name__ == "__main__":
    # # Get Reddit URLs from Firefox
    # reddit_urls = firefoxLinkSearch("https?://(www.)?reddit.com")

    # # Get Reddit URLs from IRC Logs
    # ircLogFolder = os.getenv("USERPROFILE") + r"\Desktop\irc_logs"
    # reddit_urls = ircLogFilesLinkSearch(ircLogFolder,"https?://(www.)?reddit.com[^ \n]+",reddit_urls)

    # print(reddit_urls)

    ytURLS = chromeLinkSearch("https?://(www.)?youtube.com")
    print(ytURLS)
#end def