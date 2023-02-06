package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/go-redis/redis/v8"
	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const (
	APIName    string = "Go-API"
	APIVersion string = "1.0.0"
	redisAddr  string = "redis:6379" // Redis Address
	redisPass  string = "Password:)" // Redis Password
	mongoHost  string = "mongo-db"   // Mongo Docker Hostname
	mongoPort  string = "27017"      // Mongo Host Port
)

var (
	rCtx = context.Background() // Redis
	mCtx = context.TODO()       // MongoDB
)

// Redis DB Connection
func redisDB(x int) *redis.Client {
	client := redis.NewClient(&redis.Options{
		Addr:     redisAddr,
		Password: redisPass,
		DB:       x,
	})

	err := client.Ping(rCtx).Err()
	if err != nil {
		log.Fatal("Redis: Failed To Connect - ", err)
	}

	return client
}

// mongoDB DB Connection
func mongoDB(host, port string) *mongo.Client {
	clientOptions := options.Client().ApplyURI("mongodb://" + host + ":" + port + "/")
	client, err := mongo.Connect(context.TODO(), clientOptions)

	if err != nil {
		log.Fatal("MongoDB: Failed To Connect - ", err)
	}

	err = client.Ping(context.TODO(), nil)

	if err != nil {
		log.Fatal(err)
	}

	return client
}

// Function Returns Search Engine Stats
func dbStats() (x, y, xz int64) {

	redis := redisDB(1)
	x = redis.DBSize(rCtx).Val()

	mongo := mongoDB(mongoHost, mongoPort)
	defer mongo.Disconnect(mCtx)

	y, err := mongo.Database("SearchEngineDB").Collection("returnedResults").EstimatedDocumentCount(mCtx)

	if err != nil {
		log.Fatal("dbStats() SearchEngineDB Error - ", err)
	}

	z, err := mongo.Database("ContentScraperDB").Collection("scrapedData").EstimatedDocumentCount(mCtx)

	if err != nil {
		log.Fatal("dbStats() ContentScraperDB Error - ", err)
	}

	return x, y, z
}

func redisKeyStatus(identifier string) bool {

	var t int = 0
	var response bool

	db := redisDB(1)
	defer db.Close()

	for {
		exists, err := db.Do(rCtx, "EXISTS", "id:"+identifier).Bool()

		if err != nil {
			log.Fatal("Command Failed: ", err)
			break
		}

		time.Sleep(100 * time.Millisecond)
		t += 1

		if exists {
			response = true
			return response
		} else if t == 25 {
			response = false
			return response
		}
	}

	return response

}

type queryData struct {
	Identifier string `json:"identifier"`
	Query      string `json:"query"`
}

type queryResponse struct {
	API     string    `json:"api"`
	Version string    `json:"version"`
	Status  string    `json:"status"`
	Data    queryData `json:"data"`
}

// Function Receives Query from Client
func queryAPI(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("content-type", "application/json")

	// Check That Identifier & Query Parameters Exist

	var body queryData

	err := json.NewDecoder(r.Body).Decode(&body)

	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		log.Fatal(err)
	}

	identifier := body.Identifier
	query := body.Query

	db := redisDB(0)
	defer db.Close()

	// Sends Message: API -> Stream -> SearchEngine
	db.XAdd(rCtx, &redis.XAddArgs{
		Stream:       "streamA",
		MaxLen:       0,
		MaxLenApprox: 0,
		ID:           "",
		Values: map[string]interface{}{
			"identifier": identifier,
			"query":      query,
		},
	})

	responseData := queryData{
		Identifier: identifier,
		Query:      query,
	}

	response := queryResponse{
		API:     APIName,
		Version: APIVersion,
		Status:  "SUCCESS",
		Data:    responseData,
	}

	w.WriteHeader(http.StatusAccepted)
	json.NewEncoder(w).Encode(response)
}

type resultsData struct {
	Title  string `json:"title"`
	URL    string `json:"url"`
	Source string `json:"source"`
}

type resultsResponse struct {
	API        string        `json:"api"`
	Version    string        `json:"version"`
	Status     string        `json:"status"`
	Identifier string        `json:"identifier"`
	Query      string        `json:"query"`
	TimeTaken  string        `json:"time_taken"`
	Results    []resultsData `json:"results"`
}

type errorResponse struct {
	API        string `json:"api"`
	Version    string `json:"version"`
	Identifier string `json:"identifier"`
	Status     string `json:"status"`
}

// Function Collects Results From Redis And Returns Them To Client
func resultsAPI(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("content-type", "application/json")

	identifier, found := mux.Vars(r)["identifier"]

	// If Identifier Does Not Exit
	if !found {
		response := errorResponse{
			API:        APIName,
			Version:    APIVersion,
			Identifier: identifier,
			Status:     "ERROR: No Identifier",
		}

		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(response)
	}

	db := redisDB(1)
	defer db.Close()

	exists := redisKeyStatus(identifier)

	// If Identifer Exists: Fetch Results
	if exists {

		// Collect Query From Redis
		query, err := db.Do(rCtx, "JSON.GET", "id:"+identifier, ".query").Text()

		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			log.Fatal("Command Failed: ", err)
		}

		query = strings.Trim(query, "\"")

		// Collect Results From Redis
		results, err := db.Do(rCtx, "JSON.GET", "id:"+identifier, ".results").Text()

		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			log.Fatal("Command Failed: ", err)
		}

		var resultsJSON []resultsData
		json.Unmarshal([]byte(results), &resultsJSON)

		// Collect Time Taken From Redis
		time_taken, err := db.Do(rCtx, "JSON.GET", "id:"+identifier, ".time_taken").Text()

		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			log.Fatal("Command Failed: ", err)
		}

		time_taken = strings.Trim(time_taken, "\"")

		response := resultsResponse{
			API:        APIName,
			Version:    APIVersion,
			Status:     "SUCCESS",
			Identifier: identifier,
			Query:      query,
			TimeTaken:  time_taken,
			Results:    resultsJSON,
		}

		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(response)

	}

	if !exists {
		response := errorResponse{
			API:        APIName,
			Version:    APIVersion,
			Identifier: identifier,
			Status:     "ERROR: Identifier Does Not Exist",
		}

		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(response)
	}

}

type metrixData struct {
	LiveQueries   int64 `json:"liveQueries"`
	TotalSearches int64 `json:"totalSearches"`
	TotalArticles int64 `json:"totalArticles"`
}

type metrixResponse struct {
	API     string     `json:"api"`
	Version string     `json:"version"`
	Status  string     `json:"status"`
	Data    metrixData `json:"data"`
}

// Function Returns Search Engine Statistics To Client
func metrix(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("content-type", "application/json")

	var x, y, z int64 = dbStats()

	responseData := metrixData{
		LiveQueries:   x,
		TotalSearches: y,
		TotalArticles: z,
	}

	response := metrixResponse{
		API:     APIName,
		Version: APIVersion,
		Status:  "SUCCESS",
		Data:    responseData,
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

// API URLS & Handle Endpoints
func main() {
	router := mux.NewRouter()

	router.HandleFunc("/api/v1/search", queryAPI).Methods("POST")
	router.HandleFunc("/api/v1/results/{identifier}", resultsAPI).Methods("GET")
	router.HandleFunc("/api/v1/metrix", metrix).Methods("GET")

	http.ListenAndServe(":80", router)
}
