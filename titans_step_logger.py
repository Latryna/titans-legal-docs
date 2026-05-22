# Minimal cognitive-step logger (single-process, file-backed). Python 3.10+

import os, json, time, sqlite3, hashlib
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from pathlib import Path

DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)
LOG_JSONL = DATA_DIR / "steps.jsonl"
DB_SQLITE = DATA_DIR / "index.sqlite"

# --- M1..M5 ultra-stubs (replace with real modules) ---
def m1_perception(x: str) -> Dict[str, Any]:
    # F: placeholder for real encoder/vision; here: toy features
    return {"tokens": x.split(), "len": len(x)}

def m3_abstraction(percept: Dict[str, Any]) -> Dict[str, Any]:
    # F: toy "concept": length bucket
    L = percept["len"]
    concept = "SHORT" if L < 64 else "LONG"
    return {"concept": concept}

def m4_reasoning(concept: Dict[str, Any]) -> Dict[str, Any]:
    # F: toy rule
    plan = "SUMMARIZE" if concept["concept"] == "LONG" else "VERBATIM"
    return {"plan": plan}

def m5_agency(plan: Dict[str, Any], x: str) -> Dict[str, Any]:
    # F: toy act
    if plan["plan"] == "SUMMARIZE":
        y = (x[:80] + "...") if len(x) > 80 else x
    else:
        y = x
    # F: toy uncertainty delta
    return {"action": plan["plan"], "output": y, "delta_uncertainty": 0.1 if plan["plan"]=="SUMMARIZE" else 0.02}

# --- Step schema ---
@dataclass
class Step:
    ts: float
    trace_id: str
    source: str
    event: str
    payload: Dict[str, Any]
    metrics: Dict[str, float]
    prev_hash: Optional[str] = None
    hash: Optional[str] = None

def step_hash(s: Step) -> str:
    b = json.dumps({
        "ts": s.ts, "trace_id": s.trace_id, "source": s.source, "event": s.event,
        "payload": s.payload, "metrics": s.metrics, "prev_hash": s.prev_hash
    }, sort_keys=True).encode("utf-8")
    return hashlib.sha256(b).hexdigest()

# --- Append-only log + index ---
def ensure_db():
    conn = sqlite3.connect(DB_SQLITE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS steps(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts REAL, trace_id TEXT, source TEXT, event TEXT,
        hash TEXT UNIQUE, prev_hash TEXT, offset INTEGER
    )""")
    c.execute("CREATE INDEX IF NOT EXISTS idx_trace ON steps(trace_id)")
    conn.commit(); conn.close()

def append_step(s: Step):
    # append JSONL
    line = json.dumps(asdict(s), ensure_ascii=False)
    with open(LOG_JSONL, "ab") as f:
        off = f.tell()
        f.write((line + "\n").encode("utf-8"))
    # index
    conn = sqlite3.connect(DB_SQLITE)
    c = conn.cursor()
    c.execute("INSERT INTO steps(ts, trace_id, source, event, hash, prev_hash, offset) VALUES(?,?,?,?,?,?,?)",
              (s.ts, s.trace_id, s.source, s.event, s.hash, s.prev_hash, off))
    conn.commit(); conn.close()

def latest_hash(trace_id: str) -> Optional[str]:
    conn = sqlite3.connect(DB_SQLITE); c = conn.cursor()
    c.execute("SELECT hash FROM steps WHERE trace_id=? ORDER BY id DESC LIMIT 1", (trace_id,))
    row = c.fetchone(); conn.close()
    return row[0] if row else None

# --- One cognitive step run ---
def run_step(trace_id: str, x: str):
    prev = latest_hash(trace_id)
    # M1
    p = m1_perception(x)
    s1 = Step(time.time(), trace_id, "M1", "PERCEPT", p, {"dt_ms": 0.0}, prev_hash=prev); s1.hash = step_hash(s1)
    append_step(s1)
    # M3
    a = m3_abstraction(p)
    s2 = Step(time.time(), trace_id, "M3", "ABSTRACT", a, {"dt_ms": 0.0}, prev_hash=s1.hash); s2.hash = step_hash(s2)
    append_step(s2)
    # M4
    r = m4_reasoning(a)
    s3 = Step(time.time(), trace_id, "M4", "REASON", r, {"dt_ms": 0.0}, prev_hash=s2.hash); s3.hash = step_hash(s3)
    append_step(s3)
    # M5
    act = m5_agency(r, x)
    s4 = Step(time.time(), trace_id, "M5", "ACT", act, {"dt_ms": 0.0, "delta_uncertainty": act["delta_uncertainty"]},
              prev_hash=s3.hash); s4.hash = step_hash(s4)
    append_step(s4)
    return act["output"]

if __name__ == "__main__":
    ensure_db()
    out = run_step(trace_id="demo-001", x="This is a very long input that should trigger the summarize plan in our toy pipeline.")
    print(out)
