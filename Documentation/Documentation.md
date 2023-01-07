# Documentation

[toc]

## User Guide

- Install [Docker-Compose](https://docs.docker.com/compose/)

- Download Latest Release
- Create Sub-Directory `./MongoDB`
- Execute `./start.sh`
- View Web Interface At: `http://localhost/index`



## NGINX

- NGINX + Gunicorn

- HTTP + Production grade WSGI Server



## Website

User Web Interface

- User Accessible End-Points

  - www.site.com/home
  - www.site.com/results

- Admin Accessible End-Points

  - www.site.com/admin




## Search Engine

- Ranks a corpus of titles according to the incoming query using BM25 and returns them to the API via Redis Streams




## Content Scraper

- Scrapes listed sites, collects required data & stores it in MongoDB



## GoAPI

GoLang (`gorilla/mux`) based API for communication between Frontend & Backend Services. 
Format = JSON

### Routes

- POST `/api/v1/query` - Send query to `SearchEngine` Service
- GET `/api/v1/results` - Retrieves Results from `SearchEngine` Service as JSON
- GET `/api/v1/metrix` - Retrieves `SearchEngine` usage statistics



## GlobalAPI

Python (`Flask`) based API Communication between Frontend and Backend Services. 
Format = JSON

### Routes

- POST `/api/v1/query` - Send query to `SearchEngine` Service
- GET `/api/v1/results` - Retrieves Results from `SearchEngine` Service as JSON
- GET `/api/v1/metrix` - Retrieves `SearchEngine` usage statistics



## Redis

Redis Database with RedisJSON module. Allows for communication between `SearchEngine` & API's

### DB 0

- Type: JSON Stream
- Traffic Type: Search Queries
- Traffic Direction:  API -> `SearchEngine`

### DB 1

- Type: JSON Set / Get
- Traffic Type: Search Results
- Traffic Direction: `SearchEngine` -> API



## MongoDB

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
