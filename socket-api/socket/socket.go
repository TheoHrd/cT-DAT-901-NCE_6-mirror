package socket

import (
	"fmt"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // Not secure
	},
}

func handleWebSocket(w http.ResponseWriter, r *http.Request) {

	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		fmt.Println("Erreur lors de l'upgrade WebSocket :", err)
		return
	}
	defer conn.Close()

	fmt.Println("Nouvelle connexion WebSocket établie")

	for {
		_, message, err := conn.ReadMessage()
		if err != nil {
			fmt.Println("Connexion fermée :", err)
			break
		}

		fmt.Printf("Message reçu : %s\n", message)

		
		err = conn.WriteMessage(websocket.TextMessage, []byte("Message reçu : "+string(message)))
		if err != nil {
			fmt.Println("Erreur lors de l'envoi du message :", err)
			break
		}
	}
}

func StartServer(port string) {


	http.HandleFunc("/ws", handleWebSocket)

	fmt.Println("Serveur WebSocket démarré sur le port", port)
	err := http.ListenAndServe(port, nil)
	if err != nil {
		fmt.Println("Erreur lors du démarrage du serveur :", err)
	}
}
