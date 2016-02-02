# webscraper for huffpost
import requests
from bs4 import BeautifulSoup

url = 'http://www.huffingtonpost.com/search.php/?q=Search+The+Huffington+Post&sort=date&date_filter=newest&s_it=header_form_v1&type=blogs'

r = requests.get(url)
soup = BeautifulSoup(r.content)




if __name__ == '__main__': main()