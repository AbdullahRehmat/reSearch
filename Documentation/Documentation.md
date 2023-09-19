# Documentation: reSearch

[toc]

> Version: 2.0.0
>
> Last Update: 19-09-2023



## Start Guide

- Install [Docker-Compose](https://docs.docker.com/compose/)
- Download Latest Release From GitHub Repository
- Create Sub-Directory `./MongoDB`
- Execute `./start.sh`

- View Home Page: `http://localhost:80`

- View Admin Page: `http://localhost:80/admin`



## About

`reSearch` is a basic search engine based on the BM25 algorithm and runs as a series of microservices.



## Web Server: NGINX

**Web Server, Load Balancer & Reverse Proxy**

- Port: 80:80



## Interface: Website

**User Web-Interface**

- Language: HTML5, CSS3, JavaScript

- Port: 8000



**Public Routes**

- `http://localhost:80/`
- `http://localhost:80/index`
- `http://localhost:80/home`
- `http://localhost:80/results`



**Private Routes**

- `https://localhost:80/admin`



## Interface: Android App

Not Yet Implemented



## API: Python

**Microservice Communication API**

- Language: Python 3
- Framework: `flask`
- Format: `JSON`

- Port: 8000:-



**Routes**

- POST `/api/v1/query` - Send query to `SearchEngine` Service

> **Request: **
>
> {
> 	"identifier": "sampl3id3nt1f1er",
> 	"query": "What Is A Cookie?"
> }
>
> **Response:**
>
> {
> "api": "Py-API",
> "version": "1.0.0",
> "status": "SUCCESS",
> "data": {
>  "identifier": "sampl3id3nt1f1er",
>  "query": "What Is A Cookie?"
> 	}
> } 

- GET `/api/v1/results` - Retrieves results from `SearchEngine` Service as JSON

> **Request: **
>
> http://localhost:8000/api/v1/results/<identifier> 
>
> **Response:**
>
> {
> "api": "Py-API",
> "version": "1.0.0",
> "status": "SUCCESS",
> "identifier": "sampl3id3nt1f1er",
> "query": "What Is A Cookie?",
> "time_taken": "205.50 ms",
> "results": [
>  {      "title": "What Are Cookies Made Of?",
>    "url": "http://www.example.com/cookie-ingredients",
>    "source": "example.com - Article - William Smith"
>  },
>
> ​	{      "title": "How Are Cookies Made?",
> ​      "url": "http://www.example.com/cookie-ingredients",
> ​      "source": "example.com - Article - John Doe"
> ​    }
>
> ]
> }

- GET `/api/v1/metrix` - Retrieves `SearchEngine` usage statistics

> **Request: **
>
> http://localhost:8000/api/v1/metrix
>
> **Response:**
>
> {
> "api": "Py-API",
> "version": "1.0.0",
> "status": "SUCCESS",
> "data": {
>  "liveQueries": 0,
>  "totalSearches": 292,
>  "totalArticles": 3819
> 	}
> }



## API: Go

**Microservice Communication API**

- Language: GoLang
- Framework: `gorilla/mux`

- Format: `JSON`
- Port: 5000:-



**Routes**

- POST `/api/v1/query` - Send query to `SearchEngine` Service

> **Request: **
>
> {
> 	"identifier": "sampl3id3nt1f1er",
> 	"query": "What Is A Cookie?"
> }
>
> **Response:**
>
> {
> "api": "Go-API",
> "version": "1.0.0",
> "status": "SUCCESS",
> "data": {
>  "identifier": "sampl3id3nt1f1er",
>  "query": "What Is A Cookie?"
> 	}
> } 

- GET `/api/v1/results` - Retrieves Results from `SearchEngine` Service as JSON

> http://localhost:5000/api/v1/results/<identifier> 
>
> **Response:**
>
> {
> "api": "Go-API",
> "version": "1.0.0",
> "status": "SUCCESS",
> "identifier": "sampl3id3nt1f1er",
> "query": "What Is A Cookie?",
> "time_taken": "100.00 ms",
> "results": [
>  {      "title": "What Are Cookies Made Of?",
>    "url": "http://www.example.com/cookie-ingredients",
>    "source": "example.com - Article - William Smith"
>  },
>
> ​	{      "title": "How Are Cookies Made?",
> ​      "url": "http://www.example.com/cookie-ingredients",
> ​      "source": "example.com - Article - John Doe"
> ​    }
>
> ]
> }

- GET `/api/v1/metrix` - Retrieves `SearchEngine` usage statistics

> **Request: **
>
> http://localhost:5000/api/v1/metrix
>
> **Response:**
>
> {
> "api": "Py-API",
> "version": "1.0.0",
> "status": "SUCCESS",
> "data": {
>  "liveQueries": 0,
>  "totalSearches": 292,
>  "totalArticles": 3819
> 	}
> }



## Service: SearchEngine

**BM25 Based Search Engine**

- Language: Python 3
- Framework: `Flask`
- Format: `JSON`
- Method:
  - Collects query from `Redis DB0`
  - Ranks local corpus according to query provided
  - Returns subsection of corpus as  results via `Redis DB1`



## Service: ContentScraper

**Automated Web Scraping Service**

- Language: Python 3
- Framework: `Scrapy`
- Format: `JSON`
- Method:
  - Scraped predefined list of websites
  - Collects data that matches predetermined criteria
  - Stores scraped data in MongoDB - `ContentScraperDB`



## Service: SpellChecker / LangFormatter

**Basic English Language Sentence Formatter & Spell Checker**

- Language: Python 3
- Format: `JSON`
- Method:
  - Standardises spelling of corpus if provided
  - Removes unwanted punctuation from input
  - Removes unwanted non-standard English characters from input
  - Replaces incorrectly spelt words with correct version
  - Replaces incorrectly transliterated words with correct version



## Database: Redis

**Temporarily Stores Incoming Queries & Subsequently Generated Results**

- Format: `JSON`
- Modules: `RedisJSON`
- Port: 6379:-



### DB 0

- Type: JSON Stream
- Traffic Type: Search Queries
- Traffic Direction:  API -> `SearchEngine`



### DB 1

- Type: JSON Set / Get
- Traffic Type: Search Results
- Traffic Direction: `SearchEngine` -> API



## Database: MongoDB

**Data Storage For Services**

- Port: 27020:-



### ContentScraperDB

Stores URLs + Titles from `ContentScraper`



> **Record Format:**
>
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



**Collections**

- `scrapedData` - List of all scraped URLs with titles corrected by `SpellChecker`



### SearchEngineDB

Stores URLs + Titles  as ranked by BM25 from `SearchEngine`



> **Record Format**
>
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



**Collections**

- `returnedResults` - Contains list of all results generated by `SearchEngine` 
