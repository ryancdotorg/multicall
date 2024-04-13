#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <stdio.h>
#include <libgen.h>

int sha256sum_main(int argc, char *argv[]);
int miniverify_main(int argc, char *argv[]);

int main(int argc, char *argv[]) {
    char *argv0 = argv[0];
    int i = 0;
    char *prog;
    while (0 < argc && NULL != argv) {
        prog = i ? argv[0] : basename(argv[0]);
        if (strcmp(prog, "sha256sum") == 0) {
            return sha256sum_main(argc, argv);
        } else if (strcmp(prog, "miniverify") == 0 || strcmp(prog, "minisign") == 0) {
            return miniverify_main(argc, argv);
        }
        if (i++) break;
        --argc; ++argv;
    }
    fprintf(stderr,
        "%s: applet not found: '%s'\n"
        "Make a symlink pointing at this binary with one of the\n"
        "following names or run '%s <command>'.\n"
        "'sha256sum'\n"
        "'minisign'\n"
        "'miniverify'\n"
        , argv0, prog, argv0
    );
    return -1;
}
