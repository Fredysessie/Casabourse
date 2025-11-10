# Utilisation rapide

Extraits d'exemples d'utilisation de la bibliothèque Casabourse.

```python
import casabourse as cb

# récupère les données de marché en direct (DataFrame pandas)
df_live = cb.get_live_market_data()
print(df_live.head())

# recherche d'identifiant de symbole à partir d'un ticker
sid = cb.get_symbol_id_from_ticker_auto('AFM')
print('symbol id AFM:', sid)

# historique d'un ticker sur une période
hist = cb.get_historical_data_auto('IAM', '2024-01-01', '2024-12-31')
print(hist.head())
```

Pour tracer un historique et sauvegarder un PNG, utilisez `examples/historical_plot.py` (voir la racine `examples/`).
