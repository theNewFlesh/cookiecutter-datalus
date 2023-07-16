<!-- <img id="logo" src="resources/logo.png" style="max-width: 717px"> -->

[![](https://img.shields.io/badge/License-MIT-F77E70?style=for-the-badge)](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.repo}}/blob/master/LICENSE)
[![](https://img.shields.io/pypi/pyversions/{{cookiecutter.repo}}?style=for-the-badge&label=Python&color=A0D17B&logo=python&logoColor=A0D17B)](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.repo}}/blob/master/docker/config/pyproject.toml)
[![](https://img.shields.io/pypi/v/{{cookiecutter.repo}}?style=for-the-badge&label=PyPI&color=5F95DE&logo=pypi&logoColor=5F95DE)](https://pypi.org/project/{{cookiecutter.repo}}/)
[![](https://img.shields.io/pypi/dm/{{cookiecutter.repo}}?style=for-the-badge&label=Downloads&color=5F95DE)](https://pepy.tech/project/{{cookiecutter.repo}})

# Introduction
{{cookiecutter.description}}

See [documentation](https://{{cookiecutter.github_user}}.github.io/{{cookiecutter.repo}}/) for details.

# Installation
### Python
`pip install {{cookiecutter.repo}}`

### Docker
1. Install [docker-desktop](https://docs.docker.com/desktop/)
2. `docker pull {{cookiecutter.github_user}}/{{cookiecutter.repo}}:[version]`

### Docker For Developers
1. Install [docker-desktop](https://docs.docker.com/desktop/)
2. Ensure docker-desktop has at least 4 GB of memory allocated to it.
3. `git clone git@github.com:{{cookiecutter.github_user}}/{{cookiecutter.repo}}.git`
4. `cd {{cookiecutter.repo}}`
6. `chmod +x bin/{{cookiecutter.repo}}`
7. `bin/{{cookiecutter.repo}} docker-start`

The service should take a few minutes to start up.

Run `bin/{{cookiecutter.repo}} --help` for more help on the command line tool.

---

# Production CLI

{{cookiecutter.repo}} comes with a command line interface defined in command.py.

Its usage pattern is: `{{cookiecutter.repo}} COMMAND [ARGS] [FLAGS] [-h --help]`

## Commands

---

### bash-completion
Prints BASH completion code to be written to a _{{cookiecutter.repo}} completion file

Usage: `{{cookiecutter.repo}} bash-completion`

---

### zsh-completion
Prints ZSH completion code to be written to a _{{cookiecutter.repo}} completion file

Usage: `{{cookiecutter.repo}} zsh-completion`

---

# Development CLI
bin/{{cookiecutter.repo}} is a command line interface (defined in cli.py) that works with
any version of python 2.7 and above, as it has no dependencies.

Its usage pattern is: `bin/{{cookiecutter.repo}} COMMAND [-a --args]=ARGS [-h --help] [--dryrun]`

### Commands

| Command              | Description                                                         |
| -------------------- | ------------------------------------------------------------------- |
| build-package        | Build production version of repo for publishing                     |
| build-prod           | Publish pip package of repo to PyPi                                 |
| build-publish        | Run production tests first then publish pip package of repo to PyPi |
| build-test           | Build test version of repo for prod testing                         |
| docker-build         | Build image of {{cookiecutter.repo}}                                              |
| docker-build-prod    | Build production image of {{cookiecutter.repo}}                                   |
| docker-container     | Display the Docker container id of {{cookiecutter.repo}}                          |
| docker-destroy       | Shutdown {{cookiecutter.repo}} container and destroy its image                    |
| docker-destroy-prod  | Shutdown {{cookiecutter.repo}} production container and destroy its image         |
| docker-image         | Display the Docker image id of {{cookiecutter.repo}}                              |
| docker-prod          | Start {{cookiecutter.repo}} production container                                  |
| docker-push          | Push {{cookiecutter.repo}} production image to Dockerhub                          |
| docker-remove        | Remove {{cookiecutter.repo}} Docker image                                         |
| docker-restart       | Restart {{cookiecutter.repo}} container                                           |
| docker-start         | Start {{cookiecutter.repo}} container                                             |
| docker-stop          | Stop {{cookiecutter.repo}} container                                              |
| docs                 | Generate sphinx documentation                                       |
| docs-architecture    | Generate architecture.svg diagram from all import statements        |
| docs-full            | Generate documentation, coverage report, diagram and code           |
| docs-metrics         | Generate code metrics report, plots and tables                      |
| library-add          | Add a given package to a given dependency group                     |
| library-graph-dev    | Graph dependencies in dev environment                               |
| library-graph-prod   | Graph dependencies in prod environment                              |
| library-install-dev  | Install all dependencies into dev environment                       |
| library-install-prod | Install all dependencies into prod environment                      |
| library-list-dev     | List packages in dev environment                                    |
| library-list-prod    | List packages in prod environment                                   |
| library-lock-dev     | Resolve dev.lock file                                               |
| library-lock-prod    | Resolve prod.lock file                                              |
| library-remove       | Remove a given package from a given dependency group                |
| library-search       | Search for pip packages                                             |
| library-sync-dev     | Sync dev environment with packages listed in dev.lock               |
| library-sync-prod    | Sync prod environment with packages listed in prod.lock             |
| library-update       | Update dev dependencies                                             |
| library-update-pdm   | Update PDM                                                          |
| session-app          | Run app                                                             |
| session-lab          | Run jupyter lab server                                              |
| session-python       | Run python session with dev dependencies                            |
| state                | State of {{cookiecutter.repo}}                                                    |
| test-coverage        | Generate test coverage report                                       |
| test-dev             | Run all tests                                                       |
| test-fast            | Test all code excepts tests marked with SKIP_SLOWS_TESTS decorator  |
| test-lint            | Run linting and type checking                                       |
| test-prod            | Run tests across all support python versions                        |
| version              | Full resolution of repo: dependencies, linting, tests, docs, etc    |
| version-bump-major   | Bump pyproject major version                                        |
| version-bump-minor   | Bump pyproject minor version                                        |
| version-bump-patch   | Bump pyproject patch version                                        |
| zsh                  | Run ZSH session inside {{cookiecutter.repo}} container                            |
| zsh-complete         | Generate oh-my-zsh completions                                      |
| zsh-root             | Run ZSH session as root inside {{cookiecutter.repo}} container                    |

### Flags

| Short | Long      | Description                                          |
| ----- | --------- | ---------------------------------------------------- |
| -a    | --args    | Additional arguments, this can generally be ignored  |
| -h    | --help    | Prints command help message to stdout                |
|       | --dryrun  | Prints command that would otherwise be run to stdout |
