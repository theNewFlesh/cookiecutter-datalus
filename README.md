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
- automated jupyter lab serving
- dash app development
- flask app development
- tensorflow installation
- openexr installation

# Usage
1. Install [cookiecutter](https://github.com/cookiecutter/cookiecutter) CLI
2. `cookiecutter https://github.com/theNewFlesh/cookiecutter-datalus`

# Development CLI
Datalus repos come with a development command line interface (defined in cli.py)
that works with any version of python 2.7 and above, as it has no dependencies.
Additionally, a subset of these commands are defined in the VSCode workspace
file.

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
| docker-coverage      | Generate coverage report for repo                                   |                        |
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
command.py. Pyproject.toml references this module for pip package installs.

Its usage pattern is: `repo COMMAND [FLAGS] [-h --help]`

### Commands
| Command         | Description                                                          | Flags | Flag Description |
| --------------- | ---------------------------------------------------------------------| ------| ---------------- |
| bash-completion | Prints BASH completion code to be written to a _repo completion file | -     | -                |
| zsh-completion  | Prints ZSH completion code to be written to a _repo completion file  | -     | -                |