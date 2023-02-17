{%- set REPO_NAME = cookiecutter.repo | replace('-', '_') | upper -%}
import subprocess

import click
# ------------------------------------------------------------------------------

'''
Command line interface to {{ cookiecutter.repo }} library
'''


@click.group()
def main():
    pass


@main.command()
def bash_completion():
    '''
        BASH completion code to be written to a _{{ cookiecutter.repo }} completion file.
    '''
    cmd = '_{{ REPO_NAME }}_COMPLETE=bash_source {{ cookiecutter.repo }}'
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result.wait()
    click.echo(result.stdout.read())


@main.command()
def zsh_completion():
    '''
        ZSH completion code to be written to a _{{ cookiecutter.repo }} completion file.
    '''
    cmd = '_{{ REPO_NAME }}_COMPLETE=zsh_source {{ cookiecutter.repo }}'
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result.wait()
    click.echo(result.stdout.read())


if __name__ == '__main__':
    main()
