#[derive(Debug)]
pub enum DslToken {
    Changeset(String, String),
    Action(String, String),
    Commit,
    Abort(String),
}

pub struct MlirEmitter {
    pub indent: usize,
    pub output: String,
}

impl MlirEmitter {
    pub fn new() -> Self {
        Self {
            indent: 2,
            output: String::new(),
        }
    }

    pub fn emit_module(&mut self, tokens: &[DslToken]) -> String {
        self.output.push_str("func.func @main() {\n");
        let mut cs_idx = 0;
        for token in tokens {
            match token {
                DslToken::Changeset(op_id, target) => self.emit_changeset(&mut cs_idx, op_id, target),
                DslToken::Action(action_type, params) => self.emit_action(&mut cs_idx, action_type, params),
                DslToken::Commit => self.emit_commit(cs_idx),
                DslToken::Abort(reason) => self.emit_abort(cs_idx, reason),
            }
        }
        self.output.push_str("  return\n}\n");
        self.output.clone()
    }

    fn emit_changeset(&mut self, cs_idx: &mut usize, op_id: &str, target: &str) {
        self.output.push_str(&format!("  %cs{} = apex.changeset \"{}\", \"{}\" : () -> !apex.changeset\n", cs_idx, op_id, target));
    }

    fn emit_action(&mut self, cs_idx: &mut usize, action_type: &str, params: &str) {
        let next_cs = *cs_idx + 1;
        let p = params.replace("\"", "\\\"");
        self.output.push_str(&format!("  %cs{} = apex.action %cs{}, \"{}\", \"{}\" : !apex.changeset, !apex.str, !apex.str -> !apex.changeset\n", next_cs, cs_idx, action_type, p));
        *cs_idx = next_cs;
    }

    fn emit_commit(&mut self, cs_idx: usize) {
        self.output.push_str(&format!("  %r = apex.commit %cs{} : !apex.changeset -> !apex.receipt\n", cs_idx));
    }

    fn emit_abort(&mut self, cs_idx: usize, reason: &str) {
        self.output.push_str(&format!("  apex.abort %cs{}, \"{}\" : !apex.changeset, !apex.str -> !apex.void\n", cs_idx, reason));
    }
}
