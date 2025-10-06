# Rapport TP1 - Question 1 : Application Web de Calcul d'IMC

**Réalisé par :** Arno BIDET & Antoine MAMOU  
**Date :** 6 octobre 2025  
**URL de l'application :** https://bidet-tp1-ex1-bidet-mamou.arno-bidet.dev/

## Résumé

Application web basique permettant le calcul de l'Indice de Masse Corporelle (IMC) avec stockage en base de données MySQL.

**Accès rapide :**
- **Application en ligne :** https://bidet-tp1-ex1-bidet-mamou.arno-bidet.dev/
- **Technologies :** HTML5, CSS3, JavaScript, Base de données
- **Hébergement :** Coolify + Cloudflare DNS

## Contexte et Objectifs

### Problématique
Développer une application web démonstrative illustrant l'architecture 3-tiers avec calcul d'IMC et persistance des données.

### Spécifications Techniques
- **Calcul IMC :** Formule `IMC = poids(kg) / taille(m)²`
- **Stockage :** Base de données pour historique des calculs

## Architecture de l'Application

### Stack Technologique

| Couche | Technologie | Rôle |
|--------|-------------|------|
| **Frontend** | HTML5/CSS3/JavaScript (statique) | Interface utilisateur |
| **Serveur Web** | Nginx | Serveur de fichiers statiques |
| **API Backend** | Node.js | API REST pour logique métier |
| **Base de données** | MySQL | Stockage des calculs IMC |
| **Hébergement** | Coolify | Déploiement et orchestration |
| **DNS** | Cloudflare | Gestion des domaines |

### Architecture Déployée
```
[Utilisateur] → [Cloudflare DNS] → [Nginx (site statique)]
                                            ↓ (AJAX/Fetch)
                                    [API Node.js] ← → [MySQL]
```

### Flux de Communication
1. **Client** : Site statique servi par Nginx
2. **API Calls** : JavaScript → API Node.js (endpoints REST)
3. **Persistance** : Node.js ← → MySQL (calculs et historique)
4. **Réponse** : JSON → Interface utilisateur

## Fonctionnalités

### 1. Calcul d'IMC
- **Entrées :** Poids (kg) et Taille (cm ou m)
- **Calcul :** IMC = poids / (taille²)
- **Interprétation :** Classification selon OMS

### 2. Interface Utilisateur (Site Statique)
- Formulaire HTML basique avec champs poids/taille
- Appels AJAX vers l'API Node.js
- Affichage des résultats et gestion d'erreurs simple
- Interface fonctionnelle

### 3. API REST Node.js
- **POST /imc** : Calcul IMC avec catégorisation OMS et sauvegarde
- **GET /imc** : Récupération historique complet des calculs
- Serveur HTTP natif (sans Express) avec pool de connexions MySQL2

### 4. Persistance MySQL
- Table des calculs IMC avec timestamp
- Historique des mesures par utilisateur

### Fonctionnalités Frontend Dynamiques

#### Remplacement d'URL Dynamique
Le frontend utilise un mécanisme intelligent de configuration:
```javascript
// Dans script.js - Placeholder remplacé au démarrage
fetch("__API_URL__/imc", { ... })

// Entrypoint Docker remplace automatiquement
sed -i "s|__API_URL__|${API_URL}|g" /usr/share/nginx/html/script.js
```

#### Interface Utilisateur Basique
- **Validation simple**: Vérification basique des valeurs numériques
- **Gestion d'erreurs**: Affichage des erreurs en texte rouge
- **Historique dynamique**: Bouton pour charger/afficher l'historique
- **CSS minimal**: Style basique fonctionnel

## Déploiement et Infrastructure

### Plateforme Coolify
- **Avantages :** Déploiement simplifié, gestion automatisée
- **Configuration :** Intégration continue via Git

### Cloudflare DNS
- **Domaine :** `arno-bidet.dev` avec sous-domaine dédié

## Déploiement sur Coolify

### Architecture Docker Multi-Services
- **Frontend**: Nginx statique
- **Backend**: Node.js avec pool de connexions MySQL
- **Base de données**: MySQL 8.0 avec initialisation automatique via `init.sql`
- **Réseau**: Communication inter-conteneurs avec dépendances définies

### DNS et Certificats
- **Domaine principal**: `bidet-tp1-ex1-bidet-mamou.arno-bidet.dev`
- **Proxy DNS**: Cloudflare avec protection DDoS
- **SSL/TLS**: Certificats Let's Encrypt automatiques via Coolify
- **Health checks**: Surveillance continue des services

## Guide d'Utilisation

### Accès à l'Application

### En tant que client
1. Ouvrir https://bidet-tp1-ex1-bidet-mamou.arno-bidet.dev/

### En tant que développeur
1. Remplir le fichier `.env`
2. `docker compose up`

## Conclusion

Cette application démontre une architecture 3-tiers basique avec :
- Frontend statique HTML/JS/CSS
- API REST Node.js vanilla 
- Base de données MySQL
- Déploiement Docker multi-conteneurs