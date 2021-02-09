# Documentation

[toc]

## Steps

- User visits `Website` & enters Query
- Query assigned Unique Identifier & sent to `GlobalAPI`
- User is redirected to `url_for('results')`

- `GlobalAPI` receives Query + Identifier
- `GlobalAPI` send query to `SearchEngine` via `Redis-StreamA`

- `SearchEngine` receives Query + Identifier
- `SearchEngine` uses `rank-BM25` to rank content from `MongoCS` database according to Query
- `SearchEngine` saves list of ranked links to `MongoSE`
  
- `SearchEngine` alerts `GlobalAPI` that ranking is complete
  
- `GlobalAPI` pulls list of links from `MongoSE.db`
- `GlobalAPI` sends list of links to `url_for('results')`

- `Website` receives list of links
- `Website` displays list of links at `url_for('results')`

- `ContentScraper` runs once every 24 hours to look for new URLs

  

## Services

### NGINX

NGINX + Gunicorn

HTTPS + Production grade WSGI Server



### Website

User Web Interface

- User Accessible End-Points

  - www.site.com/home
  - www.site.com/results

- Admin Accessible End-Points

  - www.site.com/admin

    

### GlobalAPI

Handles Communication between Front and Backend



### RedisAPI

Redis + RedisJSON + Streams

Handles Backend Inter-Service Communication

 

### SearchEngine 

Ranks stored data according to Query and returns results to  `GlobalAPI` via **Stream-B**



### ContentScraper

Scrapes Sites and collects relevant data



## Docs: GlobalAPI 

Communication between Frontend and Backend Services



### Route   `/api` 

API: siteAPI_GP

All responses have form:

> {
>
> ​	"identifier":   mixed-type        Randomly Generated  String
>
> ​	"query":          mixed-type     " form.query.data "
>
> }

- **GET**
  
  - Returns Query Result from SearchEngine
- **POST**
  
  - Send Query to SearchEngine for Processing
  
    

## Docs: Redis

### DB 0

- Put / Get
  - Stores Query from Site
  - Returns Query to Site via GlobalAPI



### DB 1

**Stream A**

- Messages:  GlobalAPI ->  SearchEngine

**Stream B**

- Messages:  SearchEngine -> GlobalAPI



## Docs: MongoDB

### MongoSE

URLs + Titles Ranked by Query

All Records have form:

>{
>
>​	"global_id": identifier 10 Char String
>
>​	"title": "First Blog Post"
>
>​	"URL": "www.example.com/blogpost1"
>
>}



### MongoCS

URLs + Titles from ContentScraper

All Records have form:

>{
>
>​	"global_id": "000112312334"
>
>​	"title": "First Blog Post"
>
>​	"URL": "www.example.com/blogpost1"
>
>}



## Cloud Providers

### Hosting

- Digital Ocean

### CDN

- Cloud Flare

### Caching

- Redis Labs

### Databases

- Mongo Atlas



## Checklist

### Build: General 

- [x] Set up Nginx

- [x] Set up Gunicorn

- [ ] Log Aggregator

- [ ] Docker-Compose Resource Limits ?

  


### Build: Website

- [ ] Add Flask-Login
- [ ] Collect Metrix and Stats




### Build: Content Scraper

- [ ] Docker Cron Job
- [ ] Add Multiple Sites
- [ ] Save Article Content for ranking



### Build: Search Engine Build

- [ ] Rank by Article Content




### Launch

- [ ] Update README

- [ ] Add Docs to Documentation Directory 

- [x] Remove `debug=True` from Flask scripts

- [x] Research alternative to local `.env` files

- [x] Secure Databases

- [ ] Fork - SalafiSearch

  
