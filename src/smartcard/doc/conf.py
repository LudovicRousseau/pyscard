# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.viewcode",
]

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "pyscard"
copyright = "2014, Jean-Daniel Aussel, Ludovic Rousseau"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = "2.3.1"
# The full version, including alpha/beta/rc tags.
release = "2.3.1"

pygments_style = "sphinx"


# -- Options for HTML output ---------------------------------------------------

html_theme = "default"
