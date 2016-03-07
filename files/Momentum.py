import Quandl
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import numpy as np
import matplotlib.pyplot as plt

#Function to download tickers and company names from Wikipedia, and format
#them so they can be used to download data from Quandl
def get_tickers():

    wiki = "https://en.wikipedia.org/wiki/S%26P_100"

    response = urllib.request.urlopen(wiki)

    html = response.read()

    soup = BeautifulSoup(html)


    table = soup.find("table", {"class" : "wikitable sortable" })

    ticker = []
    name = []

    for row in table.findAll("tr"):
        cells = row.findAll("td")
        try:
            symbol = cells[0]
            symbol = str(symbol)
            symbol = symbol[4 : -5]
            ticker.append(symbol)
            

            title = cells[1]
            title = str(title)
            title = title.split("title=", 1)[1].split(">", 1)[0]
            title = title[1 : -1]
            title = title.replace("&amp;", "&")
            name.append(title)
        except:
            Exception

    quandl_ticker = []

    for i in ticker:
        quandl = "WIKI/%s.11" %(i)
        quandl_ticker.append(quandl)

    return quandl_ticker, name


#Other functions used later in the program
def geometric_return(returns):

    returnseries = []
    last = 1
    for i in returns:
        calc = last + (i * last)
        returnseries.append(calc)
        last = calc
    returns = pd.DataFrame(returnseries)
    total = (last-1)/1
    geo = (total + 1)**(1/(len(returns) / 12))-1
    return geo

def std_dev(returns):
    data = np.asarray(returns)
    stddev = np.std(data) * np.sqrt(12)
    return stddev

def returnseries(returns):
    returnseries = []
    last = 100
    for i in returns:
        calc = last + (i * last)
        returnseries.append(calc)
        last = calc
    series = pd.Series(returnseries)
    return series

#Reading in data to avoid having to download all the data everytime.
try:
    data = pd.read_csv('data.csv', index_col='Date', parse_dates=True)
    
except:
    print('Datafile not found, downloading from Quandl')
    
    #Run the function to get the tickers, and format them to work on Quandl
    tickers = get_tickers()
    
    data = Quandl.get(tickers[0], authtoken="Add Your Own Token", trim_start="1999-12-20",
                    trim_end="2016-01-01", collapse="monthly")

    #Saves the file to the same folder containing the script
    data.to_csv('data.csv')
    

#Creates a DataFrame containing the one month return's and shifts it up one step to keep the next step easyer.
holding = data.pct_change(periods=1)
holding = holding.shift(periods=-1)

#Creates a DataFrame containing the one year return's used to select the best performing stocks for each month.
momentum = data.pct_change(periods=12)

#Creates a list of numbers of stocks to hold and test returns for. Here it is 1 to 10.
a = [5, 10, 15, 20, 25, 30]
lst = [ [] for i in a]

results = pd.DataFrame()

b = 0
for index, row in data.iterrows():
    
    if b > 11:
        #print(row)
        momentum_i = momentum.ix[b]
        returns_i = holding.ix[b]

        for column in data:

            momentum_stock = momentum_i[column]
            returns_stock = returns_i[column]
        
            results = results.append({'Ticker' : column, 'Momentum' : momentum_stock, 'Returns' : returns_stock}, ignore_index=True)
        

        
        i = 0 
        for list in lst:
            value = a[i]
            result = results.sort_values("Momentum", ascending = False).head(value)
            list.append(result['Returns'].mean())
            i += 1
        
    b+=1
    results = pd.DataFrame()
        

_5 = lst[0][ : -1]
_10 = lst[1][ : -1]
_15 = lst[2][ : -1]
_20 = lst[3][ : -1]
_25 = lst[4][ : -1]
_30 = lst[5][ : -1]


results_all = [_5, _10, _15, _20, _25, _30]

#Create a loop to calculate geometric return for all the different holdings
geometric_returns = []

for i in results_all:
    geo_ret = geometric_return(i)
    geometric_returns.append(geo_ret)

standard_deviation =  []

for i in results_all:
    std = std_dev(i)
    standard_deviation.append(std)


#Plots the Geometric Return for each number of holdings
y = geometric_returns
N = len(y)
x = np.arange(1, N+1)
labels = ['5', '10', '15', '20', '25', '30']
width = 0.7
bar1 = plt.bar(x, y, width)
plt.ylabel('Geometric Return')
plt.xlabel('Number of Holdings')
plt.xticks(x + width/2.0, labels)
plt.show()

#Plots the Standard Deviation for each number of holdings
y = standard_deviation
N = len(y)
x = np.arange(1, N+1)
labels = ['5', '10', '15', '20', '25', '30']
width = 0.7
bar1 = plt.bar(x, y, width, color="y" )
plt.ylabel('Standard Deviation')
plt.xlabel('Number of Holdings')
plt.xticks(x + width/2.0, labels)
plt.show()

#Plots the total equity curve for for each number of holdings
datelabel = data.index
datelabel = datelabel[ 13 : ]

plt.plot(datelabel, returnseries(_5))
plt.plot(datelabel, returnseries(_10))
plt.plot(datelabel, returnseries(_15))
plt.plot(datelabel, returnseries(_20))
plt.plot(datelabel, returnseries(_25))
plt.plot(datelabel, returnseries(_30))


plt.legend(['5', '10', '15', '20', '25', '30'], loc=2)
plt.title('Total Return on 100 investet in the different portfolios')
plt.show()

