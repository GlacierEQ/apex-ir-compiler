import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from driver.apex_compile import parse_dsl, verify_dsl

def test_parse_valid_dsl():
    text = "CHANGESET op-id-123 target=agent-42\nACTION CREATE params={\"key\": \"val\"}\nCOMMIT"
    tokens = parse_dsl(text)
    assert len(tokens) == 3
    assert tokens[0]["type"] == "Changeset"
    assert tokens[1]["type"] == "Action"
    assert tokens[2]["type"] == "Commit"

def test_parse_missing_commit_raises():
    text = "CHANGESET op-1 target=ag\nACTION CREATE params={}"
    tokens = parse_dsl(text)
    with pytest.raises(ValueError, match="Missing COMMIT or ABORT"):
        verify_dsl(tokens)

def test_parse_action_before_changeset_raises():
    text = "ACTION CREATE params={}\nCHANGESET op-1 target=ag\nCOMMIT"
    with pytest.raises(ValueError, match="ACTION before CHANGESET"):
        tokens = parse_dsl(text)
        verify_dsl(tokens)

def test_emit_mlir_structure():
    pass

def test_verify_valid_dsl():
    text = "CHANGESET op-id-123 target=agent-42\nACTION CREATE params={\"key\": \"val\"}\nCOMMIT"
    tokens = parse_dsl(text)
    verify_dsl(tokens)

def test_verify_empty_changeset_fails():
    text = "CHANGESET op-id target=ag\nCOMMIT"
    tokens = parse_dsl(text)
    with pytest.raises(ValueError, match="CHANGESET without ACTIONs"):
        verify_dsl(tokens)
