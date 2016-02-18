#!/usr/bin/env python2.7
#
# A container skeleton for the Docker From Scratch workshop
#

from __future__ import print_function

import click
import os


@click.group()
def cli():
    pass


def contain(command):
    """
    Step 0: a simple exec
    """
    os.execvp(command[0], command[0:])


@cli.command()
@click.argument('Command', help='The command that you want to contain', required=True, nargs=-1)
def run(command):
    pid = os.fork()
    if pid == 0:
        contain(command)
    else:
        _, status = os.waitpid(pid, 0)
        print('{} exited with status {}'.format(pid, status))


if __name__ == '__main__':
    cli()
