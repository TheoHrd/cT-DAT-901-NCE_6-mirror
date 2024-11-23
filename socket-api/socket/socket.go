package socket

import (
	"fmt"
	"net/http"
	"log"
	"sync"
	"time"

	"github.com/gorilla/websocket"
)

// Gestion des connexions clients
var clients = make(map[*websocket.Conn]bool) // Ensemble des clients connectés
var broadcast = make(chan string)           // Canal pour diffuser les messages
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // Autoriser toutes les origines
	},
}
var mutex = sync.Mutex{} // Pour protéger l'accès aux clients


func handleWebSocket(w http.ResponseWriter, r *http.Request) {

	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("Erreur de mise à niveau : %v", err)
		return
	}
	defer ws.Close()

	mutex.Lock()
	clients[ws] = true
	mutex.Unlock()

	for {
		var msg string
		err := ws.ReadJSON(&msg)
		if err != nil {
			log.Printf("Client déconnecté : %v", err)
			mutex.Lock()
			delete(clients, ws)
			mutex.Unlock()
			break
		}
		// Ajouter le message reçu au canal broadcast
		broadcast <- msg
		time.Sleep(1 * time.Second)
	}
	
}

func handleMessages() {
	for {
		// Recevoir un message à diffuser
		msg := <-broadcast

		// Envoyer à tous les clients connectés
		mutex.Lock()
		for client := range clients {
			err := client.WriteJSON(msg)
			if err != nil {
				log.Printf("Erreur lors de l'envoi à un client : %v", err)
				client.Close()
				delete(clients, client)
			}
		}
		mutex.Unlock()
	}
}

// Fonction publique pour envoyer un message à tous les clients
func SendMessageToAll(message string) {
	broadcast <- message
}

func StartServer(port string) {

	http.HandleFunc("/ws", handleWebSocket)

	go handleMessages()

	fmt.Println("Serveur WebSocket démarré sur le port", port)
	err := http.ListenAndServe(port, nil)
	if err != nil {
		fmt.Println("Erreur lors du démarrage du serveur :", err)
	}
}
