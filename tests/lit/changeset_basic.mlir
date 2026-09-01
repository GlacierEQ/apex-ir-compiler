// RUN: apex-compile %s | FileCheck %s
// CHECK: apex.changeset
// CHECK: apex.action
// CHECK: apex.commit
func.func @test_basic() {
  %cs = apex.changeset "op-001", "agent-42" : () -> !apex.changeset
  %cs2 = apex.action %cs, "CREATE", "{}" : !apex.changeset, !apex.str, !apex.str -> !apex.changeset
  %r = apex.commit %cs2 : !apex.changeset -> !apex.receipt
  return
}
