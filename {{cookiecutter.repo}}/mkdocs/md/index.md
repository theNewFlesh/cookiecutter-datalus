{%- set cc = cookiecutter -%}
{%- if cc.git_host == 'bitbucket' %}
{%- set url = "butbucket.org" %}
{%- elif cc.git_host == 'gitlab' %}
{%- set url = "gitlab.com" %}
{%- else %}
{%- set url = "github.com" %}
{%- endif  -%}
<!-- <img id="logo" src="resources/logo.png" style="max-width: 717px"> -->

[![](https://img.shields.io/badge/License-MIT-F77E70?style=for-the-badge)](https://{{url}}/{{cc.git_user}}/{{cc.repo}}/blob/master/LICENSE)
[![](https://img.shields.io/pypi/pyversions/{{cc.repo}}?style=for-the-badge&label=Python&color=A0D17B&logo=python&logoColor=A0D17B)](https://{{url}}/{{cc.git_user}}/{{cc.repo}}/blob/master/docker/config/pyproject.toml)
[![](https://img.shields.io/pypi/v/{{cc.repo}}?style=for-the-badge&label=PyPI&color=5F95DE&logo=pypi&logoColor=5F95DE)](https://pypi.org/project/{{cc.repo}}/)
[![](https://img.shields.io/pypi/dm/{{cc.repo}}?style=for-the-badge&label=Downloads&color=5F95DE)](https://pepy.tech/project/{{cc.repo}})

# Introduction
{{cc.description}}

See [documentation](https://{{cc.git_user}}.{{cc.git_host}}.io/{{cc.repo}}/) for details.
