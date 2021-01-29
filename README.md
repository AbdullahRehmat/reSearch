# reSearch

Search Engine and Website Index Service intended for reseach purposes

[toc]

## Steps

- User enters Query
- Query is sent to API
- User is redirected to `url_for('results')`

-

- API receives Query
- API send query to `SearchEngine` via `Redis-StreamA`

-

- `SearchEngine` receives Query
- `SearchEngine` uses `rank-BM25` to rank content from `ContentScraper` database according to Query
- `SearchEngine` saves list of ranked links to `SEngine.db`
  - `SearchEngine` alerts `API` about list of links

-

- `API` pulls list of links from `MongoSE.db`
- `API` sends list of links to `url_for('results')`

-

- `Site` receives list of links
- `Site` displays list of links at `url_for('results')`

-

- `ContentScraper` runs once every 24 hours to look for new URLs to harvest data from
- Harvested Data is stored in `MongoCS.DB`



## Services

### Website

User Web Interface

- Python + Flask

- User Accessible End-Points

  - www.site.com/home
  - www.site.com/results

- Admin Accessible End-Points

  - www.site.com/admin

    

### GlobalAPI

Handles Communication between Front and Backend

- Python + `Flask-RESTful`

  

### Redis Stream

Handles Backend Inter-Service Communication

 

### SearchEngine 

Ranks stored data according to Query and returns results to  `GlobalAPI` via **Stream-B**

- Python + `Rank-BM25`



### ContentScraper

Scrapes Sites and collects relevant data

- Python + `scrapy`



### Stats

Collects Service & Usage Metrics 



## Docs: GlobalAPI 

Handles communication between Front and Backend services



### Route   `/query` 

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
  - Returns current Query from DB
- **POST**

  - Adds a new Query to DB



### Route   `/results`



 

### Route   `/test`

API: test_API

- **GET**
  - Route for Postman testing purposes
  - **REMOVE BEFORE DEPLOYMENT**



### Database

- RedisJSON: Redis-API
- Stores Queries from Form
- Acts a in-memory storage for Redis-Streams



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

URLs + Titles in Ranked order

All Records have form:

>{
>
>​	"id": "0001"
>
>​	"URL": "www.example.com/blogpost1"
>
>​	"title": "First Blog Post"
>
>}



### MongoCS

URLs + Titles in order of scraping

All Records have form:

>{
>
>​	"id": "0001"
>
>​	"URL": "www.example.com/blogpost1"
>
>​	"title": "First Blog Post"
>
>}



## Checklist

### Build: General 

- [ ] Create Databases

- [x] Connect `forms.query.data` to streams

- [x] Check `SearchEngine` is able to read results

- [ ] Add `/results` to `GlobalAPI`

  

- [ ] For every request spawn new workers

- [ ] Research K8



### Build: Content Scraper

- [ ] Runs once every 24 hours
- [ ] Store Website URLs in persistent storage
- [ ] Scrapes URLs for Titles `articleTitleList`
- [ ] Connect to DB



### Build: Search Engine Build

- [ ] Access Data from `scraperDB`

- [ ] Connect to  DB

  


### Build: Site

- [ ] Add loading animation while waiting for results
- [ ] Research JS Frameworks
- [ ] Tailwind CSS?



### Launch

- [ ] Remove `api/test` route
- [ ] Remove `debug=True` from Flask scripts
- [ ] Research alternative to local `.env` files
- [ ] Secure Admin Routes
- [ ] Secure Databases
- [ ] Create List of most common Queries to be cached
- [ ] Research Docker Load Balancing
- [ ] Research Docker Microservice Scaling
- [ ] Docker Frontend + Backend Networks
