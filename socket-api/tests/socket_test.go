package main

import (
	"testing"
	"time"
	"socket-api/socket"
	"fmt"

	"github.com/gorilla/websocket"
)

func TestServer(t *testing.T) {
	t.Log("Test du serveur socket")

	go func() {
		socket.StartServer(":3006")
	}()
	time.Sleep(1 * time.Second)

	// URL du serveur WebSocket
	url := "ws://localhost:3006/ws"

	// Connexion au serveur
	conn, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		t.Fatalf("Erreur lors de la connexion : %v", err)
	}
	defer conn.Close()

	fmt.Println("Connecté au serveur WebSocket")

	// Envoyer un message
	message := "Bonjour, WebSocket!"
	err = conn.WriteMessage(websocket.TextMessage, []byte(message))
	if err != nil {
		t.Fatalf("Erreur lors de l'envoi du message : %v", err)
	}

	// Lire la réponse
	_, response, err := conn.ReadMessage()
	if err != nil {
		t.Fatalf("Erreur lors de la lecture de la réponse : %v", err)
	}

	fmt.Printf("Réponse du serveur : %s\n", response)




	expectedResponse := "Message reçu : Bonjour, serveur!\n"
	if string(response) != expectedResponse {
		t.Errorf("Réponse incorrecte : attendu %q, obtenu %q", expectedResponse, response)
	} else {
		fmt.Println("Réponse OK")
	}
}
