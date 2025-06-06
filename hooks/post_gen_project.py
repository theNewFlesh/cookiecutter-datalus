import json
import os
import re
import shutil
# ------------------------------------------------------------------------------


def main():
    src = 'cookiecutter-config.json'
    with open(src) as f:
        config = json.load(f)

    repo = config['repo']
    repo_ = re.sub('-', '_', repo)
    rtype = config['repo_type']
    cli = config['include_prod_cli']
    mkdocs = config['include_mkdocs']
    helm = config['include_helm']
    git_host = config['git_host']
    prod_cli = config['include_prod_cli']
    secret_env = config['include_secret_env']

    if rtype == 'library':
        shutil.rmtree('helm')
        shutil.rmtree('python/' + repo_ + '/server')
        os.remove('sphinx/server.rst')

    if rtype != 'dash':
        shutil.rmtree('artifacts')
        shutil.rmtree('templates')
        os.remove('python/conftest.py')

    if cli == 'no':
        os.remove('python/' + repo_ + '/command.py')

    if mkdocs == 'no':
        shutil.rmtree('mkdocs')

    if helm == 'no':
        shutil.rmtree('helm', ignore_errors=True)

    if git_host == 'gitlab':
        os.rename('docs', 'public')

    if git_host != 'gitlab':
        os.remove('.gitlab-ci.yml')

    if git_host != 'github':
        shutil.rmtree('.github')

    if prod_cli == 'no':
        os.remove('docker/scripts/prod-cli')

    if secret_env == 'no':
        os.remove('docker/config/secret-env')

    os.remove(src)


main()
