import bs4
import webbrowser
import requests
import platform
import pymysql
from datetime import datetime


# Computer project > Name : FastGoogler
# Submitted by ArpitMaurya


#Project Introduction :
# Google searching can also be time consuming and tiresome, therefore this project makes google search more convinient and
# ensures quicker results by crossing out opening time of chrome, websites ,
# therefore a big timesaver for quick google researching.

#> Chrome and Websites are directly opened , no need of wasting time in first searching and then selecting a website.
#> Users can switch to different websites fast if particular site is not sufficient for them
#> Reduces doing stuff manually
#> Can search through big text files and search for user specified inputs
#> Can compare websites which are more likely to contain your result through keyword matching

#https://github.com/ArpitMaurya01



#global init mysql db

db = pymysql.connect("localhost", "root", 'doraemon')
date = datetime.today().strftime('%Y-%m-%d')
mycursor = db.cursor()

mycursor.execute("SHOW DATABASES")


def commit_history(url):
    query = """INSERT INTO history (siteurl,date) VALUES ('%s','%s');""" % (url, str(date))
    mycursor.execute(query)
    db.commit() #saving the changes made

def start_historydb():

    # for checking if the program is run for the first time or not , if database not exists ,
    # its the first time , and
    # this method will create it
    # and move cursor to use history table for both conditions

    i = 0
    l = []
    for x in mycursor:
        l.append(str(x).translate({ord(','): None, ord('('): None, ord(')'): None, ord("'"): None})) #this removes the circular bracktes and comma from the sql output

    if (l.__contains__('fgt2020historydbb')):
        print(">Welcome Back!")
        mycursor.execute("USE fgt2020historydbb;")

    else:
        print("\n>Setting up FGT for the first time start...")
        print(">Creating a history database...")
        try:
            mycursor.execute("CREATE DATABASE fgt2020historydbb;")
            mycursor.execute("USE fgt2020historydbb;")

            sql_command = """
                CREATE TABLE history ( 
                serial INTEGER AUTO_INCREMENT, 
                siteurl VARCHAR(2000),  
                date DATE ,
                PRIMARY KEY (serial) 
                );
                """

            mycursor.execute(sql_command)

            print("> A History table was created successfully...")
            print(">Welcome to FGT.")


        except:
            print("Error initializing .... History feature will not work untill next restart.")

def showhistory():
    print("\n>SHOWING HISTORY :")
    mycursor.execute("SELECT * FROM history;")
    for i in mycursor:
        print("> ", i)

    inp = input("Back to searching enter to continue ...?")
    print(
        "\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>( History Closed! )<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    rep()



def SST(paper,n , path):
    d = []
    m = 0
    s = ''
    file = open(paper, 'r', encoding="utf-8") #using utf8 as text files can be big , once got an error in this , as default encoding was not sufficient..

    # algorithm for extracting the parts(or input) user need to search from a text file,
    # for example he can put whole paragaph in a that text file and
    #seperate each input by using '{' and '}'
    # for example : hello world {alok123} seesefsopi efs  ----> only alok123 will be cut and stored in the
    # list for later searching.

    print("Starting Sour-Soup-Algorithm....")
    print(">Make Sure the file is in same directory as of this program...")
    print(">Text File Selected : ",paper)
    print("\n>>>>>>>>>>>>>>>>>(  >>Thread Started<< )=======================================>")
    text = file.read().replace('\n', " ")
    for i in range(0, len(text)):
        if (text[i] == '{'):
            j = i + 1

            while (text[j] != '}' and j < len(text)):
                s += "" + text[j]
                j = j + 1
            d.append(s)
            s = ''
            m += 1
            i = j

    file.close()

    chrome_path = path

    for i in range(0, len(d)):
        print("Searching For Part :",d[i])
        res = requests.get('https://google.com/search?q=' + d[i])
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser") # html.parser for parsing out the tag classes like div , a etc ...
        linkElements = soup.select('div#main > div > div > div > a')
        linkToOpen = min(n, len(linkElements))
        # print(linkElements)

        print("\nOpening Chrome and Showing ", n, " results")

        # chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\Application\chrome.exe"

        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path)) #used for refgistering chrome and chrome path

        # os.system(r'C:\\Program Files (x86)\\Google\\Chrome\Application\chrome.exe')

        #linkElements is the whole web part , so for extracting the url(href or hyperlink) from it we use , get()
        l = input("Press Enter to Start Opening :")
        for i in range(linkToOpen):
            webbrowser.get('chrome').open('https://google.com' + linkElements[i].get('href')) #get chrome and open the url
            commit_history('https://google.com' + linkElements[i].get('href')) # saving the search history in the db
        print("\n==============( A Task Completed)==========>>> ")



def keywordSearch():
    # this algorithm gives how much keywords were matched on a particular site compared to input
    inp = input("Search For : ")
    keywords = input("Keywords :").split()
    print(keywords)
    print("Searching please wait....")
    res = requests.get('https://google.com/search?q=' + inp) # for searching anything on google ,
    # https://google.com/search?q= this is used , so sites will open with google

    # here res is returning me results from google in form of urls , say top 15 results and saving them in list and of that only first N urls I will open

    res.raise_for_status() # for error handling (raises error if something bad happen..)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    linkElements = soup.select('div#main > div > div > div > a')
    linkToOpen = min(15, len(linkElements)) #

    for i in range(linkToOpen):
        count = 0
        l = []
        url = 'https://google.com' + linkElements[i].get('href')
        commit_history('https://google.com' + linkElements[i].get('href'))
        print(">Trying on :" + url)
        for j in range(0, len(keywords)):

            if (keywords[j] in requests.get(url).text):
                # print("Keyword Matched :"+keywords[j])
                l.append(keywords[j])
                count += 1

        print(count, " Keywords Matched :", l)



def takeinput():
    text = ""
    stopword = "/end"
    while True:
        line = input()
        if line.strip() == stopword:
            break
        text += "%s\n" % line
    return text

def StandardSearch(n , path):
    print("\n>Google Search : ", end=" ")
    inp = takeinput()
    res = requests.get('https://google.com/search?q=' + inp)

    # print("Res :",requests.get('https://google.com/search?q=narendra').text)

    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    linkElements = soup.select('div#main > div > div > div > a')
    linkToOpen = min(n, len(linkElements))
    # print(linkElements)

    print("\nOpening Chrome and Showing ", n, " results")


    #chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\Application\chrome.exe"

    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(path))

    # os.system(r'C:\\Program Files (x86)\\Google\\Chrome\Application\chrome.exe')
    for i in range(linkToOpen):
        webbrowser.get('chrome').open('https://google.com' + linkElements[i].get('href'))
        commit_history('https://google.com' + linkElements[i].get('href'))

    print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>( One Thread Closed! )<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

def paperinp():
    # text file name
    inp = input("\nFile Name :")+".txt"
    return inp


def choose_algorithm(argument, n, path):

    # choosing algorithms

    if(argument =='s'):
        StandardSearch(n,path)
    elif(argument == 'k'):
        keywordSearch()
    elif(argument == 't'):
        SST(paperinp(),n , path)
    elif(argument == 'h'):
        showhistory()

def rep():
    arch = platform.architecture()[0]
    if (arch == "32bit"):
        path = "C:\\Program Files\\Google\\Chrome\Application\chrome.exe"
    else:
        path = "C:\\Program Files (x86)\\Google\\Chrome\Application\chrome.exe"


    n = int(input("\n>>Number of Results wanted : "))
    a = input(">Enter the Algorithm Tag : ")
    print(">Query Ok! Values set!")
    print(
        "\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>( Session Started! )<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    while (1 == 1):
        try:
            print(choose_algorithm(a, n, path))

        except Exception as e:
            print(e)


def init():

    arch = platform.architecture()[0]
    print(">>>>>>>>>>>>> Initializing Fast Googler Project v0.5alphaEx <<<<<<<<<<<<<<<<")
    print("\n>Arch : ",arch)

    # getting the architecture , as 32 bit and 64 bit have different paths of chrome

    if(arch=="32bit"):
        path= "C:\\Program Files\\Google\\Chrome\Application\chrome.exe"
        print(">CHROME PATH SHOULD BE :",path)
    else:
        path= "C:\\Program Files (x86)\\Google\\Chrome\Application\chrome.exe"
        print(">CHROME PATH SHOULD BE :", path)

    start_historydb()
    print("\n=================================================\n")

    print("                      I AM FEELING LUCKY AND FAST! \n  "
          "\nAlgoritm Menu >\n1.Standard Fast Googling Algorithm(SFGA) (Automatically opens N tabs ,with websites based on your input)= 's'"
          "\n2.Keyword matching Algorithm(KMA) (Search URL based on input and shows number of keywords matched in a site)= 'k' " 
          "\n3.Bulk-Input Algorithm(BIA) from a text file = 't' "
          "\n4.Search History = 'h' "
          "\n\nNOTE: You must click Enter and type \end and press enter after the search input so a input completion can be triggered."

          )



    rep()

init()
