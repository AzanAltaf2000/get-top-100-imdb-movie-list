import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re

url="https://www.imdb.com/chart/top?sort=rk,asc&mode=simple&page=1"
res=requests.get(url)
soup=BeautifulSoup(res.text,"html.parser")

movies= soup.select("td.titleColumn")
links=[x.attrs.get("href") for x in soup.select("td.titleColumn a")]
crew=[x.attrs.get("title") for x in soup.select("td.titleColumn a")]
ratings=[b.attrs.get("data-value") for b in soup.select("td.posterColumn span[name=ir]")]
votes=[b.attrs.get("data-value") for b in soup.select("td.ratingColumn strong")]
  
imdb=[]
    
#storing each item in description
for index in range(0,len(movies)):
    movie_string=movies[index].get_text()
    movie=(" ".join(movie_string.split()).replace(".",""))
    movie_title= movie[len(str(index))+1:len(movie)-7]
    #year=movie[len(movie)-5:len(movie)-1]
    year=re.search('\((.*?)\)', movie_string).group(1)
    place = movie[:len(str(index))-(len(movie))]
    data = {"place": place,
    "movie_title": movie_title,
    "year": year,
    "star_cast": crew[index],
    "rating": ratings[index],
    "vote": votes[index],
    "link": links[index]}
    imdb.append(data)
    
    
#for item in imdb:
  # print(item['place'], '-', item['movie_title'], '('+item['year']+') -', 'Starring:', item['star_cast'])
    
csv_Columns=["place","movie_title","year","star_cast","rating","vote","link"]
csv_file="imdb_.csv"
#cars=[{"place":1,"movie_title":"azabn","year":1924,"star_cast":"azan","rating":95,"vote":5,"link":"dsas"},{"place":1,"movie_title":"azabn","year":1924,"star_cast":"azan","rating":95,"vote":5,"link":"dsas"}]

with open(csv_file,"w") as csvfile:
    writer=csv.DictWriter(csvfile,fieldnames=csv_Columns)
    writer.writeheader() 
    m=imdb[0]
    print(m)
    writer.writerows(imdb)

    