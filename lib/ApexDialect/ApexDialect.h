#ifndef APEX_DIALECT_H
#define APEX_DIALECT_H

#include "mlir/IR/Dialect.h"

namespace mlir {
namespace apex {

class ApexDialect : public mlir::Dialect {
public:
  explicit ApexDialect(mlir::MLIRContext *ctx);
  static mlir::StringRef getDialectNamespace() { return "apex"; }
  void initialize();
};

} // namespace apex
} // namespace mlir

#endif // APEX_DIALECT_H
