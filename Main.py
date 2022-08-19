from bs4 import BeautifulSoup
import requests

class Entry():
    price = 0
    address = ""
#Code adpated from Alexander Demchenko
#This section is used to bypass the bots on zillow in order to get to the correct information
request_headers = {
    'accept' :
        'text/html,application/xhtml,application/xml;q=0.9,image/webp.image/apng,*/*;q=0.8',
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language' : 'en-US,en;q=0.8',
        'upgrade-insecure-requests' : '1',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/61.0.3136 Safari/537.36'
    }
with requests.Session() as session:
    #Gets input for the city and abbreviated state
    #then adds those variables into the url equation to get a working url
    city = input('Enter a city: ')
    state = input('Enter state(abbreviated): ')
    url = 'https://www.zillow.com/homes/for_sale/' + city.lower().capitalize() + ',-' + state.upper() +'/'
    website = session.get(url, headers =request_headers)
 
#changes inputted price into an integer without the $/,
#buget input is the price that can be added/subtracted to the price to create a budget margin
pricechoice = int(input('Enter a price: ').replace(',', '').replace('$',''))
budget = int(input('Input your budget margins: ').replace(',', '').replace('$',''))
#scrape is the variable name for the BeatifulSoup functioon
scrape = BeautifulSoup(website.content, "html.parser")

#scraping the price and address
price1 = list(scrape.find_all('div', {'class' : 'list-card-price'}))
address1 = list(scrape.find_all(class_= 'list-card-addr'))

#for each element in price, replace the extra test and transform it into an int; then add it to a new list full of ints
price = []
for i in price1:
    temp = (str(i).replace('<div class="list-card-price">', '').replace('</div>', '').replace('$', '').replace(',', ''))
    temp_ = int(temp)
    price.append(temp_)
   
#for each element in address, replace the extra test and transform it into an str; then add it to a new list full of str
address = []
for i in address1:
    temp = (str(i).replace('<address class="list-card-addr">', '').replace('</address>', ''))
    address.append(temp)

#combined list so prices correspond w/ addresses
house = []
for i in range(0,len(price)):
    temp = Entry()
    temp.price = price[i]
    temp.address = address[i]
    house.append(temp)

#for each price-addresss, if the price is <= the chosen price, it is under the price
#for each price-addresss, if the price is within +/- the budget, the price is w/in their budget
budgetlist = []
for i in house:
      if i.price <= pricechoice:
        print('This house is UNDER your chosen price:', i.address, 'Price: $',i.price, '\n')
      elif i.price in range(budget + pricechoice or pricechoice - budget):
          print('This house is WITHIN your budget:', i.address, 'Price: $',i.price, '\n')