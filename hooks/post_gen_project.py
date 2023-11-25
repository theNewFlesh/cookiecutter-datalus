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
    sphinx = config['include_sphinx']
    mkdocs = config['include_mkdocs']
    helm = config['include_helm']
    git_host = config['git_host']

    if rtype == 'library':
        shutil.rmtree('helm')
        shutil.rmtree('python/' + repo_ + '/server')
        os.remove('sphinx/server.rst')

    if rtype != 'dash':
        shutil.rmtree('artifacts')
        shutil.rmtree('templates')
        os.remove('python/conftest.py')

    if cli == 'no':
        os.remove('python/' + repo + '/command.py')

    if sphinx == 'no':
        shutil.rmtree('sphinx')
    
    if mkdocs == 'no':
        shutil.rmtree('mkdocs')

    if helm == 'no':
        shutil.rmtree('helm', ignore_errors=True)

    if git_host == 'gitlab':
        os.rename('docs', 'public')

    os.remove(src)


main()
