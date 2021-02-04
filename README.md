# reSearch

Search Engine and Website Index Service

[toc]

## Steps

- User enters Query
- Query is sent to API with Unique Identifier
- User is redirected to `url_for('results')`

- API receives Query + Identifier
- API send query to `SearchEngine` via `Redis-StreamA`

- `SearchEngine` receives Query
- `SearchEngine` uses `rank-BM25` to rank content from `MongoCS` database according to Query
- `SearchEngine` saves list of ranked links to `MongoSE`
  
- `SearchEngine` alerts `API` about list of links
  
- `API` pulls list of links from `MongoSE.db`
- `API` sends list of links to `url_for('results')`

- `Site` receives list of links
- `Site` displays list of links at `url_for('results')`

- `ContentScraper` runs once every 24 hours to look for new URLs to harvest data from

  

## Services

### Website

User Web Interface

- User Accessible End-Points

  - www.site.com/home
  - www.site.com/results

- Admin Accessible End-Points

  - www.site.com/admin

    

### GlobalAPI

Handles Communication between Front and Backend



### Redis Stream

Handles Backend Inter-Service Communication

 

### SearchEngine 

Ranks stored data according to Query and returns results to  `GlobalAPI` via **Stream-B**



### ContentScraper

Scrapes Sites and collects relevant data



### Metrix

Collects Service & Usage Metrics 



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
  
    

### Database

- RedisJSON: Redis-API
- Stores Queries from Form
- Redis Streams storage DB



## Docs: Redis

### DB 0

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
>​	"global_id": "0001"
>
>​	"identifier": random 10 char string
>
>​	"URL": "www.example.com/blogpost1"
>
>​	"title": "First Blog Post"
>
>}



### MongoCS

URLs + Titles from ContentScraper

All Records have form:

>{
>
>​	"global_id": "0001"
>
>​	"title": "First Blog Post"
>
>​	"URL": "www.example.com/blogpost1"
>
>}



## Checklist

### Build: General 

- Set up WSGI

- Set up Nginx

  


### Build: Content Scraper

- [ ] Docker Cron Job
- [ ] Add Multiple Sites
- [ ] Save Article Content for ranking



### Build: Search Engine Build

- [ ] Rank by Article Content




### Build: Site

- [ ] Move Response to Sessions to prevent reload issues

  


### Launch

- [ ] Remove `debug=True` from Flask scripts

- [ ] Research alternative to local `.env` files

- [ ] Secure Databases

- [ ] Secure Admin Routes

- [ ] Create List of most common Queries to be cached

- [ ] Research Docker Load Balancing

  

## Cloud Providers

### Hosting

- AWS
- Python Anywhere
- Digital Ocean

### Caching

- Redis Labs

### Databases

- Mongo Atlas
