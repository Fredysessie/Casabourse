"""Script utilitaire pour construire la documentation (HTML + PDF si possible).

Usage:
    python scripts/build_docs.py [--html] [--pdf]

Le script produit les builds dans `docs/_build/html` et `docs/_build/latex`.
Pour produire le PDF, vous aurez besoin d'une distribution LaTeX (`pdflatex`) installée.
"""
import argparse
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOCS = os.path.join(ROOT, 'docs')
BUILD = os.path.join(DOCS, '_build')


def run(cmd, cwd=None):
    print('> ', ' '.join(cmd))
    p = subprocess.run(cmd, cwd=cwd or os.getcwd())
    if p.returncode != 0:
        raise SystemExit(p.returncode)


def build_html():
    run([sys.executable, '-m', 'sphinx', '-b', 'html', DOCS, os.path.join(BUILD, 'html')])
    print('HTML build: ', os.path.join(BUILD, 'html'))


def build_latex():
    run([sys.executable, '-m', 'sphinx', '-b', 'latex', DOCS, os.path.join(BUILD, 'latex')])
    latex_dir = os.path.join(BUILD, 'latex')
    tex_files = [f for f in os.listdir(latex_dir) if f.endswith('.tex')]
    if not tex_files:
        print('No .tex file found in', latex_dir)
        return
    main_tex = os.path.join(latex_dir, tex_files[0])
    # try pdflatex twice
    try:
        run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory', latex_dir, main_tex])
        run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory', latex_dir, main_tex])
        pdf_name = os.path.splitext(main_tex)[0] + '.pdf'
        print('PDF generated at:', pdf_name)
    except Exception as e:
        print('pdflatex not found or failed:', e)
        print('LaTeX files are available in', latex_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--html', action='store_true', help='Build HTML documentation')
    parser.add_argument('--pdf', action='store_true', help='Build PDF documentation (requires pdflatex)')
    args = parser.parse_args()

    if not args.html and not args.pdf:
        args.html = True
        args.pdf = True

    if args.html:
        build_html()
    if args.pdf:
        build_latex()


if __name__ == '__main__':
    main()
