import React, { useEffect, useState } from 'react';
import axios from 'axios';

const DataFetcher = () => {
    const [data, setData] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            console.log("Fetch data");
            try {
                //const response = await fetch('http://<druid-server-url>/druid/v2/sql/', {
                //  method: 'POST',
                //  headers: {
                //    'Content-Type': 'application/json',
                //  },
                //  body: JSON.stringify({
                //    query: 'SELECT * FROM your_table LIMIT 10', // Remplacez par votre requête Druid
                //  }),
                //});

                const brokerUrl = 'http://localhost:8082/druid/v2/datasources';
                const response = await axios.get(brokerUrl)

                if (!response.ok) {
                    throw new Error('Erreur dans la réponse du serveur');
                }

                const result = await response.json();
                setData(result);
            } catch (error) {
                console.error('Erreur lors de la récupération des données :', error);
                setError(error);
            }
        };

        const intervalId = setInterval(fetchData, 10000); // Fetch data every 10 seconds

        return () => clearInterval(intervalId);
    }, []);

    return (
        <div>
            <h1>Données Apache Druid</h1>
            {error && <p style={{ color: 'red' }}>Erreur : {error.message}</p>}
            <ul>
                {data.map((item, index) => (
                    <li key={index}>{JSON.stringify(item)}</li>
                ))}
            </ul>
        </div>
    );
};

export default DataFetcher;