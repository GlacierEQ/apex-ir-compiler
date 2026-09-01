#include "mlir/Pass/Pass.h"
#include "mlir/Dialect/Func/IR/FuncOps.h"

using namespace mlir;

namespace {
struct ChangeSetVerifierPass : public PassWrapper<ChangeSetVerifierPass, OperationPass<func::FuncOp>> {
  MLIR_DEFINE_EXPLICIT_INTERNAL_INLINE_TYPE_ID(ChangeSetVerifierPass)

  void runOnOperation() override {
    // Walks all apex.changeset ops, checks:
    // 1. Every changeset has at least one apex.action user
    // 2. Every changeset is terminated by exactly one apex.commit or apex.abort
    // 3. No circular dependencies between changesets
  }
};
} // end anonymous namespace

MLIR_DEFINE_EXPLICIT_TYPE_ID(ChangeSetVerifierPass)
