import bs4
import webbrowser
import requests


def SST(paper,n):
    d = []
    m = 0
    s = ''
    file = open(paper, 'r', encoding="utf-8")

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

    chrome_path = "C:\\Program Files\\Google\\Chrome\Application\chrome.exe"

    for i in range(0, len(d)):
        print("Searching For Part :",d[i])
        res = requests.get('https://google.com/search?q=' + d[i])
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        linkElements = soup.select('div#main > div > div > div > a')
        linkToOpen = min(n, len(linkElements))
        # print(linkElements)

        print("\nOpening Chrome and Showing ", n, " results")

        # chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\Application\chrome.exe"

        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

        # os.system(r'C:\\Program Files (x86)\\Google\\Chrome\Application\chrome.exe')
        l = input("Press Enter to Start Opening :")
        for i in range(linkToOpen):
            webbrowser.get('chrome').open('https://google.com' + linkElements[i].get('href'))
        print("\n==============( A Task Completed)==========>>> ")



def keywordSearch():
    inp = input("Search For : ")
    keywords = input("Keywords :").split()
    print(keywords)
    print("Searching please wait....")
    res = requests.get('https://google.com/search?q=' + inp)

    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    linkElements = soup.select('div#main > div > div > div > a')
    linkToOpen = min(15, len(linkElements))

    for i in range(linkToOpen):
        count = 0
        l = []
        url = 'https://google.com' + linkElements[i].get('href')
        print(">Trying on :" + url)
        for j in range(0, len(keywords)):

            if (keywords[j] in requests.get(url).text):
                # print("Keyword Matched :"+keywords[j])
                l.append(keywords[j])
                count += 1

        print(count, " Keywords Matched :", l)



def takeinput():
    text = ""
    stopword = "end"
    while True:
        line = input()
        if line.strip() == stopword:
            break
        text += "%s\n" % line
    return text

def StandardSearch(n , chrome_path ="C:\\Program Files\\Google\\Chrome\Application\chrome.exe"):
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

    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

    # os.system(r'C:\\Program Files (x86)\\Google\\Chrome\Application\chrome.exe')
    for i in range(linkToOpen):
        webbrowser.get('chrome').open('https://google.com' + linkElements[i].get('href'))

    print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>( One Thread Closed! )<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

def paperinp():
    inp = input("\nFile Name :")+".txt"
    return inp


def choose_algorithm(argument, n):

    if(argument =='s'):
        StandardSearch(n)
    elif(argument == 'k'):
        keywordSearch()
    elif(argument == 't'):
        SST(paperinp(),n)



def init():


    print(">>>>>>>>>>>>> Initializing Fast Googler's Tool v0.5a <<<<<<<<<<<<<<<<")
    print("                      I AM FEELING LUCKY! \n  "
          "\nAlgoritm Menu >\n1.Standard Fast Googling Algorithm(SFGA) (Automatically opens N tabs ,with websites based on your input)= 's'"
          "\n2.Keyword matching Algorithm(KMA) (Search URL based on input and shows number of keywords matched)= 'k'  ( Under Work , not available yet)" 
          "\n3.Sweet-Shot-Text Algorithm(SST) (Take inputs from text file automatically and open best urls ( Start Area : { , End Area : } ,ie: All the words under this {} will be taken as input )= 't'"
          "\n\n$NOTE: C:\\Program Files\\Google\\Chrome\Application\chrome.exe should be your chrome location. "

          )

    n = int(input("\n>Enter the number of results you want throughout this session : "))
    a = input("Enter the Algorithm Tag : ")
    print(">Query Ok! Values set!")
    print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>( Session Started! )<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    while (1 == 1):
        try:
            print(choose_algorithm(a,n))

        except Exception as e:
            print(e)


init()
