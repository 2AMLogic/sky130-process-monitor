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
	@test -s results.xml && ! grep -q '<failure' results.xml

synth: check-env
	@mkdir -p $(REPO)/sim/build
	LIBERTY="$$($(SIM_DIR)/check_env.sh | sed -n 's/^PDK_ROOT=//p')/$$(python3 -I -c 'import json;print(json.load(open("$(SIM_DIR)/pdk.json"))["liberty_tt"])')" \
	RTL=$(VERILOG_SOURCES) OUT=$(REPO)/sim/build/smoke_synth.v \
	yosys -q -l $(REPO)/sim/build/smoke_synth.log -c $(SMOKE_DIR)/synth.tcl
	@grep -q sky130_fd_sc_hd__ $(REPO)/sim/build/smoke_synth.v && echo "synth: mapped to sky130_fd_sc_hd"

negative-control: check-env
	@fail=0; \
	out="$$(SMOKE_BREAK=1 $(MAKE) -f $(MAKEFILE_LIST) sim-run 2>&1)"; rc=$$?; \
	if [ $$rc -eq 0 ]; then echo "NEG-CONTROL FAIL: broken cocotb expectation passed"; fail=1; \
	elif printf '%s\n' "$$out" | grep -q 'AssertionError'; then \
	  echo "neg-control ok (failed as required, AssertionError seen): broken cocotb expectation"; \
	else echo "NEG-CONTROL FAIL: broken cocotb expectation failed for the wrong reason"; \
	  printf '%s\n' "$$out" | tail -5; fail=1; fi; \
	out="$$(LIBERTY=/nonexistent.lib RTL=$(VERILOG_SOURCES) OUT=/dev/null yosys -q -c $(SMOKE_DIR)/synth.tcl 2>&1)"; rc=$$?; \
	if [ $$rc -eq 0 ]; then echo "NEG-CONTROL FAIL: missing Liberty passed"; fail=1; \
	elif printf '%s\n' "$$out" | grep -q "/nonexistent.lib' not found"; then \
	  echo "neg-control ok (failed as required, Liberty not found): wrong Liberty path"; \
	else echo "NEG-CONTROL FAIL: wrong Liberty path failed for the wrong reason"; \
	  printf '%s\n' "$$out" | tail -5; fail=1; fi; \
	exit $$fail
