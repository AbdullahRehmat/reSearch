package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"

	"github.com/go-redis/redis/v8"
	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var (
	RedisAddr string = "localhost:6379"
	RedisPass string = "password"
	RCtx             = context.Background()
	MCtx             = context.TODO()
)

// Connect  to Redis and MongoDB
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

type MongoDoc struct {
	ID   string
	Data string
}

// Function: Get Results From Redis
func redisResults(identifier string) string {
	db := RedisDB(0)
	defer db.Close()
	data := db.Get(RCtx, identifier)
	return data.String()
}

// Function: Get Results From MongoDB
func mongoResults(identifier string) MongoDoc {

	var results MongoDoc

	db := MongoDB("localhost", "27018")
	defer db.Disconnect(MCtx)
	coll := db.Database("SearchEngineDB").Collection("htmlResults")
	filter := bson.D{{Key: "_id", Value: identifier}}
	err := coll.FindOne(MCtx, filter).Decode(&results)

	if err != nil {
		log.Fatal(err)
	}

	return results
}

// Receive Query from Client
func queryAPI(w http.ResponseWriter, r *http.Request) {
	identifier := r.FormValue("identifier")
	query := r.FormValue("query")

	if identifier == nil {
		log.Fatal("NEEDS TO BE COMPLETED")
	}

	if query == nil {
		log.Fatal("NEEDS TO BE COMPLETED")
	}
}

// Provide Results to Client
func resultsAPI(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("content-type", "application/json")
	params := mux.Vars(r)
	identifier := params["identifier"]

	results := redisResults(identifier)
	json.NewEncoder(w).Encode(results)
}

// Provide Metrix & Stats
func metrix(w http.ResponseWriter, r *http.Request) {

}

// Create API Endpoints
func main() {
	router := mux.NewRouter()

	router.HandleFunc("/api/query", queryAPI).Methods("POST")
	router.HandleFunc("/api/{identifier}", resultsAPI).Methods("GET")
	router.HandleFunc("/metrix", metrix).Methods("GET")

	http.ListenAndServe(":80", router)
}
