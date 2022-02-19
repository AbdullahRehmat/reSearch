package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"time"

	"github.com/go-redis/redis/v8"
	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const (
	RedisAddr string = "redis-api:6379" // Redis Address
	RedisPass string = "Password:)"     // Redis Password
)

var (
	RCtx = context.Background() // Redis
	MCtx = context.TODO()       // MongoDB
)

// Redis DB Connection
func RedisDB(x int) *redis.Client {
	db := redis.NewClient(&redis.Options{
		Addr:     RedisAddr,
		Password: RedisPass,
		DB:       x,
	})

	err := db.Ping(RCtx).Err()
	if err != nil {
		log.Fatal("Redis: Failed To Connect - ", err)
	}

	return db
}

// MongoDB DB Connection
func MongoDB(host, port string) *mongo.Client {
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

	db1 := MongoDB("mongo-se", "27017")
	defer db1.Disconnect(MCtx)
	x, err := db1.Database("SearchEngineDB").Collection("Results-C1").EstimatedDocumentCount(MCtx)

	if err != nil {
		log.Fatal(err)
	}

	db2 := MongoDB("mongo-cs", "27017")
	defer db1.Disconnect(MCtx)
	y, err = db2.Database("ContentScraperDB").Collection("ScrapedData-C1").EstimatedDocumentCount(MCtx)

	db3 := RedisDB(1)
	z = db3.DBSize(RCtx).Val()

	if err != nil {
		log.Fatal(err)
	}

	return x, y, z
}

type QueryData struct {
	Identifier string `json:"identifier"`
	Query      string `json:"query"`
}

type QueryResponse struct {
	Status string    `json:"status"`
	Data   QueryData `json:"data"`
}

// Function Receive Query from Client
func queryAPI(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("content-type", "application/json")

	var body QueryData

	err := json.NewDecoder(r.Body).Decode(&body)

	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		log.Fatal(err)
	}

	identifier := body.Identifier
	query := body.Query

	db := RedisDB(0)
	defer db.Close()

	db.XAdd(RCtx, &redis.XAddArgs{
		Stream:       "streamA",
		MaxLen:       0,
		MaxLenApprox: 0,
		ID:           "",
		Values: map[string]interface{}{
			"identifier": identifier,
			"query":      query,
		},
	})

	responseData := QueryData{
		Identifier: identifier,
		Query:      query,
	}

	response := QueryResponse{
		Status: "success",
		Data:   responseData,
	}

	w.WriteHeader(http.StatusAccepted)
	json.NewEncoder(w).Encode(response)
}

type ResultsResponse struct {
	Status     string      `json:"status"`
	Identifier string      `json:"identifier"`
	Results    interface{} `json:"results"`
}

// Function Return Results to Client
func resultsAPI(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("content-type", "application/json")

	params := mux.Vars(r)
	identifier := params["identifier"]

	time.Sleep(500 * time.Millisecond) // Delay Allows SearchEngine Time To Return Response

	db := RedisDB(1)
	defer db.Close()

	var id string = "id:" + identifier
	results, err := db.Do(RCtx, "JSON.GET", id, ".results").Result()

	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		log.Fatal("Command Failed: ", err)
	}

	response := ResultsResponse{
		Status:     "success",
		Identifier: identifier,
		Results:    results,
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

type MetrixData struct {
	TotalQueries  int64 `json:"totalQueries"`
	TotalArticles int64 `json:"totalArticles"`
	LiveQueries   int64 `json:"liveQueries"`
}

type MetrixResponse struct {
	Status string     `json:"status"`
	Data   MetrixData `json:"data"`
}

// Function Return Metrix & Stats
func metrix(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("content-type", "application/json")

	var x, y, z int64 = dbStats()

	responseData := MetrixData{
		TotalQueries:  x,
		TotalArticles: y,
		LiveQueries:   z,
	}

	response := MetrixResponse{
		Status: "success",
		Data:   responseData,
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
