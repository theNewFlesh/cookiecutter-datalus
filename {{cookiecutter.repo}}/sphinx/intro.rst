.. raw:: html

   <p>

.. raw:: html

   </p>

Introduction
============

A library of computer vision models and a streamlined framework for
training them.

See `documentation <https://thenewflesh.github.io/{{cookiecutter.repo}}/>`__ for
details.

Installation
============

Python
~~~~~~

``pip install {{cookiecutter.repo}}``

Docker
~~~~~~

1. Install `docker-desktop <https://docs.docker.com/desktop/>`__
2. ``docker pull {{cookiecutter.github_user}}/{{cookiecutter.repo}}:[version]``

Docker For Developers
~~~~~~~~~~~~~~~~~~~~~

1. Install `docker-desktop <https://docs.docker.com/desktop/>`__
2. Ensure docker-desktop has at least 4 GB of memory allocated to it.
3. ``git clone git@github.com:{{cookiecutter.github_user}}/{{cookiecutter.repo}}.git``
4. ``cd {{cookiecutter.repo}}``
5. ``chmod +x bin/{{cookiecutter.repo}}``
6. ``bin/{{cookiecutter.repo}} start``

The service should take a few minutes to start up.

Run ``bin/{{cookiecutter.repo}} --help`` for more help on the command line tool.

--------------

Production CLI
==============

{{cookiecutter.repo}} comes with a command line interface defined in command.py.

Its usage pattern is: ``{{cookiecutter.repo}} COMMAND [ARGS] [FLAGS] [-h --help]``

Commands
--------

--------------

bash-completion
~~~~~~~~~~~~~~~

Prints BASH completion code to be written to a \_{{cookiecutter.repo}} completion
file

Usage: ``{{cookiecutter.repo}} bash-completion``

--------------

zsh-completion
~~~~~~~~~~~~~~

Prints ZSH completion code to be written to a \_{{cookiecutter.repo}} completion file

Usage: ``{{cookiecutter.repo}} zsh-completion``

--------------

Development CLI
===============

bin/{{cookiecutter.repo}} is a command line interface (defined in cli.py) that works
with any version of python 2.7 and above, as it has no dependencies.

Its usage pattern is:
``bin/{{cookiecutter.repo}} COMMAND [-a --args]=ARGS [-h --help] [--dryrun]``

.. _commands-1:

Commands
~~~~~~~~

+---------------+------------------------------------------------------+
| Command       | Description                                          |
+===============+======================================================+
| build-package | Build production version of repo for publishing      |
+---------------+------------------------------------------------------+
| build-prod    | Publish pip package of repo to PyPi                  |
+---------------+------------------------------------------------------+
| build-publish | Run production tests first then publish pip package  |
|               | of repo to PyPi                                      |
+---------------+------------------------------------------------------+
| build-test    | Build test version of repo for prod testing          |
+---------------+------------------------------------------------------+
| docker-build  | Build image of {{cookiecutter.repo}}                              |
+---------------+------------------------------------------------------+
| docker-build- | Build production image of {{cookiecutter.repo}}                   |
| prod          |                                                      |
+---------------+------------------------------------------------------+
| docker-contai | Display the Docker container id of {{cookiecutter.repo}}          |
| ner           |                                                      |
+---------------+------------------------------------------------------+
| docker-covera | Generate coverage report for {{cookiecutter.repo}}                |
| ge            |                                                      |
+---------------+------------------------------------------------------+
| docker-destro | Shutdown {{cookiecutter.repo}} container and destroy its image    |
| y             |                                                      |
+---------------+------------------------------------------------------+
| docker-destro | Shutdown {{cookiecutter.repo}} production container and destroy   |
| y-prod        | its image                                            |
+---------------+------------------------------------------------------+
| docker-image  | Display the Docker image id of {{cookiecutter.repo}}              |
+---------------+------------------------------------------------------+
| docker-prod   | Start {{cookiecutter.repo}} production container                  |
+---------------+------------------------------------------------------+
| docker-push   | Push {{cookiecutter.repo}} production image to Dockerhub          |
+---------------+------------------------------------------------------+
| docker-remove | Remove {{cookiecutter.repo}} Docker image                         |
+---------------+------------------------------------------------------+
| docker-restar | Restart {{cookiecutter.repo}} container                           |
| t             |                                                      |
+---------------+------------------------------------------------------+
| docker-start  | Start {{cookiecutter.repo}} container                             |
+---------------+------------------------------------------------------+
| docker-stop   | Stop {{cookiecutter.repo}} container                              |
+---------------+------------------------------------------------------+
| docs          | Generate sphinx documentation                        |
+---------------+------------------------------------------------------+
| docs-architec | Generate architecture.svg diagram from all import    |
| ture          | statements                                           |
+---------------+------------------------------------------------------+
| docs-full     | Generate documentation, coverage report, diagram and |
|               | code                                                 |
+---------------+------------------------------------------------------+
| docs-metrics  | Generate code metrics report, plots and tables       |
+---------------+------------------------------------------------------+
| library-add   | Add a given package to a given dependency group      |
+---------------+------------------------------------------------------+
| library-graph | Graph dependencies in dev environment                |
| -dev          |                                                      |
+---------------+------------------------------------------------------+
| library-graph | Graph dependencies in prod environment               |
| -prod         |                                                      |
+---------------+------------------------------------------------------+
| library-insta | Install all dependencies into dev environment        |
| ll-dev        |                                                      |
+---------------+------------------------------------------------------+
| library-insta | Install all dependencies into prod environment       |
| ll-prod       |                                                      |
+---------------+------------------------------------------------------+
| library-list- | List packages in dev environment                     |
| dev           |                                                      |
+---------------+------------------------------------------------------+
| library-list- | List packages in prod environment                    |
| prod          |                                                      |
+---------------+------------------------------------------------------+
| library-lock- | Resolve dev.lock file                                |
| dev           |                                                      |
+---------------+------------------------------------------------------+
| library-lock- | Resolve prod.lock file                               |
| prod          |                                                      |
+---------------+------------------------------------------------------+
| library-remov | Remove a given package from a given dependency group |
| e             |                                                      |
+---------------+------------------------------------------------------+
| library-searc | Search for pip packages                              |
| h             |                                                      |
+---------------+------------------------------------------------------+
| library-sync- | Sync dev environment with packages listed in         |
| dev           | dev.lock                                             |
+---------------+------------------------------------------------------+
| library-sync- | Sync prod environment with packages listed in        |
| prod          | prod.lock                                            |
+---------------+------------------------------------------------------+
| library-updat | Update dev dependencies                              |
| e             |                                                      |
+---------------+------------------------------------------------------+
| session-lab   | Run jupyter lab server                               |
+---------------+------------------------------------------------------+
| session-pytho | Run python session with dev dependencies             |
| n             |                                                      |
+---------------+------------------------------------------------------+
| state         | State of {{cookiecutter.repo}}                                    |
+---------------+------------------------------------------------------+
| test-coverage | Generate test coverage report                        |
+---------------+------------------------------------------------------+
| test-dev      | Run all tests                                        |
+---------------+------------------------------------------------------+
| test-fast     | Test all code excepts tests marked with              |
|               | SKIP_SLOWS_TESTS decorator                           |
+---------------+------------------------------------------------------+
| test-lint     | Run linting and type checking                        |
+---------------+------------------------------------------------------+
| test-prod     | Run tests across all support python versions         |
+---------------+------------------------------------------------------+
| version       | Full resolution of repo: dependencies, linting,      |
|               | tests, docs, etc                                     |
+---------------+------------------------------------------------------+
| version-bump- | Bump pyproject major version                         |
| major         |                                                      |
+---------------+------------------------------------------------------+
| version-bump- | Bump pyproject minor version                         |
| minor         |                                                      |
+---------------+------------------------------------------------------+
| version-bump- | Bump pyproject patch version                         |
| patch         |                                                      |
+---------------+------------------------------------------------------+
| zsh           | Run ZSH session inside {{cookiecutter.repo}} container            |
+---------------+------------------------------------------------------+
| zsh-complete  | Generate oh-my-zsh completions                       |
+---------------+------------------------------------------------------+
| zsh-root      | Run ZSH session as root inside {{cookiecutter.repo}} container    |
+---------------+------------------------------------------------------+

Flags
~~~~~

===== ======= ====================================================
Short Long    Description
===== ======= ====================================================
-a    –args   Additional arguments, this can generally be ignored
-h    –help   Prints command help message to stdout
\     –dryrun Prints command that would otherwise be run to stdout
===== ======= ====================================================
