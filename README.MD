# MatrixSec - Générateur de Wordlist Avancé

```
╔═══════════════════════════════════════════════════════════════════════════╗
║ ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗███████╗███████╗ ██████╗   ║
║ ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝██╔════╝██╔════╝██╔════╝   ║
║ ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝ ███████╗█████╗  ██║        ║
║ ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗ ╚════██║██╔══╝  ██║        ║
║ ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗███████║███████╗╚██████╗   ║
║ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝   ║
║                                                                           ║
║           [+] Sécurité Avancée - Décodage - Protection [+]                ║
║                         v1.0.0 | by ScriptSeinsei                         ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Description

MatrixSec est un outil avancé de génération de wordlists pour les professionnels de la sécurité informatique. Il permet de créer des listes de mots personnalisées en combinant divers éléments comme des mots, des dates, des caractères spéciaux, etc., pour tester la robustesse des systèmes d'authentification.

**AVERTISSEMENT:** Cet outil est destiné à un usage éthique uniquement. Utilisez-le exclusivement sur des systèmes pour lesquels vous disposez d'une autorisation explicite.

## Fonctionnalités

- Génération de combinaisons à partir d'une liste de mots source
- Ajout automatique de caractères spéciaux
- Intégration de dates (années, formats JJ/MM/AAAA)
- Variations de casse (minuscules, majuscules, capitalisées)
- Mode interactif ou non-interactif
- Contrôle du nombre maximum de combinaisons
- Filtrage automatique des mots trop courts (moins de 6 caractères)

## Installation

### Prérequis

- Python 3.6 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
git clone https://github.com/scriptseinsei/ultimate_wordlist_gen.git
cd ultimate_wordlist_gen
pip install tqdm
```

## Utilisation

### Mode interactif

```bash
python wordlist_gen.py --input mots-exemple.txt --output wordlist.txt
```

### Mode non-interactif

```bash
python wordlist_gen.py --input mots-exemple.txt --output wordlist.txt --no-interactive --max-combinations 500000 --min-length 2 --separator "-" --case-variants
```

### Options disponibles

| Option | Description |
|--------|-------------|
| `--input` | Fichier avec les mots (un par ligne) |
| `--output` | Fichier de sortie pour la wordlist |
| `--max-combinations` | Nombre maximum de combinaisons (défaut: 1000000) |
| `--min-length` | Longueur minimale des combinaisons (nombre d'éléments) |
| `--max-length` | Longueur maximale des combinaisons (nombre d'éléments) |
| `--separator` | Caractère entre les éléments (ex. "-", "_") |
| `--case-variants` | Ajouter des variations majuscules/minuscules |
| `--no-interactive` | Désactiver les questions interactives |

## Exemples de fichiers d'entrée

Créez un fichier texte (par exemple `mots.txt`) contenant des mots-clés pertinents, un par ligne:

```
admin
password
123456
utilisateur
entreprise
securite
```

## Fonctionnement

1. Le script charge les mots fournis dans le fichier d'entrée
2. En mode interactif, il pose des questions pour personnaliser la génération
3. Il génère toutes les combinaisons possibles selon les paramètres
4. Il filtre les résultats selon les critères définis (longueur minimale, etc.)
5. Il enregistre les résultats dans le fichier de sortie

## Structure du projet

```
MatrixSec/
├── wordlist_gen.py     # Script principal de génération
├── mots-exemple.txt    # Exemple de fichier d'entrée
├── README.md           # Documentation
└── config.json         # Configuration par défaut (optionnel)
```

## Licence

Ce logiciel est distribué sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Contributeurs

- ScriptSeinsei - Développeur principal

## Support

Pour toute question ou suggestion, veuillez ouvrir une issue sur le dépôt du projet.