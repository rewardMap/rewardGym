# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys
import os
import re
import pathlib

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
sys.path.insert(0, os.path.abspath(os.path.pardir))

# Import your package and read the version Versioneer computed
import rewardgym  # replace with your top-level package name

# Sphinx's full version string (e.g. "1.2.3.dev0+gHASH")
release = rewardgym.__version__

# Sphinx's short X.Y version for the UI (strip pre/dev/build metadata)
# Keep it simple: first two numeric components
m = re.match(r"(\d+\.\d+)", release)
version = m.group(1) if m else release

project = "rewardGym"
copyright = "2024, Simon R. Steinkamp"
author = "Simon R. Steinkamp"

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
    "myst_parser",
    "sphinx_copybutton",
    "sphinxcontrib.relativeinclude",
]

autosummary_generate = True
numpydoc_show_class_members = True
autoclass_content = "class"

autodoc_mock_imports = ["psychopy"]

# The suffix(es) of source filenames.
sourcesuffix = {".rst": "restructuredtext", ".md": "markdown"}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
bibtex_bibfiles = ["references.bib"]
bibtex_reference_style = "author_year"


myst_enable_extensions = [
    "colon_fence",  # ::: and ```{directive} fences
    "substitution",  # if you want substitutions
    "deflist",
    "linkify",
    "attrs_inline",
    "html_image",
]

code_to_convert = ["tutorial.py"]
for ii in code_to_convert:
    file = os.path.join("../notebooks", ii)
    os.popen(f"jupytext {file} --to ipynb")
# Make nbsphinx detect jupytext files

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = []
plot_html_show_source_link = True
plot_include_source = True

# Make tasks readme.rst - toc?
curr_file = pathlib.Path(__file__).parent
task_path = pathlib.Path("../rewardgym/tasks/")
task_glob = list(task_path.glob("*/README*"))
task_glob = sorted(task_glob)

for i in task_glob:
    string_template = i.parent.name + "\n===================\n\n"
    string_template += (
        ".. relativeinclude:: "
        + "../"
        + i.absolute().relative_to(curr_file).as_posix()
        + "\n"
    )

    if i.suffix == ".md":
        string_template += "  :parser: myst_parser.sphinx_"

    (curr_file / "tasks" / f"{i.parent.name}.rst").write_text(string_template)
