import requests as r
from bs4 import BeautifulSoup
import pandas as pd
movies_data={
    'movie_name':[],
    'movie_rank':[],
    'movie_year':[],
    'movie__IMDB_rating':[],
    'movie_link':[]
}

url='https://www.imdb.com/chart/top/?ref_=nv_mv_250'
site_url='https://www.imdb.com'

def give_data(response):
    data=BeautifulSoup(response.content,'html.parser')

    data=data.find('tbody')
    movies=data.find_all('tr')
    for movie in movies:
        movie_name=movie.find('td',class_="titleColumn").a.text.strip()
        movie_year=movie.find('td',class_="titleColumn").span.text.strip('()')
        movie_rank=movie.find('td',class_="titleColumn").text.strip().split('.')[0]
        # movie_rank=movie.find('td',class_="titleColumn").get_text(strip=True).split('.')[0]

        rating=movie.find('td',class_="ratingColumn imdbRating").strong.text
        movie_link=site_url+ movie.find('td',class_="titleColumn").a['href']
        movies_data['movie_rank'].append(movie_rank)
        movies_data['movie_name'].append(movie_name)
        movies_data['movie_year'].append(movie_year)
        movies_data['movie__IMDB_rating'].append(rating)
        movies_data['movie_link'].append(movie_link)
        
    return pd.DataFrame(movies_data) 
    
response=r.get(url)
if response.status_code==200:
    return_data=give_data(response)
    return_data.to_csv('top_movies.csv',index=False)
        
