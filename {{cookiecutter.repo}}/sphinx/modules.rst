{%- set cc = cookiecutter -%}
.. toctree::
   :maxdepth: 4

   core
{%- if cc.repo_type in ['dash', 'flask'] %}
   server
{%- endif %}
