{%- set cc = cookiecutter -%}
{%- set repo_ = (cc.repo | replace('-', '_')) -%}
{% if cc.include_prod_cli == "yes" -%}
import {{ repo_ }}.command  # noqa F401
{% endif -%}
import {{ repo_ }}.core  # noqa F401
{% if cc.repo_type in ["dash", "flask"] -%}
import {{ repo_ }}.server  # noqa F401
{% endif %}