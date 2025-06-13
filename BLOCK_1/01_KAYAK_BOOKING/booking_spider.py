import os
import logging
import argparse
import scrapy
from scrapy.crawler import CrawlerProcess

class BookingSpider(scrapy.Spider):

    name = "booking"

    custom_settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7"
    }

    def start_requests(self):
        # Loading URLs
        urls = load_urls()
        
        # Iterating on URLs
        for index, url in enumerate(urls):
            # Setting an index, it will be useful when exporting on a SQL database
            yield scrapy.Request(url=url, callback=self.parse, meta={"city_id":index+1}) 

    def parse(self, response):
        # Getting all hotels in the page
        hotels = response.xpath('/html/body/div[4]/div/div/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[@data-testid="property-card"]')

        # Iterating on each hotel
        for hotel in hotels:

            # Getting URL within the overview
            url = hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a[@data-testid="title-link"]/@href').get()

            # Following URL to get more infos on the hotel
            yield scrapy.Request(url=url, callback=self.parse_hotel_details, meta={"city_id":response.meta["city_id"]})
        

    def parse_hotel_details(self, response):
            
            # Getting coordinates
            coordinates = response.xpath('//*[@id="map_trigger_header_pin"]/@data-atlas-latlng').get()

            # Retrieving latitude and longitude from coordinates
            latitude = coordinates.split(",")[0]
            longitude = coordinates.split(",")[1]

            # Getting all necessaries info and returning it : name, rating, latitude, longitude, description, URL and index
            yield {
                'name': response.xpath('//*[@id="hp_hotel_name"]/div/h2/text()').get(),
                'rating': response.xpath('//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div[1]/text()').get(),
                'lat': latitude,
                'lon': longitude,
                'description': response.xpath('//*[@id="basiclayout"]//*[@data-testid="property-description"]/text()').get(),
                'url': response.url,
                'city_id': response.meta["city_id"]
            }
            
# Name of the file where the results will be saved
filename = "hotels.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('data/'):
        os.remove('data/' + filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'data/' + filename: {"format": "json"},
    }
})

# Function creating and returning a list of URLs based on cities we want infos
def load_urls():

    # Base of booking search URL
    base_url = "https://www.booking.com/searchresults.fr.html?ss="

    # List of cities we're interested in
    cities_list = ["Mont Saint Michel",
                    "St Malo",
                    "Bayeux",
                    "Le Havre",
                    "Rouen",
                    "Paris",
                    "Amiens",
                    "Lille",
                    "Strasbourg",
                    "Chateau du Haut Koenigsbourg",
                    "Colmar",
                    "Eguisheim",
                    "Besancon",
                    "Dijon",
                    "Annecy",
                    "Grenoble",
                    "Lyon",
                    "Gorges du Verdon",
                    "Bormes les Mimosas",
                    "Cassis",
                    "Marseille",
                    "Aix en Provence",
                    "Avignon",
                    "Uzes",
                    "Nimes",
                    "Aigues Mortes",
                    "Saintes Maries de la mer",
                    "Collioure",
                    "Carcassonne",
                    "Ariege",
                    "Toulouse",
                    "Montauban",
                    "Biarritz",
                    "Bayonne",
                    "La Rochelle"]
    
    urls = [base_url+i for i in cities_list]

    return urls
     
# Start the crawling using the spider you defined above
process.crawl(BookingSpider)
process.start()