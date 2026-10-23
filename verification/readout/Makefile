# Readout: lint (Verilator) and cocotb on Icarus for rtl/readout/.
# Entry point:  make -C verification/readout          (see verification/README.md)
# Targets mirror verification/smoke/Makefile (check-env, lint, cocotb); pins are in sim/toolchain.json.
READOUT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO        := $(abspath $(READOUT_DIR)/../..)
SIM_DIR     := $(REPO)/sim
VERILOG_SOURCES := $(REPO)/rtl/readout/readout.v $(REPO)/rtl/readout/readout_counter.v

.PHONY: all sim-run cocotb check-env lint negative-control
all: check-env lint cocotb

check-env:
	@$(SIM_DIR)/check_env.sh >/dev/null && echo "check_env: OK"

lint: check-env
	verilator --lint-only -Wall --top-module readout $(VERILOG_SOURCES)

cocotb: check-env
	$(MAKE) -f $(MAKEFILE_LIST) sim-run

sim-run:
	rm -f results.xml
	$(MAKE) -f $(READOUT_DIR)/cocotb.mk
	@test -s results.xml && ! grep -q '<failure' results.xml

# A deliberately wrong expected count must fail with an AssertionError.
negative-control: check-env
	@out="$$(READOUT_BREAK=1 $(MAKE) -f $(MAKEFILE_LIST) sim-run 2>&1)"; rc=$$?; \
	if [ $$rc -eq 0 ]; then echo "NEG-CONTROL FAIL: broken expected count passed"; exit 1; \
	elif printf '%s\n' "$$out" | grep -q 'AssertionError'; then \
	  echo "neg-control ok (failed as required, AssertionError seen): broken expected count"; \
	else echo "NEG-CONTROL FAIL: failed for the wrong reason"; printf '%s\n' "$$out" | tail -5; exit 1; fi
