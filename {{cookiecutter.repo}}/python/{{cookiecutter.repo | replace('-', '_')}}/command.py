{%- set cc = cookiecutter -%}
{%- set REPO_NAME = cc.repo | replace('-', '_') | upper -%}
import subprocess

import click
import lunchbox.theme as lbc
# ------------------------------------------------------------------------------

'''
Command line interface to {{ cc.repo }} library
'''

click.Context.formatter_class = lbc.ThemeFormatter


@click.group()
def main():
    pass


@main.command()
def bash_completion():
    '''
    BASH completion code to be written to a _{{ cc.repo }} completion file.
    '''
    cmd = '_{{ REPO_NAME }}_COMPLETE=bash_source {{ cc.repo }}'
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result.wait()
    click.echo(result.stdout.read())


@main.command()
def zsh_completion():
    '''
    ZSH completion code to be written to a _{{ cc.repo }} completion file.
    '''
    cmd = '_{{ REPO_NAME }}_COMPLETE=zsh_source {{ cc.repo }}'
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result.wait()
    click.echo(result.stdout.read())


if __name__ == '__main__':
    main()
