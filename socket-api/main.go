package main

import (
	"fmt"
	"sync"
	"socket-api/socket"
	//"socket-api/druid"
)



func main() {
	fmt.Printf("yo")


	var wg sync.WaitGroup

	wg.Add(1)
	go func() {
		defer wg.Done()
		socket.StartServer(":3006")
	}()
}
