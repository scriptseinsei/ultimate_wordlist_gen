#!/usr/bin/env python3
# Script Wordlist Generator - By ScriptSeinsei

import itertools
import argparse
import os
import time
from tqdm import tqdm
from pathlib import Path
import re

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
# ║           [+] Sécurité Avancée - Décodage - Protection [+]                ║
# ║                         v1.0.0 | by ScriptSeinsei                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def collect_additional_inputs(args):
    """
    Demande à l'utilisateur s'il veut ajouter des caractères spéciaux, des dates, ou d'autres mots.
    À la fin, demande si l'utilisateur veut utiliser --no-interactive.
    :param args: Arguments de la ligne de commande pour construire la commande --no-interactive.
    :return: Tuple (special_chars, dates, extra_words)
    """
    special_chars = []
    dates = []
    extra_words = []

    # Caractères spéciaux
    print("\nVoulez-vous ajouter des caractères spéciaux (ex. !, @, #) ?")
    add_special = input("Tapez 'oui' ou 'non' [non] : ").lower().strip() or 'non'
    if add_special == 'oui':
        default_special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        print(f"Caractères par défaut : {default_special}")
        custom_special = input("Ajoutez vos propres caractères ou appuyez sur Entrée pour utiliser ceux par défaut : ").strip()
        special_chars = list(custom_special or default_special)

    # Dates
    print("\nVoulez-vous ajouter des dates (ex. années comme 2023, ou formats comme 01/01/2000) ?")
    add_dates = input("Tapez 'oui' ou 'non' [non] : ").lower().strip() or 'non'
    if add_dates == 'oui':
        print("Générer des années (ex. 1990, 2023) ?")
        start_year = input("Année de début [1900] : ").strip() or '1900'
        end_year = input("Année de fin [2025] : ").strip() or '2025'
        try:
            start_year = int(start_year)
            end_year = int(end_year)
            if start_year <= end_year:
                dates.extend(str(year) for year in range(start_year, end_year + 1))
            else:
                print("Erreur : l'année de début doit être inférieure ou égale à l'année de fin.")
        except ValueError:
            print("Erreur : veuillez entrer des années valides.")

        print("Générer des dates au format DD/MM/YYYY (ex. 01/01/2000) ?")
        add_full_dates = input("Tapez 'oui' ou 'non' [non] : ").lower().strip() or 'non'
        if add_full_dates == 'oui':
            for year in range(max(1900, start_year), min(end_year + 1, 2026)):
                for month in range(1, 13):
                    for day in range(1, 29):  # Limité à 28 pour simplifier
                        dates.append(f"{day:02d}/{month:02d}/{year}")

    # Autres mots
    print("\nVoulez-vous ajouter d'autres mots (ex. noms, numéros, 'admin', 'password') ?")
    add_extra = input("Tapez 'oui' ou 'non' [non] : ").lower().strip() or 'non'
    if add_extra == 'oui':
        print("Entrez les mots, un par ligne (tapez 'fin' pour terminer) :")
        while True:
            word = input().strip()
            if word.lower() == 'fin':
                break
            if word:
                extra_words.append(word)

    # Demande pour --no-interactive
    print("\nVoulez-vous générer la wordlist sans questions interactives la prochaine fois ?")
    use_no_interactive = input("Tapez 'oui' ou 'non' [non] : ").lower().strip() or 'non'
    if use_no_interactive == 'oui':
        command = f"python ultimate_wordlist_gen.py --input {args.input} --output {args.output} --no-interactive"
        if args.max_combinations != 1000000:
            command += f" --max-combinations {args.max_combinations}"
        if args.min_length != 1:
            command += f" --min-length {args.min_length}"
        if args.max_length:
            command += f" --max-length {args.max_length}"
        if args.separator:
            command += f" --separator \"{args.separator}\""
        if args.case_variants:
            command += " --case-variants"
        print(f"\nUtilisez cette commande pour éviter les questions :")
        print(f"{command}")

    return special_chars, dates, extra_words

def generate_wordlist(words, output_file, max_combinations=1000000, min_length=1, max_length=None, separator='', case_variants=False, special_chars=None, append_special=False):
    """
    Génère une wordlist en concaténant les mots, dates, et caractères spéciaux en un seul mot, avec un minimum de 6 caractères.
    """
    if not words and not special_chars:
        print("Erreur : aucune donnée à combiner.")
        return

    print_banner()
    start_time = time.time()

    max_length = max_length or len(words)
    max_length = min(max_length, len(words))

    total_generated = 0
    buffer = []
    buffer_size = 1000
    min_char_length = 6  # Longueur minimale des combinaisons

    try:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for i in range(min_length, max_length + 1):
                total_combinations = sum(1 for _ in itertools.combinations(words, i))
                with tqdm(total=total_combinations, desc=f"Création de {i} éléments", unit="combinaison") as pbar:
                    for combo in itertools.combinations(words, i):
                        if total_generated >= max_combinations:
                            print(f"\nLimite de {max_combinations} combinaisons atteinte.")
                            return
                        # Concaténer les éléments en un seul mot
                        combination = separator.join(combo) if separator else ''.join(combo)
                        variations = [combination.lower(), combination.capitalize(), combination.upper()] if case_variants else [combination]

                        # Ajouter des caractères spéciaux si demandé
                        final_variations = []
                        if special_chars and append_special:
                            for var in variations:
                                for char in special_chars:
                                    final_variations.extend([var + char, char + var])
                            final_variations.extend(variations)  # Inclure la version sans caractère spécial
                        else:
                            final_variations = variations

                        # Filtrer les combinaisons de moins de 6 caractères
                        for var in final_variations:
                            if len(var) >= min_char_length:
                                buffer.append(var + '\n')
                                total_generated += 1
                                if len(buffer) >= buffer_size:
                                    f_out.writelines(buffer)
                                    buffer.clear()
                        pbar.update(1)
            if buffer:
                f_out.writelines(buffer)
    except PermissionError:
        print(f"Erreur : impossible d'écrire dans {output_file}. Vérifie les permissions.")
        return
    except Exception as e:
        print(f"Erreur : {e}")
        return

    end_time = time.time()
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # Taille en Mo
    print(f"\nWordlist créée avec succès !")
    print(f"Total : {total_generated} combinaisons (au moins {min_char_length} caractères)")
    print(f"Fichier : {output_file} ({file_size:.2f} Mo)")
    print(f"Temps : {end_time - start_time:.2f} secondes")

def load_words_from_file(file_path):
    """
    Charge les mots à partir d'un fichier texte.
    """
    file_path = Path(file_path)
    if not file_path.is_file():
        print(f"Erreur : le fichier {file_path} n'existe pas.")
        return []
    try:
        with file_path.open('r', encoding='utf-8') as f:
            words = {line.strip() for line in f if line.strip()}
        return list(words)
    except UnicodeDecodeError:
        print(f"Erreur : problème avec l'encodage du fichier {file_path}.")
        return []
    except Exception as e:
        print(f"Erreur : {e}")
        return []

def main():
    parser = argparse.ArgumentParser(
        description="Script Wordlist Generator - By ScriptSeinsei",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--input', type=str, required=True, help='Fichier avec les mots (un par ligne)')
    parser.add_argument('--output', type=str, required=True, help='Fichier de sortie pour la wordlist')
    parser.add_argument('--max-combinations', type=int, default=1000000, help='Nombre maximum de combinaisons')
    parser.add_argument('--min-length', type=int, default=1, help='Longueur minimale des combinaisons (nombre d\'éléments)')
    parser.add_argument('--max-length', type=int, help='Longueur maximale des combinaisons (nombre d\'éléments)')
    parser.add_argument('--separator', type=str, default='', help='Caractère entre les éléments (ex. "-", "_"; vide par défaut)')
    parser.add_argument('--case-variants', action='store_true', help='Ajouter des variations majuscules/minuscules')
    parser.add_argument('--no-interactive', action='store_true', help='Désactiver les questions interactives')

    args = parser.parse_args()

    output_dir = os.path.dirname(args.output) or '.'
    if not os.access(output_dir, os.W_OK):
        print(f"Erreur : impossible d'écrire dans {output_dir}.")
        return

    # Charger les mots du fichier
    words = load_words_from_file(args.input)

    # Collecter des entrées supplémentaires (caractères spéciaux, dates, mots)
    special_chars = []
    if not args.no_interactive:
        special_chars, dates, extra_words = collect_additional_inputs(args)
        words.extend(dates)
        words.extend(extra_words)
        words.extend(special_chars)  # Les caractères spéciaux sont aussi des "mots" combinables
    else:
        special_chars = ['!', '@', '#', '$', '%']  # Par défaut si non interactif

    if words or special_chars:
        generate_wordlist(
            words,
            args.output,
            args.max_combinations,
            args.min_length,
            args.max_length,
            args.separator,
            args.case_variants,
            special_chars,
            append_special=bool(special_chars)  # Ajouter les caractères spéciaux au début/fin
        )

if __name__ == "__main__":
    main()