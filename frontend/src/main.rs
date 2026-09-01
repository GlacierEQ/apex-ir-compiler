mod ast_to_mlir;
use ast_to_mlir::{DslToken, MlirEmitter};
use std::env;
use std::fs;
use std::io::{self, Read};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ParseError {
    #[error("Invalid line format: {0}")]
    InvalidLine(String),
    #[error("Missing argument: {0}")]
    MissingArgument(String),
}

fn tokenize(input: &str) -> Result<Vec<DslToken>, ParseError> {
    let mut tokens = Vec::new();
    for line in input.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        let parts: Vec<&str> = line.split_whitespace().collect();
        match parts[0] {
            "CHANGESET" => {
                if parts.len() < 3 {
                    return Err(ParseError::MissingArgument("CHANGESET needs op-id and target".to_string()));
                }
                let op_id = parts[1].to_string();
                let target = parts[2].strip_prefix("target=").unwrap_or(parts[2]).to_string();
                tokens.push(DslToken::Changeset(op_id, target));
            }
            "ACTION" => {
                if parts.len() < 3 {
                    return Err(ParseError::MissingArgument("ACTION needs action_type and params".to_string()));
                }
                let action_type = parts[1].to_string();
                let params_idx = line.find("params=").ok_or_else(|| ParseError::MissingArgument("params".into()))?;
                let params = line[params_idx + 7..].to_string();
                tokens.push(DslToken::Action(action_type, params));
            }
            "COMMIT" => tokens.push(DslToken::Commit),
            "ABORT" => {
                let reason = if parts.len() > 1 { parts[1..].join(" ") } else { "".to_string() };
                tokens.push(DslToken::Abort(reason));
            }
            _ => return Err(ParseError::InvalidLine(line.to_string())),
        }
    }
    Ok(tokens)
}

fn emit_mlir(tokens: &[DslToken]) -> String {
    let mut emitter = MlirEmitter::new();
    emitter.emit_module(tokens)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut input = String::new();
    
    if args.len() > 1 {
        input = fs::read_to_string(&args[1]).unwrap();
    } else {
        io::stdin().read_to_string(&mut input).unwrap();
    }

    match tokenize(&input) {
        Ok(tokens) => {
            let mlir = emit_mlir(&tokens);
            print!("{}", mlir);
        }
        Err(e) => eprintln!("Error: {}", e),
    }
}
