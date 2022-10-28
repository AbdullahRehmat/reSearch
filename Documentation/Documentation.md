# Documentation

[toc]

## User Guide

- Install [Docker-Compose](https://docs.docker.com/compose/)
- Execute `./start.sh` and view Web Interface `http://localhost`



## Services

### NGINX

- NGINX + Gunicorn

- HTTP + Production grade WSGI Server



### Website

User Web Interface

- User Accessible End-Points

  - www.site.com/home
  - www.site.com/results

- Admin Accessible End-Points

  - www.site.com/admin



### Global API

- Handles Communication between Front and Backend
- Original API written in Python



### Go API

- Handles Communication between Front and Backend

- `GlobalAPI` alternative written in Go



### Redis API

- Redis + RedisJSON Module + Streams

- Handles Backend Inter-Service Communication




### Search Engine

- Ranks stored data according to Query and returns results to `Global API` via **Stream-B**




### Content Scraper

- Scrapes listed sites, collects required data & stores it in the `MongoCS` Database



## Docs: GlobalAPI

Python (`Flask`) based API Communication between Frontend and Backend Services. 
Format = JSON

### Routes

- POST `/api/v1/query` - Send query to `SearchEngine` Service
- GET `/api/v1/results` - Retrieves Results from `SearchEngine` Service as JSON
- GET `/api/v1/metrix` - Retrieves `SearchEngine` usage statistics



## Docs: GoAPI

GoLang (`gorilla/mux`) based API for communication between Frontend & Backend Services. 
Format = JSON

### Routes

- POST `/api/v1/query` - Send query to `SearchEngine` Service
- GET `/api/v1/results` - Retrieves Results from `SearchEngine` Service as JSON
- GET `/api/v1/metrix` - Retrieves `SearchEngine` usage statistics



## Docs: Redis

### DB 0

- Type: JSON Stream
- Traffic Type: Search Queries
- Traffic Direction:  API -> `SearchEngine`

### DB 1

- Type: JSON Set / Get
- Traffic Type: Search Results
- Traffic Direction: `SearchEngine` -> API



## Docs: MongoDB

### ContentScraperDB

Stores URLs + Titles from `ContentScraper`

**All Records have form:**

> {
>
> "global_id": identifier - Unique 10 Character String
>
> "title":[ "Sample Title"]
>
> "url": ["www.example.com/blogpost1"]
>
> "source": "www.example.com - Admin - 2021"
>
> }



#### Collections

- `scrapedData` - List of all scraped URLs with titles corrected by `SpellChecker`



### SearchEngineDB

Stores URLs + Titles  as ranked by BM25 from `SearchEngine`

**All Records have form:**

> {
>
> "global_id": identifier - Unique 10 Character String
>
> "title":[ "Sample Title"]
>
> "url": ["www.example.com/blogpost1"]
>
> "source": "www.example.com - Admin - 2021"
>
> }



#### Collections

- `returnedResults` - List of all results generated
