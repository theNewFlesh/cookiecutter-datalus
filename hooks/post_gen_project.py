import json
import os
import re
import shutil
from pprint import pprint
# ------------------------------------------------------------------------------


def main():
    src = 'cookiecutter-config.json'
    with open(src) as f:
        config = json.load(f)

    pprint(config)
    repo = config['repo']
    repo_ = re.sub('-', '_', repo)
    rtype = config['repo_type']
    cli = config['include_prod_cli']

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

    os.remove(src)


main()
