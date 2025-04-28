#!/usr/bin/env python3
# Module d'analyse de mots de passe pour MatrixSec - By ScriptSeinsei

import sys
import re
import math
import argparse
import time
from pathlib import Path
from tqdm import tqdm

def print_banner():
    banner = """
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗███████╗███████╗ ██████╗   ║
# ║ ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝██╔════╝██╔════╝██╔════╝   ║
# ║ ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝ ███████╗█████╗  ██║        ║
# ║ ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗ ╚════██║██╔══╝  ██║        ║
# ║ ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗███████║███████╗╚██████╗   ║
# ║ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝   ║
# ║                                                                           ║
# ║           [+] Analyseur de Mots de Passe - MatrixSec [+]                  ║
# ║                         v1.0.0 | by ScriptSeinsei                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def calculate_entropy(password):
    """
    Calcule l'entropie d'un mot de passe.
    L'entropie est une mesure de la prévisibilité d'un mot de passe.
    Plus l'entropie est élevée, plus le mot de passe est difficile à deviner.
    """
    # Déterminer le pool de caractères
    pool_size = 0
    if re.search(r'[a-z]', password):
        pool_size += 26
    if re.search(r'[A-Z]', password):
        pool_size += 26
    if re.search(r'[0-9]', password):
        pool_size += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        pool_size += 33  # Caractères spéciaux communs

    # Si aucun caractère n'est trouvé (ce qui est impossible), assignons un petit pool
    if pool_size == 0:
        pool_size = 10

    # Calculer l'entropie
    entropy = math.log2(pool_size) * len(password)
    return entropy

def analyze_password_strength(password):
    """
    Analyse la force d'un mot de passe et retourne un score et des commentaires.
    """
    score = 0
    comments = []

    # Longueur
    if len(password) < 8:
        comments.append("Trop court")
    elif len(password) >= 12:
        score += 2
        comments.append("Bonne longueur")
    else:
        score += 1

    # Complexité
    if re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
        score += 1
    else:
        comments.append("Manque de variation de casse")

    if re.search(r'[0-9]', password):
        score += 1
    else:
        comments.append("Pas de chiffres")

    if re.search(r'[^a-zA-Z0-9]', password):
        score += 1
    else:
        comments.append("Pas de caractères spéciaux")

    # Motifs
    if re.search(r'(.)\1\1', password):  # Trois caractères identiques consécutifs
        score -= 1
        comments.append("Répétitions de caractères")

    if re.search(r'(123|abc|qwerty|password|admin)', password.lower()):
        score -= 1
        comments.append("Contient des séquences communes")

    # Entropie
    entropy = calculate_entropy(password)
    if entropy < 40:
        comments.append(f"Faible entropie ({entropy:.1f} bits)")
    elif entropy > 60:
        score += 1
        comments.append(f"Bonne entropie ({entropy:.1f} bits)")
    else:
        comments.append(f"Entropie moyenne ({entropy:.1f} bits)")

    # Classification finale
    strength = "Faible"
    if score >= 4:
        strength = "Fort"
    elif score >= 2:
        strength = "Moyen"

    return {
        "score": score,
        "strength": strength,
        "comments": comments,
        "entropy": entropy
    }

def analyze_wordlist(input_file, output_file=None, sample_size=None):
    """
    Analyse une wordlist complète et produit des statistiques.
    """
    print_banner()
    start_time = time.time()
    
    try:
        # Compter le nombre total de lignes pour la barre de progression
        total_lines = sum(1 for _ in open(input_file, 'r', encoding='utf-8'))
        
        # Limiter à l'échantillon si spécifié
        if sample_size and sample_size < total_lines:
            total_lines = sample_size
            print(f"Analyse sur un échantillon de {sample_size} mots de passe...")
        else:
            print(f"Analyse de tous les {total_lines} mots de passe...")
        
        # Initialiser les statistiques
        stats = {
            "total": 0,
            "weak": 0,
            "medium": 0,
            "strong": 0,
            "avg_length": 0,
            "avg_entropy": 0,
            "common_issues": {},
            "top_passwords": []
        }
        
        passwords_analyzed = 0
        
        with open(input_file, 'r', encoding='utf-8') as f:
            with tqdm(total=total_lines, desc="Analyse en cours", unit="mot de passe") as pbar:
                for line in f:
                    password = line.strip()
                    if not password:
                        continue
                    
                    # Analyser le mot de passe
                    analysis = analyze_password_strength(password)
                    
                    # Mettre à jour les statistiques
                    stats["total"] += 1
                    stats["avg_length"] += len(password)
                    stats["avg_entropy"] += analysis["entropy"]
                    
                    if analysis["strength"] == "Faible":
                        stats["weak"] += 1
                    elif analysis["strength"] == "Moyen":
                        stats["medium"] += 1
                    else:
                        stats["strong"] += 1
                    
                    # Compter les problèmes communs
                    for comment in analysis["comments"]:
                        if comment not in stats["common_issues"]:
                            stats["common_issues"][comment] = 0
                        stats["common_issues"][comment] += 1
                    
                    # Ajouter aux top passwords si le score est élevé
                    if analysis["score"] >= 4:
                        stats["top_passwords"].append((password, analysis["score"], analysis["entropy"]))
                        # Garder seulement les 10 meilleurs
                        stats["top_passwords"] = sorted(stats["top_passwords"], key=lambda x: (x[1], x[2]), reverse=True)[:10]
                    
                    pbar.update(1)
                    passwords_analyzed += 1
                    
                    # Arrêter si on a atteint la limite d'échantillonnage
                    if sample_size and passwords_analyzed >= sample_size:
                        break
        
        # Calculer les moyennes
        if stats["total"] > 0:
            stats["avg_length"] /= stats["total"]
            stats["avg_entropy"] /= stats["total"]
        
        # Calculer les pourcentages
        stats["weak_percent"] = (stats["weak"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        stats["medium_percent"] = (stats["medium"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        stats["strong_percent"] = (stats["strong"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        
        # Trier les problèmes communs
        stats["common_issues"] = sorted(stats["common_issues"].items(), key=lambda x: x[1], reverse=True)
        
        end_time = time.time()
        stats["analysis_time"] = end_time - start_time
        
        # Afficher les résultats
        print_results(stats)
        
        # Enregistrer les résultats dans un fichier
        if output_file:
            save_results(stats, output_file)
            print(f"\nRésultats enregistrés dans {output_file}")
        
    except Exception as e:
        print(f"Erreur lors de l'analyse : {e}")
        return

def print_results(stats):
    """Affiche les résultats de l'analyse."""
    print("\n" + "="*80)
    print(f"                       RAPPORT D'ANALYSE DE WORDLIST                       ")
    print("="*80)
    print(f"Nombre total de mots de passe analysés : {stats['total']}")
    print(f"Temps d'analyse : {stats['analysis_time']:.2f} secondes")
    print("-"*80)
    print("RÉPARTITION PAR FORCE :")
    print(f"  • Faible  : {stats['weak']} ({stats['weak_percent']:.1f}%)")
    print(f"  • Moyen   : {stats['medium']} ({stats['medium_percent']:.1f}%)")
    print(f"  • Fort    : {stats['strong']} ({stats['strong_percent']:.1f}%)")
    print("-"*80)
    print(f"Longueur moyenne : {stats['avg_length']:.1f} caractères")
    print(f"Entropie moyenne : {stats['avg_entropy']:.1f} bits")
    print("-"*80)
    print("PROBLÈMES FRÉQUENTS :")
    for issue, count in stats["common_issues"][:5]:  # Top 5 des problèmes
        print(f"  • {issue} : {count} occurrences ({(count/stats['total'])*100:.1f}%)")
    print("-"*80)
    if stats["top_passwords"]:
        print("MEILLEURS MOTS DE PASSE (score + entropie) :")
        for i, (password, score, entropy) in enumerate(stats["top_passwords"], 1):
            print(f"  {i}. {password} (Score: {score}, Entropie: {entropy:.1f} bits)")
    print("="*80)

def save_results(stats, output_file):
    """Enregistre les résultats dans un fichier."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("                       RAPPORT D'ANALYSE DE WORDLIST                       \n")
        f.write("="*80 + "\n")
        f.write(f"Nombre total de mots de passe analysés : {stats['total']}\n")
        f.write(f"Temps d'analyse : {stats['analysis_time']:.2f} secondes\n")
        f.write("-"*80 + "\n")
        f.write("RÉPARTITION PAR FORCE :\n")
        f.write(f"  • Faible  : {stats['weak']} ({stats['weak_percent']:.1f}%)\n")
        f.write(f"  • Moyen   : {stats['medium']} ({stats['medium_percent']:.1f}%)\n")
        f.write(f"  • Fort    : {stats['strong']} ({stats['strong_percent']:.1f}%)\n")
        f.write("-"*80 + "\n")
        f.write(f"Longueur moyenne : {stats['avg_length']:.1f} caractères\n")
        f.write(f"Entropie moyenne : {stats['avg_entropy']:.1f} bits\n")
        f.write("-"*80 + "\n")
        f.write("PROBLÈMES FRÉQUENTS :\n")
        for issue, count in stats["common_issues"]:
            f.write(f"  • {issue} : {count} occurrences ({(count/stats['total'])*100:.1f}%)\n")
        f.write("-"*80 + "\n")
        if stats["top_passwords"]:
            f.write("MEILLEURS MOTS DE PASSE (score + entropie) :\n")
            for i, (password, score, entropy) in enumerate(stats["top_passwords"], 1):
                f.write(f"  {i}. {password} (Score: {score}, Entropie: {entropy:.1f} bits)\n")
        f.write("="*80 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Analyseur de Wordlist - MatrixSec",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--input', type=str, required=True, help='Fichier wordlist à analyser')
    parser.add_argument('--output', type=str, help='Fichier de sortie pour le rapport (optionnel)')
    parser.add_argument('--sample', type=int, help='Nombre de mots de passe à analyser (échantillon)')

    args = parser.parse_args()

    if not Path(args.input).is_file():
        print(f"Erreur : le fichier {args.input} n'existe pas.")
        return

    analyze_wordlist(args.input, args.output, args.sample)

if __name__ == "__main__":
    main()