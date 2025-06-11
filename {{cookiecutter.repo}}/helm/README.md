{%- set cc = cookiecutter -%}
# {{ cc.repo }} Helm Chart Structure
## Directory structure
```yaml
helm
  ├── Chart.yaml
  ├── values.yaml
  └── templates
     └── [template-name].yaml    # kebab-case
```

## values.yaml structure
```yaml
enable:
  [template]: [bool]

[template_name]:                 # snake_case
  [parameter]: [value]
```

## Note
`env-configmap.yaml` and `env-secret.yaml` values are interpreted by `_helpers.tpl`.
