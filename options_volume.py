from config import * 

url = 'http://www.barchart.com/options/volume-leaders/stocks'
response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')
print(soup.findAll('div'))