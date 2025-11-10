# Configuration Sphinx pour la documentation de Casabourse
import os
import sys
from datetime import datetime

# ajouter le chemin du package (racine du dépôt)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

try:
    from casabourse import __version__ as _ver
    release = getattr(_ver, '__version__', str(_ver)) if hasattr(_ver, '__version__') else str(_ver)
except Exception:
    release = '0.0'

project = 'Casabourse'
author = 'Koffi Frederic SESSIE <sessiekoffifrederic@gmail.com>'

# metadata for templates
html_context = {
    'owner_name': 'Koffi Frederic SESSIE',
    'owner_email': 'sessiekoffifrederic@gmail.com',
}

# -- General configuration ------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'myst_parser',
]

autosummary_generate = True
autodoc_typehints = 'description'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output ----------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# myst-parser configuration (supporter Markdown source files)
myst_enable_extensions = [
    'deflist',
    'colon_fence',
]

# Date for the documentation
today = datetime.now().strftime('%Y-%m-%d')

# If API imports are heavy, you can mock them by adding their names here.
autodoc_mock_imports = []
