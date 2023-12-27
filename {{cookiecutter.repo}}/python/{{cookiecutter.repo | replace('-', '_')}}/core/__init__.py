{%- set cc = cookiecutter -%}
{%- set repo_ = (cc.repo | replace('-', '_')) -%}
import {{ repo_ }}.core.tools  # noqa F401
