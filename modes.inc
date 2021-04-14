# add custom modes
INET_DSME_CFLAGS = -DLORA_SYMBOL_TIME
ALL_MODES = release debug sanitize lora_omnetpp lora_omnetpp_debug
# this is the default mode
MODE = release
ifeq ($(MODE),release)
  CFLAGS = $(CFLAGS_RELEASE)
  D=
else ifeq ($(MODE),debug)
  CFLAGS = $(CFLAGS_DEBUG)
  D=_dbg
else ifeq ($(MODE),sanitize)
  CFLAGS = $(CFLAGS_DEBUG) $(SANITIZE_FLAGS)
  LDFLAGS = $(SANITIZE_FLAGS)
  D=_sanitize
else ifeq ($(MODE),lora_omnetpp)
  CFLAGS = $(CFLAGS_RELEASE) $(INET_DSME_CFLAGS)
  D=
  TARGET_NAME=$(LIB_PREFIX)inet-dsme_lora_omnetpp$(D)
else ifeq ($(MODE),lora_omnetpp_debug)
  CFLAGS = $(CFLAGS_DEBUG) $(INET_DSME_CFLAGS)
  D=_dbg
  TARGET_NAME=$(LIB_PREFIX)inet-dsme_lora_omnetpp$(D)
else
  $(error Unknown mode: '$(MODE)'. Accepted modes: $(ALL_MODES); or define your own mode in 'Makefile.inc.in')
endif
