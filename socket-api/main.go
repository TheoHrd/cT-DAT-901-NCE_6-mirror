package main

import (
	//"fmt"
	"socket-api/fetcher"
	"socket-api/socket"
	"sync"
	"time"
)

// Cache pour les données
var dataCache []map[string]interface{}
var mu sync.RWMutex

func updateCache(data []map[string]interface{}) {
	mu.Lock()
	defer mu.Unlock()
	dataCache = data
}

func getCache() []map[string]interface{} {
	mu.RLock()
	defer mu.RUnlock()
	return dataCache
}

func main() {

	var wg sync.WaitGroup

	wg.Add(1)
	go func() {
		defer wg.Done()
		socket.StartServer(":3006")
	}()

	ticker := time.NewTicker(1 * time.Second)
	quit := make(chan struct{})
	go func() {
		for {
			select {
			case <-ticker.C:
				data, err := fetcher.FetchDruid()

				if err != nil {
					updateCache(data)
				}
			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()

}
