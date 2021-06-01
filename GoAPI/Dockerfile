FROM golang:1.16

WORKDIR /go/src/app
COPY . .

#RUN go get -d -v ./...
#RUN go install -v ./...

#CMD ["go", "run", "main.go"]

RUN go mod download
RUN go build -o main .

CMD ["./main"]