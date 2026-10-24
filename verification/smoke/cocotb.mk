# Inner cocotb makefile (kept separate so the outer Makefile can re-invoke it).
SIM ?= icarus
TOPLEVEL_LANG ?= verilog
REPO := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/../..)
VERILOG_SOURCES = $(REPO)/rtl/smoke/smoke.v
COCOTB_TOPLEVEL = smoke
COCOTB_TEST_MODULES = test_smoke
SIM_BUILD = $(REPO)/sim/build/cocotb_smoke
include $(shell cocotb-config --makefiles)/Makefile.sim
