# SoundSearch

# Sound Search

Search Engine and Website Index Service for selected Websites

[toc]

## Steps

- User enters Query
- Query is sent to API
- User is redirected to `url_for('results')`

-

- API recives Query
- API notifies `SearchEngine` that query has been recieved
- API send query to `SearchEngine`

-

- `SearchEngine` recieves Query
- `SearchEngine` uses `rank-BM25` to rank content from `ContentScraper` database acording to Query
- `SearchEngine` saves list of ranked links to `SEngine.db`
- `SearchEngine` alerts `API` about list of links

-

- `API` pulls list of links from `SEngine.db`
- `API` sends list of links to `url_for('results')`

-

- `Site` recieves list of links
- `Site` displays list of links at `url_for('results')`

-

- `ContentScraper` runs once every 24 hours to look for new URLs to harvest data from
- Harvested Data is stored in `CScraper.DB`



## Services



### Website

STATUS:

Provides Web Interface for User

- **Python Scripts:** `app.py`

  - https://sitename/index

  - https://sitename/results

    

### GlobalAPI

STATUS: 

Handles Communication between Front and Backend

- **Python Script:** `api.py`
  - `GET` User sends request to server from `index.html` 
  - `POST` Results returned  to `results.html`
- **Database:** 
  - **REDISJSON:**  Redis-API  



### RabbitMQ

STATUS:

Handles communication between Backend services

- **Python Script:** `rabbit.py` 



### ContentScraper

STATUS:

Scrapes Sites and collects relavent data

Spider + Indexer

- **Python Script:** `scraper.py`
- `Scrapy`
  - `Requests`
  - `lxml`
  - Scraper compiles list of URLs
  - Scrapes Title + Content from each URL
  - Stores URL + Title + Content in DB
  - Title + Content identified via URL
- **Database:** 
  - **Mongo DB ? :** CScraper.db

 

### SearchEngine 

STATUS:

Ranking

Ranks stored data according to BM25 and returns results via GlobalAPI

- **Python Script:** `repo.py`
  - `rank-BM25`
  - Access Data from ContentScraper
- **Database:**
  - **Mongo DB ? :** SEngine.db



## Docs: API 

All responses have form:

> {
>
> ​	"identifier":   mixed-type     " Query "
>
> ​	"query":          mixed-type     " form.query.data "
>
> }



### Route:   ` /query` 

API: siteAPI_GP

- **GET**
  - Returns existing / current Queries from DB
- **POST**
  - Adds a new Query to DB



## Checklist

### General

- [x] Move from Shelve to Redis Container
- [x] Allow Python Scripts to communicate without globalAPI
- [ ] Create MongoDB Databases



### RabbitMQ Build

- [ ] Allow Messages to be sent to services
- [ ] Allow Messages to be recieved from services



### Content Scraper Build

- [ ] Runs once every 24 hours
- [ ] Connects to RabbitMQ



### Search Engine Build

- [ ] Connects to RabbitMQ
- [ ] Store Website URLs in Persistant Storage - MongoDB 
- [ ] How to send notifications between services - Rabbit MQ



### Pre Release

- [ ] Add `.env` files for every service

- [ ] Research alternative to local `.env` files

- [ ] Remove `debug=True` from Flask scripts

- [ ] Find List of most common Queries to be cached

- [ ] Docker Load Balancing

- [ ] Docker Microservice Scaling

  

###  Redis Streams

- Query recived
- Query sent to stream