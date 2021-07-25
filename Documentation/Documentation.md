# Documentation

[toc]

## User Guide

- User visits `Website` & enters Query
- Query assigned Unique Identifier & sent to `GlobalAPI`
- User is redirected to `url_for('results')`

- `GlobalAPI` receives Query + Identifier
- `GlobalAPI` send query to `SearchEngine` via `Redis-StreamA`

- `SearchEngine` receives Query + Identifier
- `SearchEngine` uses `rank-BM25` to rank content from `MongoCS` database according to Query
- `SearchEngine` adds list of ranked results to `RedisAPI DB0`
  
- `GlobalAPI`  fetches list of ranked results from `RedisAPI DB0`
  
- `GlobalAPI` sends list of links to `url_for('results')`

- `Website` receives list of links
- `Website` displays list of links at `url_for('results')`

- `ContentScraper` runs once every 24 hours to look for new URLs

  

## Services

### NGINX

NGINX + Gunicorn

HTTP + Production grade WSGI Server



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

Python (`Flask`) based API Communication between Frontend and Backend Services


## Docs: GoAPI

**Not Fully Implemented!** 
Golang (`gorilla/mux`) based API for communication between Frontend & Backend Services.
Up to 75x faster than `GlobalAPI`. 

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

**Stream A**

- Messages:  GlobalAPI ->  SearchEngine



### DB 1

**Set/Get**

- Results: SearchEngine -> GlobalAPI



## Docs: MongoDB

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

- [ ] Secure Databases

  



### Build: Website

- [ ] Add Flask-Login

  


### Build: Content Scraper

- [ ] Save Article Content for ranking



### Build: Search Engine Build

- [ ] Rank by Article Content
