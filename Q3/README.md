# Rapport TP1 - Question 3 : Plateforme de Calcul Collaborative

**Réalisé par :** Arno BIDET & Antoine MAMOU  
**Date :** 6 octobre 2025

## Résumé

Implémentation de deux protocoles de communication distribués : **OBJECTColl** (RMI) et **BYTEColl** (Socket + bytecode dynamique).

**Installation :**
```bash
make compile
# OBJECTColl: make start-rmi + java Main server/client
# BYTEColl: java Main server/client
```

## Contexte

**Objectif :** Un client léger délègue des calculs à un serveur distant via deux protocoles :

| Protocole | Mécanisme | Port |
|-----------|-----------|------|
| **OBJECTColl** | RMI + objets sérialisés | 1099 |
| **BYTEColl** | Socket TCP + bytecode dynamique | 12345 |

## OBJECTColl (RMI)

**Fonctionnement :**
1. Serveur enregistre les objets dans le registre RMI 
2. Client récupère les références via `Naming.lookup()`
3. Appels de méthodes transparents

**Lancement :**
```bash
make start-rmi    # Registre RMI
java Main server  # Serveur
java Main client  # Client
```

## BYTEColl (Socket + Bytecode)

**Principe :** Transmet le bytecode compilé via socket TCP. Le serveur charge dynamiquement les classes.

**Flux :**
```
Client → Serveur
1. Nom opération (add/substract/multiply/divide)
2. Nom classe (Adder/Substractor/Multiplier/Divider)  
3. Bytecode (.class file)
4. Paramètres (int, int)
5. ← Résultat (int)
```

**Composants clés :**
```java
// ClassLoader dynamique
private static class ByteCodeClassLoader extends ClassLoader {
    protected Class<?> findClass(String name) {
        return defineClass(name, classData, 0, classData.length);
    }
}

// Chargement et exécution
Class<?> clazz = classLoader.loadClass("calculator." + className);
Object instance = clazz.getConstructor().newInstance();
Method method = clazz.getMethod("add", int.class, int.class);
Object result = method.invoke(instance, param1, param2);
```

**Lancement :**
```bash
java Main server  # Terminal 1 (port 12345)
java Main client  # Terminal 2
```

## Comparaison

| Critère | OBJECTColl | BYTEColl |
|---------|------------|----------|
| **Communication** | RMI (port 1099) | Socket TCP (port 12345) |
| **Flexibilité** | Couplage fort | Code à la demande |
| **Complexité** | Transparent | Gestion manuelle |

**Avantages BYTEColl :**
- Flexibilité maximale (exécution de code arbitraire)
- Performance optimisée 
- Isolation des exécutions

**Avantages OBJECTColl :**
- Transparence d'appel
- Gestion automatique des erreurs réseau

## Conclusion

**BYTEColl** préfigure les architectures serverless modernes où le code migre vers les ressources disponibles. Idéal pour systèmes IoT et calcul distribué à la demande.

**OBJECTColl** convient aux applications d'entreprise avec infrastructure stable.

## Annexes

### Structure du Projet
```
Q3/
├── OBJECTColl/         # RMI + registre
├── BYTEColl/           # Socket + ClassLoader dynamique
└── rapport.md
```

### Commandes Utiles
```bash
make clean && make compile
make start-rmi # RMI registry (OBJECTColl)
java Main server
java Main client
```
