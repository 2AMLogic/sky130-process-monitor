# Inner cocotb makefile (kept separate so the outer Makefile can re-invoke it).
SIM ?= icarus
TOPLEVEL_LANG ?= verilog
READOUT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO := $(abspath $(READOUT_DIR)/../..)
VERILOG_SOURCES = $(REPO)/rtl/readout/readout.v $(REPO)/rtl/readout/readout_counter.v
COCOTB_TOPLEVEL = readout
COCOTB_TEST_MODULES = test_readout
SIM_BUILD = $(REPO)/sim/build/cocotb_readout
export PYTHONPATH := $(READOUT_DIR):$(PYTHONPATH)
include $(shell cocotb-config --makefiles)/Makefile.sim
