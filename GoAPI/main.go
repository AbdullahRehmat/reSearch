package main

import (
	"context"
	"fmt"
	"log"

	"github.com/go-redis/redis/v8"
	//"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var (
	RedisAddr string = "localhost:6379"
	RedisPass string = "password"
	RCtx             = context.Background()

	MongoPort string = ":27018"
)

func RDB(x int) *redis.Client {
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

func MDB(dbHost, dbName, dbColl string) *mongo.Collection {

	var MongoAddr string = "mongodb://" + dbHost + MongoPort

	clientOptions := options.Client().ApplyURI(MongoAddr)
	client, err := mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		log.Fatal("Failed to Connect to MongoDB: ", err)
	}

	collection := client.Database(dbName).Collection(dbColl)

	return collection
}

//func getRedisResults(identifier string) string {
//	return "test"
//}
//
//func getMongoResults(identifier string) string {
//	return "test"
//}
//
//func apiEndpoints() {
//}

func main() {
	rDB0 := RDB(0)
	defer rDB0.Close()
	fmt.Println(rDB0.Ping(RCtx))

	mDB0 := MDB("localhost", "SearchEngineDB", "htmlResults")
	fmt.Print(mDB0.CountDocuments(context.TODO(), nil, nil))
}
