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
	RedisAddr string = "redis-api:6379"
	RedisPass string = "Password:)"
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
		log.Fatal("Failed to Connect to Redis: ", err)
	}

	return db
}

// MongoDB DB Connection
func MongoDB(host, port string) *mongo.Client {
	clientOptions := options.Client().ApplyURI("mongodb://" + host + ":" + port + "/")
	client, err := mongo.Connect(context.TODO(), clientOptions)

	if err != nil {
		log.Fatal("Failed to Connect to MongoDB ", err)
	}

	err = client.Ping(context.TODO(), nil)

	if err != nil {
		log.Fatal(err)
	}

	return client
}

// Returns Search Engine Stats
func dbStats() (x, y, z int64) {

	db1 := MongoDB("mongo-se", "27017")
	defer db1.Disconnect(MCtx)
	x, err := db1.Database("SearchEngineDB").Collection("ResultsC1").EstimatedDocumentCount(MCtx)

	if err != nil {
		log.Fatal(err)
	}

	db2 := MongoDB("mongo-cs", "27017")
	defer db1.Disconnect(MCtx)
	y, err = db2.Database("ContentScraperDB").Collection("ScrapedDataC1").EstimatedDocumentCount(MCtx)

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

type QueryReponse struct {
	Message string    `json:"message"`
	Data    QueryData `json:"data"`
}

// Receive Query from Client
// Unable to get IDENTIFIER AND QUERY
func queryAPI(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("content-type", "application/json")

	var body QueryData

	err := json.NewDecoder(r.Body).Decode(&body)

	if err != nil {
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

	response := QueryReponse{
		Message: "Success",
		Data:    responseData,
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

// Return Results to Client
func resultsAPI(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("content-type", "application/json")

	params := mux.Vars(r)
	identifier := params["identifier"]

	time.Sleep(2 * time.Second) // To Allow SearchEngine Time To Return Response

	db := RedisDB(1)
	defer db.Close()
	results, err := db.Get(RCtx, identifier).Result()

	if err != nil {
		log.Fatal(err)
	}

	w.WriteHeader(http.StatusAccepted)
	json.NewEncoder(w).Encode(results)
}

type MetrixReponse struct {
	TotalQueryCount   int64 `json:"totalQueryCount"`
	TotalArticleCount int64 `json:"totalArticleCount"`
	LiveQueryCount    int64 `json:"liveQueryCount"`
}

// Return Metrix & Stats
func metrix(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("content-type", "application/json")

	var x, y, z int64 = dbStats()

	data := MetrixReponse{
		TotalQueryCount:   x,
		TotalArticleCount: y,
		LiveQueryCount:    z,
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(data)
}

// Create API URLS & Handle Endpoints
func main() {
	router := mux.NewRouter()

	router.HandleFunc("/api/v1/query", queryAPI).Methods("POST")
	router.HandleFunc("/api/v1/results/{identifier}", resultsAPI).Methods("GET")
	router.HandleFunc("/api/v1/metrix", metrix).Methods("GET")

	http.ListenAndServe(":80", router)
}
