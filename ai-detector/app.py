from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import List, Optional, Tuple
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re

api = FastAPI(title="ai-detector", version="0.1.0")

# Shared screenshots directory (mounted as ./captures on host)
CAPTURES_DIR = Path("/data/captures")

# Default menu-like keywords
KEYWORDS = [
    r"\bpress\s+start\b",
    r"\bstart\b",
    r"\boptions?\b",
    r"\bselect\b",
    r"\bmenu\b",
]

# ---------- Data models ----------
class AnalyzeRequest(BaseModel):
    filename: str
    keywords: Optional[List[str]] = None

# ---------- Helpers ----------
def _read_image(p: Path):
    im = Image.open(p).convert("RGB")
    return np.array(im)

def _preproc(img_rgb: np.ndarray) -> np.ndarray:
    g = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    g = cv2.bilateralFilter(g, 7, 50, 50)
    g = cv2.convertScaleAbs(g, alpha=1.2, beta=10)
    return g

def _ocr(g: np.ndarray):
    data = pytesseract.image_to_data(g, output_type=pytesseract.Output.DICT)
    words, confs = [], []
    for t, c in zip(data.get("text", []), data.get("conf", [])):
        if t and t.strip():
            words.append(t.strip())
            try:
                confs.append(float(c))
            except:
                pass
    text = " ".join(words)
    avg = float(np.mean(confs)) if confs else 0.0
    return text, avg

def _newest_capture(dirpath: Path) -> Tuple[Path, list[str]]:
    """Return newest PNG/JPG in /data/captures and a short listing for debug."""
    candidates = list(dirpath.glob("*.png")) + list(dirpath.glob("*.jpg")) + list(dirpath.glob("*.jpeg"))
    if not candidates:
        raise FileNotFoundError("No PNG/JPG images found in captures")
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0], [c.name for c in candidates[:10]]

# ---------- API ----------
@api.post("/analyze")
def analyze(req: AnalyzeRequest):
    p = (CAPTURES_DIR / req.filename).resolve()
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {req.filename}")
    img = _read_image(p)
    g = _preproc(img)
    text, avg_conf = _ocr(g)
    patterns = [re.compile(k, re.IGNORECASE) for k in (req.keywords or KEYWORDS)]
    hits = [pat.pattern for pat in patterns if pat.search(text.lower())]
    return {
        "filename": req.filename,
        "is_menu": len(hits) > 0,
        "avg_conf": round(avg_conf, 1),
        "keywords_hit": hits,
        "text_excerpt": text[:300],
    }

@api.get("/latest")
def analyze_latest():
    try:
        newest, listing = _newest_capture(CAPTURES_DIR)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    img = _read_image(newest)
    g = _preproc(img)
    text, avg_conf = _ocr(g)
    patterns = [re.compile(k, re.IGNORECASE) for k in KEYWORDS]
    hits = [pat.pattern for pat in patterns if pat.search(text.lower())]
    return {
        "filename": newest.name,
        "is_menu": len(hits) > 0,
        "avg_conf": round(avg_conf, 1),
        "keywords_hit": hits,
        "text_excerpt": text[:300],
        "debug_recent_files": listing,
    }

@api.get("/healthz")
def healthz():
    return {"ok": True}
