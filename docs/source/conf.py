import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

project = 'Pyr4t'
copyright = '2026, R4tL'
author = 'R4tL'
release = '1.1.0'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'furo'
html_static_path = ['_static']

html_logo = "_static/logo-light.png"

html_js_files = [
    "logo-switch.js",
]
