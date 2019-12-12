from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import urllib.request

root_dir = "https://engineering.purdue.edu/Engr/People/ptDirectory"
faculty_letters = ["A",'B','C']
BIO_URLS_FILE_LOCATION = "../bio_urls.txt"
BIOS_FILE_LOCATION = "../bios.txt"
TIMEOUT = 30
MINIMUM_BIO_REQUIREMENT = 10

''' More tidying
Sometimes the text extracted HTML webpage may contain javascript code and some style elements.
This function removes script and style tags from HTML so that extracted text does not contain them.
'''
def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup

#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,browser):
    soup = None
    try:
        browser.get(url)
        res_html = browser.execute_script('return document.body.innerHTML')
        soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
        soup = remove_script(soup)
    except:
        soup = None

    return soup


# Helper Funciton: Get faculties for letter
def get_faculty_for_letter(browser, letter):

    url = "{}?letter={}".format(root_dir,letter)
    # print(url)

    soup = get_js_soup(url, browser) #get html code

    # Get faculty-ids
    links = []

    people_rows = soup.find("div", class_="people-list").find_all("div",class_="col-8 col-sm-9 list-info")
    for row in people_rows:
        a = row.find("a")['href']
        # print(a)
        links.append(a)

    return links

# Scrapy the lists of faculty links
def get_list_of_faculty_links(browser):
    faculty_links = []
    for letter in faculty_letters:
        links = get_faculty_for_letter(browser, letter)
        faculty_links += links
        print(letter + " " + str(len(links)))

    return faculty_links

#tidies extracted text
def process_bio(bio):
    bio = bio.encode('ascii',errors='ignore').decode('utf-8')       #removes non-ascii characters
    bio = re.sub('\s+',' ',bio)       #repalces repeated whitespace characters with single space
    return bio

#Checks if bio_url is a valid faculty homepage
def is_valid_homepage(link):
    try:
        #sometimes the homepage url points to the faculty profile page
        #which should be treated differently from an actual homepage
        code = urllib.request.urlopen(link, timeout = TIMEOUT).getcode()
        return code == 200
    except:
        return False

# Process each specific faculty link
def process_specific_faculty_link(browser, link):
    if not is_valid_homepage(link): return ("", "")

    soup = get_js_soup(link, browser) #get html code
    if soup is None: return ("", "") #sometimes the page does not exist or wait longer than 30 seconds, then we consider it as invalid

    # Check if the HOMEPAGE exist, if then parse the homepage. else just parse the current page
    homepage_url = ""
    bio = ""
    all_ths = soup.find_all('th')
    for index, th in enumerate(all_ths):
        if th.text.lower() == "homepage:":
            # find homepage, try to get the homepage url
            homepage_url = all_ths[index+1].find("a")['href']
            break

    if "purdue.edu" not in homepage_url: homepage_url = "" #if we can't find purdue.edu in the homepage_url, we treat it as invalid. and use the default option

    if homepage_url == "": #homepage_url does not exist, we treat current page as the homepage:
        homepage_url = link
        main_content = soup.find("div", class_='content col-md-9') #we only interested in this part of the page
        bio = process_bio(main_content.get_text(separator=' '))
    else: #homepage_url does exist,
        homepage_soup = get_js_soup(homepage_url, browser)
        if homepage_soup is None: return ("", "") #sometimes the directed page does not exist or wait longer than 30 seconds, then we consider it as invalid

        #get all the text from homepage(bio) since there's no easy to filter noise like navigation bar etc
        bio = process_bio(homepage_soup.get_text(separator=' '))

    # print(homepage_url)
    # print(bio)
    if len(bio) < MINIMUM_BIO_REQUIREMENT: return ("", "") #if the len of bio is less than 10, we consider it as invalid

    return (homepage_url, bio)

# Helper function to write array to local file
def write_array_to_local_text_file(file_name, array):
    with open(file_name,'w') as f:
        for l in array:
            f.write(l)
            f.write('\n')

if __name__ == '__main__':
    #create a webdriver object and set options for headless browsing
    options = Options()
    # options.headless = True
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(TIMEOUT)
    faculty_links = get_list_of_faculty_links(browser) #Get lists of faculty links

    #loop through the faculty links, and process each one by one
    bio_urls = []
    bios = []

    for index, link in enumerate(faculty_links):
        print("{}/{}".format(index, len(faculty_links)))
        homepage_url, bio = process_specific_faculty_link(browser, link)
        if homepage_url == "" or bio == "":
            print("not valid! {}".format(link))
            continue
        bio_urls.append(homepage_url)
        bios.append(bio)

    #Write the data to local file system
    write_array_to_local_text_file(BIO_URLS_FILE_LOCATION, bio_urls)
    write_array_to_local_text_file(BIOS_FILE_LOCATION, bios)
