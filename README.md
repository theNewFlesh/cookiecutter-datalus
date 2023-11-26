<p>
    <a href="https://www.linkedin.com/in/alexandergbraun" rel="nofollow noreferrer">
        <img src="https://www.gomezaparicio.com/wp-content/uploads/2012/03/linkedin-logo-1-150x150.png"
             alt="linkedin" width="30px" height="30px"
        >
    </a>
    <a href="https://github.com/theNewFlesh" rel="nofollow noreferrer">
        <img src="https://tadeuzagallo.com/GithubPulse/assets/img/app-icon-github.png"
             alt="github" width="30px" height="30px"
        >
    </a>
    <a href="https://pypi.org/user/the-new-flesh" rel="nofollow noreferrer">
        <img src="https://cdn.iconscout.com/icon/free/png-256/python-2-226051.png"
             alt="pypi" width="30px" height="30px"
        >
    </a>
    <a href="http://vimeo.com/user3965452" rel="nofollow noreferrer">
        <img src="https://cdn1.iconfinder.com/data/icons/somacro___dpi_social_media_icons_by_vervex-dfjq/500/vimeo.png"
             alt="vimeo" width="30px" height="30px"
        >
    </a>
    <a href="http://www.alexgbraun.com" rel="nofollow noreferrer">
        <img src="https://i.ibb.co/fvyMkpM/logo.png"
             alt="alexgbraun" width="30px" height="30px"
        >
    </a>
</p>

# Introduction
Cookiecutter-Datalus is a cookiecutter template for generating datalus
repositories.

# Usage
1. Install [cookiecutter](https://github.com/cookiecutter/cookiecutter) CLI
2. `cookiecutter https://github.com/theNewFlesh/cookiecutter-datalus`

# Purpose
Datalus is designed to facilitate the development of modern python applications.
It supports:
- Dash app development (ie Plotly + Flask + ReactJS) 
- Flask app development
- Kuberenetes app development via Helm and ArgoCD
- Python library development (multi version pip packages via pyproject and PDM)

# Features
Datalus repositories are extremely opionated, comprehensive and automated repos
for modern python development inside docker.

Datalus supports the following via a command line interface and VSCode tasks:
- multiple version support via PDM
  - separate python environments per version per mode (dev and prod)
- automated invocation of most PDM commands (sync, lock, add, etc)
- automated, parallel testing across all environments (pytest)
- automated linting across all environments (flake8)
- automated type checking across all environments (mypy)
- automated documentation generation (sphinx)
- automated dependency graph generation (rolling-pin)
- automated code coverage reports and metrics (rolling-pin)
- automated publishing to PyPI
  - including CLI for package (ie command.py)
- automated jupyter lab serving, pre-customized with color theme and plugins
- tensorflow installation
- openexr installation

# Developer Level Agreement
Functional division of labor between developer and devops requires a standard
contract across repositories. There are three essential parts to this contract:

  1. A consistent repository structure regarding directories, file names and
     configurations
  2. A consistent command line interface for running common developer tasks
  3. A consistent means of deploying applications to Kubernetes

# Design
Datalus solves this contract through comprehensive, standardized developer tools
and repository structure. The developer tools are accessed through the command
line and as VSCode tasks. Development is done against a dev docker container
defined in dev.dockerfile. Prod.dockerfile defines a slim production container
for running the repository code as an installed pip package.

# Development CLI
Datalus repos come with a development command line interface (defined in cli.py)
that works with any version of python 2.7 and above, as it has no dependencies.
Additionally, a subset of these commands are defined in the VSCode workspace
file. Appending `--dryrun` to any command will outputs the exact shell code that
would have been run without the flag.

Its usage pattern is: `bin/repo COMMAND [-a --args]=ARGS [-h --help] [--dryrun]`

### Commands

| Command              | Description                                                         | VSCode Task            |
| -------------------- | ------------------------------------------------------------------- | -----------------------|
| build-package        | Build production version of repo for publishing                     | [build] package        |
| build-prod           | Publish pip package of repo to PyPi                                 | [build] prod           |
| build-publish        | Run production tests first then publish pip package of repo to PyPi | [build] publish        |
| build-test           | Build test version of repo for prod testing                         | [build] test           |
| docker-build         | Build image of repo                                                 |                        |
| docker-build-prod    | Build production image of repo                                      |                        |
| docker-container     | Display the Docker container id of repo                             |                        |
| docker-destroy       | Shutdown repo container and destroy its image                       |                        |
| docker-destroy-prod  | Shutdown repo production container and destroy its image            |                        |
| docker-image         | Display the Docker image id of repo                                 |                        |
| docker-prod          | Start repo production container                                     |                        |
| docker-push          | Push repo production image to Dockerhub                             |                        |
| docker-remove        | Remove repo Docker image                                            |                        |
| docker-restart       | Restart repo container                                              |                        |
| docker-start         | Start repo container                                                |                        |
| docker-stop          | Stop repo container                                                 |                        |
| docs                 | Generate sphinx documentation                                       | [docs] docs            |
| docs-architecture    | Generate architecture.svg diagram from all import statements        | [docs] architecture    |
| docs-full            | Generate documentation, coverage report, diagram and code           | [docs] full            |
| docs-metrics         | Generate code metrics report, plots and tables                      | [docs] metrics         |
| library-add          | Add a given package to a given dependency group                     | [library] add          |
| library-graph-dev    | Graph dependencies in dev environment                               | [library] graph-dev    |
| library-graph-prod   | Graph dependencies in prod environment                              | [library] graph-prod   |
| library-install-dev  | Install all dependencies into dev environment                       | [library] install-dev  |
| library-install-prod | Install all dependencies into prod environment                      | [library] install-prod |
| library-list-dev     | List packages in dev environment                                    | [library] list-dev     |
| library-list-prod    | List packages in prod environment                                   | [library] list-prod    |
| library-lock-dev     | Resolve dev.lock file                                               | [library] lock-dev     |
| library-lock-prod    | Resolve prod.lock file                                              | [library] lock-prod    |
| library-remove       | Remove a given package from a given dependency group                | [library] remove       |
| library-search       | Search for pip packages                                             | [library] search       |
| library-sync-dev     | Sync dev environment with packages listed in dev.lock               | [library] sync-dev     |
| library-sync-prod    | Sync prod environment with packages listed in prod.lock             | [library] sync-prod    |
| library-update       | Update dev dependencies                                             | [library] update       |
| library-update-pdm   | Update PDM                                                          | [library] update-pdm   |
| quickstart           | Display quickstart guide                                            |
| session-app          | Run app                                                             | [session] app          |
| session-lab          | Run jupyter lab server                                              | [session] lab          |
| session-python       | Run python session with dev dependencies                            | [session] python       |
| state                | State of repo                                                       |                        |
| test-coverage        | Generate test coverage report                                       | [test] coverage        |
| test-dev             | Run all tests                                                       | [test] dev             |
| test-fast            | Test all code excepts tests marked with SKIP_SLOWS_TESTS decorator  | [test] fast            |
| test-lint            | Run linting and type checking                                       | [test] lint            |
| test-prod            | Run tests across all support python versions                        | [test] prod            |
| version              | Full resolution of repo: dependencies, linting, tests, docs, etc    | [version] version      |
| version-bump-major   | Bump pyproject major version                                        | [version] bump-major   |
| version-bump-minor   | Bump pyproject minor version                                        | [version] bump-minor   |
| version-bump-patch   | Bump pyproject patch version                                        | [version] bump-patch   |
| zsh                  | Run ZSH session inside repo container                               |                        |
| zsh-complete         | Generate oh-my-zsh completions                                      |                        |
| zsh-root             | Run ZSH session as root inside repo container                       |                        |

### Flags

| Short | Long      | Description                                          |
| ----- | --------- | ---------------------------------------------------- |
| -a    | --args    | Additional arguments, this can generally be ignored  |
| -h    | --help    | Prints command help message to stdout                |
| -     | --dryrun  | Prints command that would otherwise be run to stdout |


# Production CLI

Datalus repos come with a production command line interface defined in
command.py. pyproject.toml references this module for pip package installs.

Its usage pattern is: `repo COMMAND [FLAGS] [-h --help]`

### Commands
| Command         | Description                                                          | Flags | Flag Description |
| --------------- | ---------------------------------------------------------------------| ------| ---------------- |
| bash-completion | Prints BASH completion code to be written to a _repo completion file | -     | -                |
| zsh-completion  | Prints ZSH completion code to be written to a _repo completion file  | -     | -                |

---

# Repository Structure
The following is a comprehensive diagram of the Datalus repository structure:

```
APP
   ├── README.md                               <-- README with install instructions
   ├── .gitignore                              <-- git config
   ├── .gitattributes                          <-- git config
   ├── APP.code-workspace                      <-- VSCode config (contains task commands)
   ├── .devcontainer.json                      <-- VSCode remote container config
   ├── .env                                    <-- needed by VSCode docker-compose
   ├── bin
   |   └── APP                                 <-- shell wrapper for CLI
   |
   ├── docker                                  <-- everything needed to build and run container
   |   ├── dev.dockerfile                      <-- development version of app image
   |   ├── prod.dockerfile                     <-- production version of app image
   |   ├── docker-compose.yml                  <-- dev means of starting container
   │   ├── scripts
   │   |  └── x_tools.sh                       <-- developer tools
   │   ├── config
   │      ├── pyproject.toml                   <-- defines all dependencies
   │      ├── flake8.ini                       <-- linting config
   │      ├── dev-env                          <-- dev environment variables
   │      ├── pdm.toml                         <-- needed by PDM
   │      ├── dev.lock                         <-- frozen dev dependencies
   │      ├── prod.lock                        <-- frozen prod dependencies
   │      ├── build.yaml                       <-- defines pip package builds
   │      ├── zshrc                            <-- zsh environment setup
   │      ├── henanigans.zsh-theme             <-- zsh theme
   │      ├── jupyter
   │         ├── jupyter_lab_config.py         <-- jupyter lab config
   │         └── lab
   │            └── ...                        <-- jupyter lab plugins
   |
   ├── python
   |   ├── cli.py                              <-- dev command line interface
   |   ├── conftest.py                         <-- pytest config (optional)
   |   └── APP                                 <-- app source code
   │      ├── __init__.py
   │      ├── command.py                       <-- prod CLI module (optional)
   │      ├── core
   │      │   ├── __init__.py
   |      |   └── ...                          <-- core logic modules
   │      └── server                           <-- (optional)
   │         ├── __init__.py
   |         └── ...                           <-- server logic modules
   |
   ├── docs                                    <-- documentation build (/public if using gitlab)
   |   ├── index.html                          <-- docs homepage
   |   ├── architecture.svg                    <-- auto-generated graph of app dependecies
   |   ├── plots.html                          <-- code metric plots
   |   ├── all_metrics.html                    <-- master code metrics table
   |   ├── cyclomatic_complexity_metrics.html  <-- code metrics table
   |   ├── halstead_metrics.html               <-- code metrics table
   |   ├── htmlcov
   |   |   └── index.html                      <-- code coverage report
   |   └── resources
   |       └── ...                             <-- additional media for docs
   |
   ├── mkdocs                                  <-- markdown documentation config (optional)
   |   ├── md
   |   │  ├── index.md                         <-- markdown docs homepage
   |   │  ├── style.css                        <-- custom stylesheet
   |   |  └── ...                              <-- markdown files
   |   └── mkdocs.yml                          <-- mkdocs file index
   |
   ├── sphinx                                  <-- automatic documentation config
   |   ├── conf.py                             <-- sphinx config
   |   ├── make.bat                            <-- sphinx config
   |   ├── Makefile                            <-- sphinx config
   |   ├── cli.rst                             <-- cli docs
   |   ├── core.rst                            <-- core logic docs
   |   ├── index.rst                           <-- sphinx tox tree
   |   ├── modules.rst                         <-- sphinx toc tree
   |   ├── server.rst                          <-- server.py docs (optional)
   │   ├── intro.rst                           <-- README.md as rst
   │   ├── style.css                           <-- used by sphinx for styling docs
   |   └── images
   |      └── ...                              <-- images for docs
   |
   ├── helm                                    <-- Helm app definition (optional)
   |   ├── README.md                           <-- app README
   |   ├── Chart.yaml                          <-- Helm chart
   |   ├── values.yaml                         <-- default values
   |   ├── .helmignore                         <-- ignores files
   |   └── templates
   │       ├── _helpers.tpl                    <-- creates vars from values.yml
   │       ├── argocd-application.yaml         <-- ArgoCD app definition
   │       ├── deployment.yaml                 <-- k8s deployment
   │       ├── desktop-volume.yaml             <-- allows mounting of repo into pod
   │       ├── env-configmap.yaml              <-- env vars
   │       ├── env-secret.yaml                 <-- env secrets
   │       ├── image-pull-secret.yaml          <-- image pull secret (ie ECR creds, etc)
   │       ├── namespace.yaml                  <-- app namespace
   │       ├── nginx-ingress.yaml              <-- Nginx ingress (HarvesterOS)
   │       ├── repo-volume.yaml                <-- mount repo in volume
   │       ├── service.yaml                    <-- app service
   │       └── traefik-ingress.yaml            <-- Traefik ingress (RancherOS)
   |
   ├── notebooks
   |   └── ...                                 <-- jupyter lab notebooks
   ├── resources
   |   └── ...                                 <-- resources used by app
   ├── artifacts                               <-- (optional)
   |   └── ...                                 <-- dash artifacts
   └── templates                               <-- (optional)
       └── ...                                 <-- dash templates
```
