# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys
import os

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
sys.path.insert(0, os.path.abspath(os.path.pardir))
import rewardgym

project = "rewardGym"
copyright = "2024, Simon R. Steinkamp"
author = "Simon R. Steinkamp"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "matplotlib.sphinxext.plot_directive",
    "sphinxcontrib.bibtex",
    "nbsphinx",
    "nbsphinx_link",
]

autosummary_generate = True
numpydoc_show_class_members = True
autoclass_content = "class"

autodoc_mock_imports = ["psychopy"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
bibtex_bibfiles = ["references.bib"]
bibtex_reference_style = "author_year"

import glob
import jupytext

code_to_convert = ["tutorial.py"]
for ii in code_to_convert:
    file = os.path.join("../notebooks", ii)
    os.popen(f"jupytext {file} --to ipynb")
# Make nbsphinx detect jupytext files

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
