.PHONY: rust-build python-test verify-example cmake-build

rust-build:
	source ~/.cargo/env && cd frontend && cargo build --release

python-test:
	python3 -m pytest tests/unit/ -v

verify-example:
	echo -e 'CHANGESET op-001 target=agent-42\nACTION CREATE params={}\nCOMMIT' | python3 driver/apex_compile.py verify

cmake-build:
	cmake -B build -DMLIR_DIR=$$(llvm-config --prefix)/lib/cmake/mlir && cmake --build build
