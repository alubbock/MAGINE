# -*- coding: utf-8 -*-
#
# magine documentation build configuration file, created by
# sphinx-quickstart on Tue Apr 18 16:35:12 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

import os
import sys

import mock

sys.path.append(os.path.abspath('..'))

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.coverage',
              'sphinx.ext.imgmath', 'sphinx.ext.ifconfig', 'numpydoc',
              'sphinx.ext.viewcode', 'sphinx.ext.autosummary']

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'magine'
copyright = u'2017, James C. Pino'
author = u'James C. Pino'


# -- Mock out some problematic modules-------------------------------------

# Note that for sub-modules, all parent modules must be listed explicitly.
MOCK_MODULES = ['pandas', 'pandas.plotting',

                'scipy', 'scipy.cluster.hierarchy', 'scipy.cluster',
                'scipy.special', 'scipy.optimize', 'scipy.stats',
                'scipy.stats.stats', 'scipy.stats.stats.distributions',
                'scipy.sparse', 'scipy.linalg', 'seaborn',
                'seaborn.color_palette', 'seaborn.color_palette',

                # 'mpl_toolkits', 'mpl_toolkits.axes_grid1',
                # 'mpl_toolkits.axes_grid1.make_axes_locatable',

                'matplotlib', 'matplotlib.pyplot', 'matplotlib.image',
                'matplotlib.path', 'matplotlib.axes', 'matplotlib.ticker',
                'matplotlib.patches', 'matplotlib.colors', 'matplotlib.cbook',

                'numpy', 'numpy.testing', 'numpy.core', 'numpy.core.multiarray',
                'numpy.core.ma', 'numpy.linalg', 'numpy.ma',

                'statsmodels', 'statsmodels.sandbox',
                'statsmodels.sandbox.stats',
                'statsmodels.sandbox.stats.multicomp',
                'statsmodels.sandbox.stats.multicomp.fdrcorrection0',
                'statsmodels.stats', 'statsmodels.stats.proportion',
                'statsmodels.stats.proportion.binom_test',
                ]

for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.MagicMock()


# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u'0.1a1'
# The full version, including alpha/beta/rc tags.
release = u'0.1a1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'default'
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'maginedoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'magine.tex', u'magine Documentation',
     u'James C. Pino', 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'magine', u'magine Documentation',
     [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'magine', u'magine Documentation',
     author, 'magine', 'One line description of project.',
     'Miscellaneous'),
]

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# -- Options for numpydoc ------------------------------------------------------

numpydoc_show_class_members = False
