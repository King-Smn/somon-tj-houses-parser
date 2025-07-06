import requests
from bs4 import BeautifulSoup as bs
# It's a simple Python parser of a website Somon.tj
# Somon.tj is a popular real estate website in Tajikistan
# It lists various properties for sale or rent, including houses, apartments, and land
# Fetching the HTML content from the website
# The website is a real estate listing for houses with pools in Tajikistan
# The URL is filtered to show houses for rent with a maximum price of 1000 somoni
# The BeautifulSoup library is used to parse the HTML content
get_html = requests.get(
    "https://somon.tj/nedvizhimost/arenda-dach/bassejn---10/srok-arendyi---10/?price_max=1000")
soup = bs(get_html.text, "html.parser")
section = soup.select("section")
houses_block = section[2]
target_section = soup.select_one(
    "section.list-announcement[data-params-for-map='{\"user\": \"\"}']")
price_links = houses_block.select('a.advert__content-price._not-title')
price_links = [price_link.text for price_link in price_links]
prices = []

# Extracting prices from the links
for price in price_links:
    str_price = ""

    for char in price:
        try:
            char_int = int(char)
            str_price += str(char_int)
        except:
            pass
    list_str_price = list(str_price)
    while True:
        if len(list_str_price) > 3 and str_price != "1000":
            list_str_price.remove(list_str_price[-1])
        if len(list_str_price) <= 3 or str_price == "1000":
            break
    str_price = ""
    for char in list_str_price:
        str_price += char
    prices.append(int(str_price))

# Displaying the results
print(f"""The prices of houses are:
{', '.join([str(price) + ' somoni' for price in prices])}
\nThe minimum price is: {min(prices)} somoni
The maximum price is: {max(prices)} somoni
The total price of all houses is: {sum(prices)} somoni
The average price of houses is: {round(sum(prices) / len(prices))} somoni
The number of houses is: {len(prices)}""")