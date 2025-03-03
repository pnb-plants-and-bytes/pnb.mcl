# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import pnb.mcl

project = 'pnb.mcl'
copyright = '2025, pnb plants & bytes GmbH'
author = 'pnb plants & bytes'
version = '0.1'
release = version

html_title = f'{project} {version}'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_execute_code_pnb']

todo_include_todos = False

templates_path = ['_templates']
exclude_patterns = []

autodoc_default_options = {
    'members': 'var1, var2',
    'member-order': 'alphabetical',
    'special-members': '''
        __contains__,
        __get__,
        __getattr__,
        __iter__,
        __len__,
        __repr__''',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}


html_copy_source = False

html_theme = 'furo'
html_logo = 'pnb.png'
html_static_path = ['_static']

rst_prolog = f'''
.. |version| replace:: {version}
'''
