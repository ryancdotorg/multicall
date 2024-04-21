#!/usr/bin/env python3

from sys import argv, exit, stdin, stdout, stderr, version_info
from functools import partial
eprint = partial(print, file=stderr)

# Python standard library imports

# Third party library imports

# End imports

applets = {}

for arg in argv[1:]:
    applet, *aliases = arg.split(',')
    applets[applet] = aliases

print("""
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <stdio.h>
#include <libgen.h>
""".lstrip())

for applet in applets.keys():
    print(f'int {applet}_main(int argc, char *argv[]);')

print("""
int main(int argc, char *argv[]) {
  char *argv0 = argv[0];
  int i = 0;
  char *prog = NULL;
  while (0 < argc && NULL != argv) {
    prog = i ? argv[0] : basename(argv[0]);
""".rstrip())

for i, tup in enumerate(applets.items()):
    applet, aliases = tup
    cond = '} else ' if i > 0 else ''
    check = ' || '.join(map(lambda x: f'strcmp(prog, "{x}") == 0', [applet] + aliases))
    print(f'    {cond}if ({check}) {{')
    print(f'      return {applet}_main(argc, argv);')

print("""    }
    if (i++) break;
    --argc; ++argv;
  }
  fprintf(stderr,
    "%s: applet not found: '%s'\\n"
    "Make a symlink pointing at this binary with one of the\\n"
    "following names or run '%s <command>'.\\n"
""".rstrip())

for i, tup in enumerate(applets.items()):
    applet, aliases = tup
    line = f"    \"'{applet}'"
    if len(aliases) == 1:
        line += f" (alias: '{aliases[0]}')"
    elif len(aliases) > 1:
        joined = ', '.join(map(lambda x: f"'{x}'", aliases))
        line += f" (aliases: {joined})"
    line += '\\n"'
    print(line)

print("""    , argv0, prog, argv0
  );
  return -1;
}
""".rstrip())
