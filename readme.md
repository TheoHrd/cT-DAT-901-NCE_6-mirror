# Ports par défaut dans Apache Druid

Apache Druid utilise plusieurs services, chacun étant accessible via un port par défaut. Voici une liste des principaux services, leurs ports, et leurs rôles :

## Services et ports

### Postgres
- **Port** : `5432`

### Scrapper
- **Port** : `8000`
- **Description** : Scrapper python vers Google trends, Binance et flux rss.

### Dashboard
- **Port** : `3005`
- **Description** : Dashboard React des informations traitées par Druid.


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
- Les ports listés ici sont les ports par défaut et peuvent être configurés selon les besoins spécifiques de votre environnement.
- Assurez-vous que les ports nécessaires sont ouverts dans votre pare-feu pour permettre une communication correcte entre les services.

Pour plus de détails, consultez la [documentation officielle d'Apache Druid](https://druid.apache.org/).
