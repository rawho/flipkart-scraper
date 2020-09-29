
# import the libraries
from bs4 import BeautifulSoup as soup
import requests
import os 

####################################################################################

def banner():
    print(r'''
	  __ _ _       _              _   
	 / _| (_)_ __ | | ____ _ _ __| |_ 
	| |_| | | '_ \| |/ / _` | '__| __|
	|  _| | | |_) |   < (_| | |  | |_ 
	|_| |_|_| .__/|_|\_\__,_|_|   \__| @rawho
	        |_|                       

    ''')

##################################################################################

#checking whether the file is already present
def is_file_already_present(filename):
    lst = os.listdir()
    return filename in lst 

#####################################################################################

#creating a filename
def create_file():
    filename = input('save the file as ....: ')
    filename = filename + '.csv'
    return filename

#################################################################################

# writing the header
def header_():
    global f
    f = open(filename, 'w')
    header = 'NAME, PRICE, RATING, NO:OF RATING \n'
    f.write(header)

############################################################################

# requesting and souping the html                                          
def requesting(url):
    uClient = requests.get(url)
    page_html = uClient.text
    page_soup = soup(page_html, 'html.parser')
    return page_soup

############################################################################

#scraping the details of the product in one model
def details(page_soup):
    global f
    containers = page_soup.find_all('div', {'class':'_3O0U0u'})

    for container in containers:
        if container is None: continue
        for i in container: 
            #product name
            name = i.div.div.img['alt']
            print('PRODUCT NAME : ', name)
    
            #product price
            price_container = i.find('div', {'class':'_1vC4OE'})
            if price_container is None:
                price = 'NA'
                print('PRODUCT PRICE : ', price)
            else:
                price = price_container.text.strip()
                print('PRODUCT PRICE : ', price)
            
            #rating
            rating_container = i.find('div', {'class':'hGSR34'})
            if rating_container is None: 
                rating = 'NA'
                print('PRODUCT RATING : ', rating)
            else:
                rating = rating_container.text
                print('PRODUCT RATING : ', rating)

            #no:of ratings
            no_ratings_container = i.find('span', {'class':'_38sUEc'})
            if no_ratings_container is None: 
                no_ratings = 'NA'
                print('NO:OF RATINGS : ' + no_ratings)
            else:
                no_ratings1 = no_ratings_container.text
                try:
                    no_rating = no_ratings1.split('&').split()
                    no_ratings = no_rating[0]
                    print('NO:OF RATINGS : ' + no_ratings)
                except: 
                    no_rating = no_ratings1.split()
                    no_ratings = no_rating[0]
                    print('NO:OF RATINGS : ' + no_ratings)   
    
            print('==========================')

            f.write(f'{name.replace(',','|')},{price.replace(',','').replace('₹','')},{rating},{no_ratings.replace(',','').replace('(','').replace(')','')}\n')

###########################################################################################################            

#scraping the details of product in another way
def details2(page_soup):
    global f
    
    containers = page_soup.find_all('div', {'class':'bhgxx2 col-12-12'})
    for container in containers:
        try:
            name_container = container.find('div', {'class':'_3wU53n'})
            if name_container is None : continue
            name = name_container.text.strip()
            print('PRODUCT NAME : ' + name)
                
            price_container = container.find('div',{'class':'_1vC4OE _2rQ-NK'})
            if price_container is None: 
                price = 'NA'
                print('PRODUCT PRICE : ' + price)
            else:
                price1 = price_container.text.strip()
                price = price1.replace(',','') 
                print('PRODUCT PRICE : ' + price)
                
            rating_container = container.find('div', {'class':'hGSR34'})
            if rating_container is None: 
                rating = 'NA'
                print('PRODUCT PRICE : ' + price)
            else:
                rating = rating_container.text.strip()
                print('PRODUCT RATING : ' + rating)

            no_ratings_container = container.find('span', {'class': '_38sUEc'}).span.span
            if no_ratings_container is None:
                no_ratings = 'NA'
                print('NO:OF RATINGS : ' + no_ratings)
            else:
                no_ratings1 = no_ratings_container.text.strip()
                try:
                    no_rating = no_ratings1.split('&').split()
                    no_ratings = no_rating[0]
                    print('NO:OF RATINGS : ' + no_ratings)
                except:
                    no_rating = no_ratings1.split()
                    no_ratings = no_rating[0]
                    print('NO:OF RATINGS : ' + no_ratings)

        
            print('=========================================================')
            
            f.write(f'{name.replace(',','|')},{price.replace(',','').replace('₹','')},{rating},{no_ratings.replace(',','').replace('(','').replace(')','')}\n')

        except:
            continue

#########################################################################################

def oh_yeah():
    
    page_soup = requesting(my_url)

    #takings the links of all the page
    page_container = page_soup.find_all('a','_2Xp0TH')

        #looping through the each page
    for page in page_container:
        url1 = 'https://www.flipkart.com'
        url2 = page.get('href')
        url = url1 + url2
        soup1 = requesting(url)
        try:
            details(soup1)
        except:
            details2(soup1)

########################## MAIN #############################################

banner()
my_url = input('Enter the flipcart url : ')
filename = create_file()
while True:
    if is_file_already_present(filename):
        aa = input('filename already exits. Do u want to replace it (y/n) : ')
        if aa == 'n':
            filename = create_file()
            if is_file_already_present(filename): continue
    header_()
    oh_yeah()
    break

################################################################################
