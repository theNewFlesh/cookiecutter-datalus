.. toctree::
   :maxdepth: 4

   cli
{%- if cookiecutter.repo_type in ['dash', 'flask'] %}
   server
{%- endif %}
