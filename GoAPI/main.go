package main

import (
	"context"
	"log"

	"github.com/go-redis/redis/v8"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var (
	RedisAddr string = "localhost:6379"
	RedisPass string = "password"
	RCtx             = context.Background()
	MCtx             = context.TODO()
)

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

func MongoDB(host string) *mongo.Client {
	clientOptions := options.Client().ApplyURI("mongodb://" + host + ":27019/")
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

// Connect  to Redis and MongoDB
// Function: Get Results From Redis
// Function: Get Results From MongoDB
// Create API Endpoints
// Assign relavent Logic to API Endpoints

func main() {
	//m := MongoDB("localhost")
	//defer m.Disconnect(MCtx)
	//collection := m.Database("ContentScraperDB").Collection("ScrapedDataS1")
	//fmt.Println(collection.EstimatedDocumentCount(MCtx))

}
