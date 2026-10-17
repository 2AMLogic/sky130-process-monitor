# Digital smoke: lint (Verilator), cocotb on Icarus, Yosys synth to sky130_fd_sc_hd tt.
# Entry point:  make -C verification/smoke all        (see verification/README.md)
SMOKE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO      := $(abspath $(SMOKE_DIR)/../..)
SIM_DIR   := $(REPO)/sim
VERILOG_SOURCES := $(REPO)/rtl/smoke/smoke.v


.PHONY: sim-run cocotb all check-env lint synth negative-control
all: check-env lint cocotb synth

check-env:
	@$(SIM_DIR)/check_env.sh >/dev/null && echo "check_env: OK"

lint: check-env
	verilator --lint-only -Wall --top-module smoke $(VERILOG_SOURCES)

cocotb: check-env
	$(MAKE) -f $(MAKEFILE_LIST) sim-run

sim-run:
	rm -f results.xml
	$(MAKE) -f $(SMOKE_DIR)/cocotb.mk
	@! grep -q '<failure' results.xml

synth: check-env
	@mkdir -p $(REPO)/sim/build
	LIBERTY="$$($(SIM_DIR)/check_env.sh | sed -n 's/^PDK_ROOT=//p')/$$(python3 -I -c 'import json;print(json.load(open("$(SIM_DIR)/pdk.json"))["liberty_tt"])')" \
	RTL=$(VERILOG_SOURCES) OUT=$(REPO)/sim/build/smoke_synth.v \
	yosys -q -l $(REPO)/sim/build/smoke_synth.log -c $(SMOKE_DIR)/synth.tcl
	@grep -q sky130_fd_sc_hd__ $(REPO)/sim/build/smoke_synth.v && echo "synth: mapped to sky130_fd_sc_hd"

negative-control: check-env
	@fail=0; \
	if SMOKE_BREAK=1 $(MAKE) -f $(MAKEFILE_LIST) sim-run >/dev/null 2>&1; then \
	  echo "NEG-CONTROL FAIL: broken cocotb expectation passed"; fail=1; \
	else echo "neg-control ok (failed as required): broken cocotb expectation"; fi; \
	if LIBERTY=/nonexistent.lib RTL=$(VERILOG_SOURCES) OUT=/dev/null yosys -q -c $(SMOKE_DIR)/synth.tcl >/dev/null 2>&1; then \
	  echo "NEG-CONTROL FAIL: missing Liberty passed"; fail=1; \
	else echo "neg-control ok (failed as required): wrong Liberty path"; fi; \
	exit $$fail
