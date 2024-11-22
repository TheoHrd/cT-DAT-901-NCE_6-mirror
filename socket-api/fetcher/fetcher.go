package fetcher

import (
	"fmt"
	"encoding/json"

	"github.com/go-resty/resty/v2"
)

func queryDruidWithResty(druidURL, sqlQuery string) error {
	// Créer un client Resty
	client := resty.New()

	// Construire la requête
	resp, err := client.R().
		SetHeader("Content-Type", "application/json").
		SetBody(map[string]string{"query": sqlQuery}).
		Post(druidURL)

	if err != nil {
		return fmt.Errorf("erreur lors de l'envoi de la requête : %v", err)
	}

	// Vérifier le statut de la réponse
	if resp.StatusCode() != 200 {
		return fmt.Errorf("erreur de la réponse du serveur : %s (%d)", resp.String(), resp.StatusCode())
	}

	// Décoder la réponse JSON
	var result []map[string]interface{}
	if err := json.Unmarshal(resp.Body(), &result); err != nil {
		return fmt.Errorf("erreur lors du décodage de la réponse JSON : %v", err)
	}

	// Afficher le résultat
	for _, row := range result {
		fmt.Println(row)
	}
	return nil
}

func DruidClient() {

	druidURL := "http://localhost:8888/druid/v2/sql"
	sqlQuery := "SELECT * FROM sentiment_analysis"

	// Envoyer la requête avec Resty
	if err := queryDruidWithResty(druidURL, sqlQuery); err != nil {
		fmt.Println("Erreur :", err)
	} else {
		fmt.Println("Requête réussie.")
	}
}