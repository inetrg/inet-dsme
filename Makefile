INET_PATH ?= ../../inet

OPP_MAKEMAKE_ARGS = -f --deep -KINET_PROJ=$(INET_PATH) -DINET_IMPORT -I. -I$$\(INET_PROJ\)/src -L$$\(INET_PROJ\)/src -lINET$$\(D\)

LORA_OMNETPP ?= 0

CMDENV ?= 0
VERBOSE ?= 0

ifneq (0, $(CMDENV))
  OMNETPP_EXTRA_ARGS += -u Cmdenv
  ifneq (0, $(VERBOSE))
    OMNETPP_EXTRA_ARGS += --cmdenv-express-mode=false
  endif
endif

ifneq (0, $(LORA_OMNETPP))
  OPP_MAKEMAKE_ARGS += -o inet-dsme_lora_omnetpp -KCFLAGS_EXTRA=-DLORA_SYMBOL_TIME
endif

OPP_RUN_ARGS += -r $(RUN) --seed-set=$(REP) --repeat=1 --vector-recording=$(VECTOR_RECORDING) $(OMNETPP_EXTRA_ARGS) -c $(CONFIG) -n .:../src:../../inet/examples:../../inet/src:../../inet/tutorials:.:../src -l ../../inet/src/INET --debug-on-errors=false example.ini


all: checkmakefiles
	cd src && $(MAKE)

clean: checkmakefiles
	cd src && $(MAKE) clean

cleanall: checkmakefiles
	cd src && $(MAKE) MODE=release clean
	cd src && $(MAKE) MODE=debug clean
	rm -f src/Makefile

makefiles:
	@cd src && opp_makemake $(OPP_MAKEMAKE_ARGS)

makefiles-lib:
	@cd src && opp_makemake $(OPP_MAKEMAKE_ARGS) -s

makefiles-static-lib:
	@cd src && opp_makemake $(OPP_MAKEMAKE_ARGS) -a

CONFIG ?= DSME
RUN ?= 0
REP ?= 0
VECTOR_RECORDING ?= true

run:
	cd simulations && ../src/inet-dsme $(OPP_RUN_ARGS)

checkmakefiles:
	@if [ ! -f src/Makefile ]; then \
	echo; \
	echo '======================================================================='; \
	echo 'src/Makefile does not exist. Please use "make makefiles" to generate it!'; \
	echo '======================================================================='; \
	echo; \
	exit 1; \
	fi
