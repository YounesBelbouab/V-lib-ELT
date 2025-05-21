# 🚲 Projet Data Pipeline Vélib' - GCP & DBT

Ce projet a pour but de récupérer les données des stations Vélib’ via l’API officielle, de les stocker sur Google Cloud Platform (GCP) puis de les transformer et modéliser via une pipeline DBT (Data Build Tool).

## 📌 Objectifs

- Collecter les données en temps réel sur les stations Vélib’ (disponibilité, état, etc.)
- Stocker ces données dans un data lake sur GCP (BigQuery ou Cloud Storage)
- Construire une pipeline de traitement et de modélisation des données avec DBT
- Préparer des données prêtes à l’analyse ou à la visualisation

## 🛠️ Stack technique

- **Langage :** Python  
- **Sources de données :** API Vélib’ Métropole  
- **Cloud :** Google Cloud Platform (GCP)  
  - Cloud Storage (optionnel)  
  - BigQuery  
- **Orchestration / Modélisation :** DBT (Data Build Tool)

## 🚀 Étapes du pipeline

1. **Récupération des données**  
   Script Python pour appeler l’API Vélib’ et collecter les données au format JSON.

2. **Envoi sur GCP**  
   Transformation et chargement des données vers BigQuery (ou via Cloud Storage).

3. **Transformation avec DBT**  
   Modèles DBT pour nettoyer, enrichir et structurer les données.

4. **Visualisation des données**  
   Création de dashboards via Looker Studio ou autre outil BI.

## ▶️ Exécution

1. **Installer les dépendances Python**  
   ```bash
   pip install -r requirements.txt

![alt text](images\relationel bdd.png)