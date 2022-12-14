# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from __future__ import division, print_function, unicode_literals
from datetime import datetime
#import sphinx_theme

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    ]

project = 'Cluster Cin'
copyright = str(datetime.now().year)
version = 'latest'
release = 'latest'
htmlhelp_basename = 'apuana-docs'

templates_path = ['templates', '_templates', '.templates']
source_suffix = ['.rst', '.md']
master_doc = 'index'
exclude_patterns = []
pygments_style = 'sphinx'
language = 'pt_BR'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'groundwork'
html_theme_path = ["."]
html_static_path = ['_static']

#html_theme_path = [sphinx_theme.get_html_theme_path()]
html_logo = '/home/mordor/Ambiente-Python/Cluster-Doc/docs/build/html/_static/cin-logo.png'