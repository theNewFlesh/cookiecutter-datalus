.. toctree::
   :maxdepth: 4

   core
{%- if cookiecutter.repo_type in ['dash', 'flask'] %}
   server
{%- endif %}
