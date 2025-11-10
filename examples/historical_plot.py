"""examples/historical_plot.py

Script d'exemple : récupère l'historique d'un ticker et trace le prix de clôture.
Usage:
    python examples/historical_plot.py IAM --start 2024-01-01 --end 2024-12-31

Le script essaie d'utiliser la colonne de fermeture la plus probable.
Sauvegarde un fichier PNG dans le répertoire courant.
"""

import argparse
import sys
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Récupère l'historique d'un ticker et trace un graphique de prix.")
    parser.add_argument('ticker', help='Ticker (ex: IAM, AFM)')
    parser.add_argument('--start', '-s', default='2024-01-01', help='Date de début YYYY-MM-DD')
    parser.add_argument('--end', '-e', default=None, help='Date de fin YYYY-MM-DD (par défaut aujourd\'hui)')
    parser.add_argument('--outfile', '-o', default=None, help='Fichier de sortie PNG (défaut: <TICKER>_history.png)')
    args = parser.parse_args()

    try:
        import casabourse as cb
        import pandas as pd
        import matplotlib.pyplot as plt
    except Exception as exc:
        print("Dépendances manquantes ou erreur d'import :", exc)
        print("Assurez-vous d'avoir installé casabourse (pip install -e .), pandas et matplotlib.")
        sys.exit(2)

    end = args.end or datetime.now().strftime("%Y-%m-%d")

    print(f"Récupération de l'historique pour {args.ticker} de {args.start} à {end} ...")
    try:
        df = cb.get_historical_data_auto(args.ticker, args.start, end)
    except Exception as exc:
        print("Erreur lors de l'appel à get_historical_data_auto:", exc)
        sys.exit(3)

    if df is None or getattr(df, 'empty', False):
        print("Aucune donnée historique retournée.")
        sys.exit(0)

    # Normaliser l'index en datetime si nécessaire
    try:
        if not pd.api.types.is_datetime64_any_dtype(df.index):
            # essaie de convertir une colonne 'date' en index si présente
            if 'date' in df.columns:
                df = df.set_index(pd.to_datetime(df['date']))
            else:
                try:
                    df.index = pd.to_datetime(df.index)
                except Exception:
                    pass
    except Exception:
        pass

    # Choisir une colonne de prix de clôture probable
    candidates = [c for c in df.columns if c.lower() in ('close', 'closing', 'clôture', 'cloture', 'prix_cloture', 'last', 'close_price')]
    if candidates:
        close_col = candidates[0]
    else:
        # fallback sur la première colonne numérique
        num_cols = df.select_dtypes(include='number').columns.tolist()
        close_col = num_cols[0] if num_cols else df.columns[0]

    print(f"Utilisation de la colonne '{close_col}' pour le tracé.")

    # Tracé
    plt.figure(figsize=(10, 4))
    try:
        plt.plot(df.index, df[close_col], marker='.', linestyle='-')
    except Exception as exc:
        print('Erreur lors du tracé:', exc)
        sys.exit(4)

    plt.title(f"{args.ticker} — {close_col} ({args.start} → {end})")
    plt.xlabel('Date')
    plt.ylabel(close_col)
    plt.grid(True)
    plt.tight_layout()

    outfile = args.outfile or f"{args.ticker}_history.png"
    plt.savefig(outfile)
    print('Graphique sauvegardé dans :', outfile)


if __name__ == '__main__':
    main()
