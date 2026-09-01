#ifndef APEX_DIALECT_TD
#define APEX_DIALECT_TD

include "mlir/IR/OpBase.td"

def Apex_Dialect : Dialect {
  let name = "apex";
  let cppNamespace = "::mlir::apex";
  let summary = "The APEX custom MLIR dialect for swarm agent operations";
}

class Apex_Op<string mnemonic, list<Trait> traits = []> : Op<Apex_Dialect, mnemonic, traits>;

def Apex_ChangesetOp : Apex_Op<"changeset"> {
  let summary = "Create a new changeset";
  let arguments = (ins StrAttr:$operation_id, StrAttr:$target);
  let results = (outs AnyType:$cs);
}

def Apex_ActionOp : Apex_Op<"action"> {
  let summary = "Add action to changeset";
  let arguments = (ins AnyType:$cs, StrAttr:$action_type, StrAttr:$params);
  let results = (outs AnyType:$res_cs);
}

def Apex_VerifyOp : Apex_Op<"verify"> {
  let summary = "Static verify op";
  let arguments = (ins AnyType:$cs);
  let results = (outs AnyType:$valid);
}

def Apex_CommitOp : Apex_Op<"commit"> {
  let summary = "Commit changeset";
  let arguments = (ins AnyType:$cs);
  let results = (outs AnyType:$receipt);
}

def Apex_AbortOp : Apex_Op<"abort"> {
  let summary = "Abort changeset";
  let arguments = (ins AnyType:$cs, StrAttr:$reason);
}

#endif // APEX_DIALECT_TD
