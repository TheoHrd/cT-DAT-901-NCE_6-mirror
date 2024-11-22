package main

import (
	//"fmt"
	"sync"
	"socket-api/socket"
	"socket-api/fetcher"
)


func main() {

	var wg sync.WaitGroup

	wg.Add(1)
	go func() {
		defer wg.Done()
		socket.StartServer(":3006")
	}()

	fetcher.DruidClient()
}