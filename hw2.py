# -*- coding: utf-8 -*-
"""HW2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vO_1tkgT7U85JJHUvgwJr9eBwicpOPf0

Problem 1
"""

!pip install scrapy
!pip install response
import time
import response
import requests
import pandas as pd
from scrapy.http import TextResponse

URL = "http://quotes.toscrape.com/"
base_url = "http://quotes.toscrape.com"

class Quotes:

    def __init__(self,URL):
        self.URL = URL
        self.page = requests.get(self.URL)
        self.response = TextResponse(body=self.page.text,url=self.URL,encoding="utf-8")

    def get_quotes(self):
        quotes = self.response.css("span.text::text").extract()
        authors = self.response.css("small.author::text").extract() 
        tags = [i.css("a.tag::text").extract() for i in self.response.css("div.tags")]
        hyperlinks = [base_url+i for i in self.response.css("small.author ~ a::attr(href)").extract()]
        return quotes, authors, tags, hyperlinks

    def get_next(self):
        next_url = self.response.css("li.next a::attr(href)").extract()
        return next_url

quotes = []
qts = Quotes(URL)

while True:
    time.sleep(2)
    if(qts.get_next()==[]):
        quotes.append(qts.get_quotes())
        break
    else:
        quotes.append(qts.get_quotes())
        URL = base_url + qts.get_next()[0]
        qts = Quotes(URL)

quotes

"""Problem 2"""

URL = "https://www.imdb.com/chart/moviemeter/"
base_url = "https://www.imdb.com"

class Movies: 

    def __init__(self,URL):
        self.URL = URL
        self.page = requests.get(self.URL)
        self.response = TextResponse(body=self.page.text,url=self.URL,encoding="utf-8")

    def get_movies(self):
        titles = self.response.css("td.titleColumn>a::text").extract()
        year = self.response.css("td.titleColumn>span.secondaryInfo::text").extract()
        ranking = [i.css("div.velocity::text").extract() for i in self.response.css("td.titleColumn")]
        rating_td = self.response.css('td[class = "ratingColumn imdbRating"]')
        rating = [i.css('strong::text').extract() for i in rating_td]
        rel_hyperlinks = self.response.css("td.titleColumn > a::attr(href)").extract()
        hyperlink_movie = [base_url + i for i in rel_hyperlinks]
        return pd.DataFrame({"Titles":titles,"Year":year,"Hyperlink_movie":hyperlink_movie,"Ranking":ranking,"Rating":rating})

movies = Movies("https://www.imdb.com/chart/moviemeter/")

movies.get_movies()

"""Problem 3"""

URL = "http://books.toscrape.com/"
base_url = "http://books.toscrape.com"

class Books:

    def __init__(self,URL):
        self.URL = URL
        self.page = requests.get(self.URL)
        self.response = TextResponse(body=self.page.text,url=self.URL,encoding="utf-8")
    def get_books(self):  
        page = requests.get(URL)
        response = TextResponse(body=page.text,url=URL,encoding="utf-8")
        title = self.response.css("h3 a::attr(title)").extract()
        price = self.response.css("p.price_color::text").extract()
        Price = [i.replace("Â","") for i in price]
        stock = [i.css("p.instock.availability::text").extract() for i in self.response.css("div.product_price")]
        rel_hyperlinks = self.response.css("h3 a::attr(href)").extract()
        hyperlink_book = [base_url + i for i in rel_hyperlinks]
        rel_hyperlink = self.response.css("img.thumbnail::attr(src)").extract()
        hyperlink_image = [base_url + i for i in rel_hyperlink]
        rating_books = self.response.css("p.star-rating::attr(class)").extract()
        Rating_books = [i.replace("star-rating","") for i in rating_books]
        return {"Title":title,"Price":Price,"Stock":stock,"Hyperlink_book":hyperlink_book,"Hyperlink_image":hyperlink_image,"Rating":Rating_books}

books = []
bks = Books(URL)

for i in range(1,51):
  books.append(bks.get_books())
  URL = base_url
  bks = Books(URL)

books