# Casabourse

Bienvenue dans la documentation de la bibliothèque Casabourse.

Cette documentation expose :

- Une introduction et des exemples d'utilisation (HTML/Markdown).
- La documentation API générée depuis les docstrings du package `casabourse`.

## Résumé rapide

Installez en mode développement puis consultez la doc :

```powershell
pip install -e .
pip install -r docs/requirements-docs.txt
```

Pour générer la documentation HTML et (si disponible) le PDF, voir `scripts/build_docs.py` ou lancer :

```powershell
python .\scripts\build_docs.py
```

## Contenu

- `Usage` — exemples et commandes rapides.
- `API` — modules et fonctions exportés (générés automatiquement si vous lancez `sphinx-apidoc`/`sphinx-build`).

Voir les pages ci-dessous pour plus de détails.

---

Owner / Contact
----------------

Documentation maintenue par : **Koffi Frederic SESSIE** — sessiekoffifrederic@gmail.com

Pages importantes
-----------------

- `Usage` — exemples d'utilisation
- `API` — documentation des modules et fonctions exportées (voir `api`)

```{eval-rst}
.. toctree::
	:maxdepth: 2

	usage
	api
```
