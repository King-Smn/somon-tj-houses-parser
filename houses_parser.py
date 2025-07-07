import requests
from bs4 import BeautifulSoup as bs

# It's a simple Python parser of a website Somon.tj
# Somon.tj is a popular real estate website in Tajikistan
# It lists various properties for sale or rent, including houses, apartments, and land
# Fetching the HTML content from the website
# The website is a real estate listing for houses with pools in Tajikistan 
# The URL is filtered to show houses for rent with a price filter
# The BeautifulSoup library is used to parse the HTML content

def parse_houses_with_price_filter():
    """Function to parse houses with a price filter"""
    print("Parsing houses with a price filter")
    price_min = int(input("Enter the minimum price of houses: "))
    price_max = int(input("Enter the maximum price of houses: "))
    max_num_of_page = int(
        input("Enter the maximum number of pages to parse: "))
    if max_num_of_page <= 2:
        print("The number of pages must be greater than 0")
        exit()
    num_of_page = 1
    prices = []
    pages = []
    while True:
        num_of_page += 1
        page = f"https://somon.tj/nedvizhimost/arenda-dach/bassejn---10/srok-arendyi---10/?page={num_of_page}&price_min={price_min}&price_max={price_max}"
        get_html = requests.get(page)
        if get_html.status_code != 200 or num_of_page == max_num_of_page:
            print(
                f'You have a bad internet connection or {page} does not exist')
            break
        print(f"Parsing page: {page}")
        # Parsing the HTML content using BeautifulSoup
        soup = bs(get_html.text, "html.parser")
        section = soup.select("section")
        houses_block = section[2]
        price_links = houses_block.select('a.advert__content-price._not-title')
        price_links = [price_link.text for price_link in price_links]
        # Extracting prices from the links
        for price in price_links:
            str_price = ""
            for char in price:
                try:
                    char_int = int(char)
                    str_price += str(char_int)
                except:
                    pass
            if str_price >= str(price_max):
                str_price = str_price[:len(str(price_max))-1]
            else:
                str_price = str_price[:len(str(price_max))]
            prices.append(int(str_price))
            pages.append(page)
    # Displaying the results
    print(f"""The prices of houses are:
    {', '.join([str(price) + ' somoni' for price in prices])}
    \nThe minimum price is: {min(prices)} somoni:   {pages[prices.index(min(prices))]}
    The maximum price is: {max(prices)} somoni:   {pages[prices.index(max(prices))]}
    The total price of all houses is: {sum(prices)} somoni
    The average price of houses is: {round(sum(prices) / len(prices))} somoni
    The number of houses is: {len(prices)}""")


if __name__ == "__main__":
    parse_houses_with_price_filter()