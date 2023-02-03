package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"strings"

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
func dbStats() (x, y, z int64) {

	mongo := mongoDB(mongoHost, mongoPort)
	defer mongo.Disconnect(mCtx)
	x, err := mongo.Database("SearchEngineDB").Collection("returnedResults").EstimatedDocumentCount(mCtx)

	if err != nil {
		log.Fatal("dbStats() SearchEngineDB Error - ", err)
	}
	y, err = mongo.Database("ContentScraperDB").Collection("scrapedData").EstimatedDocumentCount(mCtx)

	if err != nil {
		log.Fatal("dbStats() ContentScraperDB Error - ", err)
	}

	redis := redisDB(1)
	z = redis.DBSize(rCtx).Val()

	if err != nil {
		log.Fatal("RedisDB(1) Error - ", err)
	}

	return x, y, z
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
		Status:  "success",
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
	TimeTaken  string        `json:"time_taken"`
	Results    []resultsData `json:"results"`
}

// Function Collects Results From Redis And Returns Them To Client
func resultsAPI(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("content-type", "application/json")

	identifier, found := mux.Vars(r)["identifier"]

	// If Identifier Does Not Exit
	if !found {
		response := resultsResponse{
			API:        APIName,
			Version:    APIVersion,
			Status:     "ERROR: No Identifier",
			Identifier: identifier,
		}

		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(response)
	}

	var jsonID string = "id:" + identifier

	db := redisDB(1)
	defer db.Close()

	// Wait Until Results Appear In Redis DB
	for {

		exists, err := db.Do(rCtx, "EXISTS", jsonID).Bool()

		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			log.Fatal("Command Failed: ", err)

			break
		}

		// If Identifer Exists: Fetch Results
		if exists {

			results, err := db.Do(rCtx, "JSON.GET", jsonID, ".results").Text()

			if err != nil {
				w.WriteHeader(http.StatusBadRequest)
				log.Fatal("Command Failed: ", err)
			}

			var resultsJSON []resultsData
			json.Unmarshal([]byte(results), &resultsJSON)

			time_taken, err := db.Do(rCtx, "JSON.GET", jsonID, ".time_taken").Text()
			time_taken = strings.Trim(time_taken, "\"")

			if err != nil {
				w.WriteHeader(http.StatusBadRequest)
				log.Fatal("Command Failed: ", err)
			}

			response := resultsResponse{
				API:        APIName,
				Version:    APIVersion,
				Status:     "success",
				Identifier: identifier,
				TimeTaken:  time_taken,
				Results:    resultsJSON,
			}

			w.WriteHeader(http.StatusOK)
			json.NewEncoder(w).Encode(response)

			break
		}

	}

}

type metrixData struct {
	TotalQueries  int64 `json:"totalQueries"`
	TotalArticles int64 `json:"totalArticles"`
	LiveQueries   int64 `json:"liveQueries"`
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
		TotalQueries:  x,
		TotalArticles: y,
		LiveQueries:   z,
	}

	response := metrixResponse{
		API:     APIName,
		Version: APIVersion,
		Status:  "success",
		Data:    responseData,
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

// API URLS & Handle Endpoints
func main() {
	router := mux.NewRouter()

	router.HandleFunc("/api/v1/query", queryAPI).Methods("POST")
	router.HandleFunc("/api/v1/results/{identifier}", resultsAPI).Methods("GET")
	router.HandleFunc("/api/v1/metrix", metrix).Methods("GET")

	http.ListenAndServe(":80", router)
}
