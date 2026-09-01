#include "mlir/Pass/Pass.h"
#include "mlir/Transforms/DialectConversion.h"
#include "mlir/Dialect/Func/IR/FuncOps.h"

using namespace mlir;

namespace {
struct LowerApexToStandard : public PassWrapper<LowerApexToStandard, OperationPass<func::FuncOp>> {
  MLIR_DEFINE_EXPLICIT_INTERNAL_INLINE_TYPE_ID(LowerApexToStandard)

  void runOnOperation() override {
    // walks all apex.changeset ops, converts to memref allocations
    // all apex.action ops to function calls
    // apex.verify to arith.constant true
    // apex.commit to memref store
  }
};
} // end anonymous namespace

MLIR_DEFINE_EXPLICIT_TYPE_ID(LowerApexToStandard)
