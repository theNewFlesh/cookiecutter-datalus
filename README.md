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
2. `cookiecutter https://github.com/thenewflesh/cookiecutter-datalus`
