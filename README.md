# nicehash-monitor
NiceHash Mining Monitor with e-Paper Display

## Description
Un système de monitoring pour NiceHash qui affiche les statistiques de minage en temps réel sur un écran e-paper. Le projet collecte les données de l'API NiceHash et affiche les informations essentielles comme le hashrate, le nombre de rigs actifs et les soldes de portefeuille.

## Fonctionnalités
- Affichage du nombre de rigs actifs et total
- Affichage du hashrate total avec l'algorithme utilisé (VRSC)
- Affichage du solde BTC
- Conversion en temps réel du solde BTC en EUR (via CoinGecko API)
- Mise à jour automatique des données
- Compatible avec les écrans e-paper Waveshare

## Structure du Projet
```
nicehash/
├── api_client.py        # Gestion des appels API NiceHash
├── config.py           # Configuration et variables d'environnement
├── data_formatter.py   # Formatage des données
├── display_manager.py  # Gestion de l'affichage e-paper
└── main.py            # Point d'entrée principal
```

## Technologies Utilisées
- Python 3.x
- API NiceHash
- API CoinGecko (pour les taux de change)
- Bibliothèque Waveshare e-Paper
- Pillow (PIL) pour le traitement d'images

## Dépendances
```bash
pip install requests pillow python-dotenv waveshare-epaper
```

## Configuration
1. Créer un fichier `.env` avec vos identifiants NiceHash :
```env
NICEHASH_API_KEY=votre_api_key
NICEHASH_API_SECRET=votre_api_secret
NICEHASH_ORG_ID=votre_org_id
```

## Format d'Affichage
- Timestamp
- Active Rigs: X (total Y)
- Total Hashrate: XX.XX MH/s VRSC
- BTC: X.XXXXXXXX
- EUR: XX.XX €

## APIs Utilisées
- NiceHash API v2 pour les données de minage
- CoinGecko API pour les taux de change BTC/EUR

## Matériel Requis
- Raspberry Pi (ou similaire)
- Écran e-Paper Waveshare
- Connexion Internet

## Notes
- L'affichage est optimisé pour les écrans e-paper
- Les taux de change sont mis à jour en temps réel
- La mise à jour des données se fait toutes les X minutes

## Améliorations Possibles
- Mise en cache du taux de change
- Support pour d'autres algorithmes de minage
- Interface de configuration web
- Graphiques de performance
- Support pour d'autres exchanges

