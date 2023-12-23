{%- set cc = cookiecutter -%}
{%- set repo_ = (cc.repo | replace('-', '_')) -%}
core
====

tools
-----
.. automodule:: {{ repo_ }}.core.tools
    :members:
    :private-members:
    :undoc-members:
    :show-inheritance:
