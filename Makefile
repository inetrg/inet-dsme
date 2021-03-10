all: checkmakefiles
	cd src && $(MAKE)

clean: checkmakefiles
	cd src && $(MAKE) clean

cleanall: checkmakefiles
	cd src && $(MAKE) MODE=release clean
	cd src && $(MAKE) MODE=debug clean
	rm -f src/Makefile

INET_PATH ?= ../../inet

OPP_MAKEMAKE_ARGS = -f --deep -KINET_PROJ=$(INET_PATH) -DINET_IMPORT -I. -I$$\(INET_PROJ\)/src -L$$\(INET_PROJ\)/src -lINET$$\(D\)

BUILD_LIB ?= 0

ifneq (0, $(BUILD_LIB))
  OPP_MAKEMAKE_ARGS += -s
endif

makefiles:
	@cd src && opp_makemake $(OPP_MAKEMAKE_ARGS)

checkmakefiles:
	@if [ ! -f src/Makefile ]; then \
	echo; \
	echo '======================================================================='; \
	echo 'src/Makefile does not exist. Please use "make makefiles" to generate it!'; \
	echo '======================================================================='; \
	echo; \
	exit 1; \
	fi
