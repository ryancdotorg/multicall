MAKEFLAGS += --no-builtin-rules
export LANG=C LC_ALL=C

.PHONY: all clean _clean _nop

C ?= gcc
AS ?= gcc
PP ?= cpp
LD ?= ld

#override CPPFLAGS += ...
CFLAGS ?= -O2
override CFLAGS += -std=gnu17 -Wall -Wextra -pedantic \
	-D_ALL_SOURCE -D_GNU_SOURCE \
	-D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64

COMPILE = $(CC) $(CPPFLAGS) $(CFLAGS)

all: bin/multicall-miniverify-sha256sum

bin/multicall-miniverify-sha256sum: obj/multicall-miniverify-sha256sum.o ../sha256sum/obj/sha256sum_multicall.o ../minisign/obj/miniverify_multicall.o
	@mkdir -p $(@D)
	$(COMPILE) $^ $(LDFLAGS) -lsodium -lpthread -o $@

gen/multicall-miniverify-sha256sum.c: scripts/multicall.py
	@mkdir -p $(@D)
	python3 $< sha256sum miniverify,minisign > $@

# generic build rules
obj/%.o: src/%.c src/%.h
	@mkdir -p $(@D)
	$(COMPILE) -c $< -o $@

obj/%.o: src/%.c
	@mkdir -p $(@D)
	$(COMPILE) -c $< -o $@

obj/%.o: gen/%.c
	@mkdir -p $(@D)
	$(COMPILE) -c $< -o $@

# hack to force clean to run first *to completion* even for parallel builds
# note that $(info ...) prints everything on one line
clean: _nop $(foreach _,$(filter clean,$(MAKECMDGOALS)),$(info $(shell $(MAKE) _clean)))
_clean:
	rm -rf obj bin gen || /bin/true
_nop:
	@true
