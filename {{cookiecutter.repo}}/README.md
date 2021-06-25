# Introduction
{{cookiecutter.description}}

See [documentation](https://{{cookiecutter.github_user}}.github.io/{{cookiecutter.repo}}/) for details.

# Installation
### Python
`pip install {{cookiecutter.repo}}`

### Docker
1. Install
   [docker](https://docs.docker.com/v17.09/engine/installation)
2. Install
   [docker-machine](https://docs.docker.com/machine/install-machine)
   (if running on macOS or Windows)
3. `docker pull {{cookiecutter.github_user}}/{{cookiecutter.repo}}:[version]`
4. `docker run --rm --name {{cookiecutter.repo}}-prod --publish {{cookiecutter.port_prefix}}80:80 {{cookiecutter.github_user}}/{{cookiecutter.repo}}:[version]`

### Docker For Developers
1. Install
   [docker](https://docs.docker.com/v17.09/engine/installation)
2. Install
   [docker-machine](https://docs.docker.com/machine/install-machine)
   (if running on macOS or Windows)
3. Ensure docker-machine has at least 4 GB of memory allocated to it.
4. `git clone git@github.com:{{cookiecutter.github_user}}/{{cookiecutter.repo}}.git`
5. `cd {{cookiecutter.repo}}`
6. `chmod +x bin/{{cookiecutter.repo}}`
7. `bin/{{cookiecutter.repo}} start`

The service should take a few minutes to start up.

Run `bin/{{cookiecutter.repo}} --help` for more help on the command line tool.
