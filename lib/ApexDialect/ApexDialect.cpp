#include "ApexDialect.h"
#include "mlir/IR/DialectImplementation.h"
#include "mlir/IR/Types.h"

using namespace mlir;
using namespace mlir::apex;

void ApexDialect::initialize() {
}

ApexDialect::ApexDialect(mlir::MLIRContext *ctx)
    : mlir::Dialect(getDialectNamespace(), ctx, mlir::TypeID::get<ApexDialect>()) {
  initialize();
}
