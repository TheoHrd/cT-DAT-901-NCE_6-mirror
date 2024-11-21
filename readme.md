

Scrapper -> Druid -> Socket Api -> Dashboard


## Services et ports

### Postgres
- **Port** : `5432`

### Scrapper
- **Port** : `8000`
- **Description** : Scrapper python vers Google trends, Binance et flux rss.

### Dashboard
- **Port** : `3005`
- **Description** : Dashboard React des informations traitées par Druid.

### Socket api
- **Port** : `3006`
- **Description** : Fais la passerelle entre Druid et le dashboard. Des requêtes périodiques sont effectuées vers Druid puis sont transférées en socket vers les clients.


### Router (console Druid)
- **Port** : `8081`
- **Description** : Ce service sert l'interface web (Druid Console).
- **Accès** : [http://<hostname>:8081](http://<hostname>:8081)

### Coordinator
- **Port** : `8081`
- **Description** : Gère les segments et la gestion des métadonnées.  
  Le Router redirige généralement vers ce service.

### Overlord
- **Port** : `8090`
- **Description** : Responsable de la soumission et de la gestion des tâches.

### Broker
- **Port** : `8082`
- **Description** : Traite les requêtes envoyées par les utilisateurs.

### Historical
- **Port** : `8083`
- **Description** : Fournit des données stockées sur disque.

### MiddleManager
- **Port** : `8091`
- **Description** : Gère l'ingestion de données et exécute des tâches.

### Zookeeper
- **Port** : `2181`
- **Description** : (Dépendance externe) Utilisé pour la coordination entre les différents services Druid.

## Notes