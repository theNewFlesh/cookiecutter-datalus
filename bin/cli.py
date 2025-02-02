#!/usr/bin/env python3

from pathlib import Path
import argparse
import re
import os
import json
import shutil
import subprocess
# ------------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        usage='''
Helper CLI for datalus repos.

Commands:
  - test
  - update
  - generate'''
    )
    parser.add_argument('command', help='Command to run')
    parser.add_argument('--source', help='.cruft.json file')
    parser.add_argument('--target', help='Target file or directory', required=True)
    parser.add_argument('--branch', help='Cruft branch', default='HEAD')
    args = parser.parse_args()
    if args.command == 'test':
        test(args.target)
    elif args.command == 'update':
        update(args.target, args.branch)
    elif args.command == 'generate':
        generate(args.source, args.target)


def test(target):
    tgt_ = Path(target, 'datalus-test')
    tgt = tgt_.as_posix()
    if tgt_.is_dir():
        shutil.rmtree(tgt)
    os.makedirs(tgt)
    cmd = 'cookiecutter . --no-input --config-file test_config.yml --output-dir {}'.format(tgt)
    subprocess.Popen(cmd, shell=True).wait()


def update(target, branch):
    tgt = Path(target, '.cruft.json').as_posix()
    with open(tgt) as f:
        raw_data = f.read()
        data = json.loads(raw_data)

    data['template'] = Path(os.getcwd()).absolute().as_posix()
    with open(tgt, 'w') as f:
        json.dump(data, f, indent=4)

    cmd = 'cruft diff --checkout {} > /tmp/cruft.diff'.format(branch)
    subprocess.Popen(cmd, shell=True, cwd=target).wait()

    with open(tgt, 'w') as f:
        f.write(raw_data)

    cmd = 'git apply /tmp/cruft.diff'
    subprocess.Popen(cmd, shell=True, cwd=target).wait()

    os.remove('/tmp/cruft.diff')

    cmd = 'git --no-pager diff --name-only'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd=target)
    proc.wait()

    diff = proc.stdout.read().decode('utf-8').split('\n')

    skip = data.get('skip', [])
    if skip != []:
        revert = filter(lambda x: re.search('|'.join(skip), x), diff)
        revert = ' '.join(list(revert))
        cmd = 'git checkout HEAD -- {}'.format(revert)
        subprocess.Popen(cmd, shell=True, cwd=target).wait()


def generate(source, target):
    with open(source) as f:
        data = json.load(f)
    data = dict(default_context=data['context']['cookiecutter'])
    with open(target, 'w') as f:
        json.dump(data, f, indent=4)
# ------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
