{%- set cc = cookiecutter -%}
import {{ cc.repo }}.command  # noqa F401
import {{ cc.repo }}.core  # noqa F401
{%- if cc.repo_type in ["dash", "flask"] %}
import {{ cc.repo }}.server  # noqa F401
{%- endif %}
