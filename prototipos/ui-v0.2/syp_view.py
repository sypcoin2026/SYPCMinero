"""Normalizacion visual de snapshots SYPminer. Sin IO, solo stdlib.

El dato recibido se trata como observacion, nunca como prueba de minado.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import math
import re
import time
import unicodedata

ND = "N/D"
VALID_STATES = {"OK", "N/D", "DESCONECTADO", "DESACTIVADO"}


def safe(value: object, size: int = 120) -> str:
    """Neutraliza controles de terminal y limita longitudes de fuentes externas."""
    s = str(value or "")
    s = re.sub(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\)?)?", "", s)
    s = "".join(ch if ch.isprintable() else " " for ch in s)
    return s[:size] if len(s) <= size else s[:size-1] + "…"


def finite(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def canonical_name(value: object) -> str:
    name = safe(value, 60).upper()
    plain = "".join(ch for ch in unicodedata.normalize("NFKD", name)
                    if not unicodedata.combining(ch))
    for token, canon in (("GUARDIAN", "GUARDIAN"), ("GPU", "GPU"),
                         ("SOAT", "SOAT"), ("NOD", "NODOS"),
                         ("EMISION", "EMISION")):
        if token in plain:
            return canon
    return name


def state(value: object) -> str:
    s = safe(value, 32).upper()
    return s if s in VALID_STATES else ND


@dataclass(frozen=True)
class Metric:
    label: str
    text: str = ND
    number: float | None = None
    present: bool = False


@dataclass
class Source:
    name: str
    status: str = ND
    detail: str = ""
    fields: dict[str, Metric] = field(default_factory=dict)

    def get(self, *names: str) -> Metric:
        for key in names:
            key = key.casefold().strip()
            if key in self.fields:
                return self.fields[key]
        return Metric(names[0] if names else "")


@dataclass
class View:
    clock: str = ""
    created_at: float | None = None
    sources: dict[str, Source] = field(default_factory=dict)
    origin: str = "sin configurar"
    error: str = ""
    stale: bool = False

    def src(self, name: str) -> Source:
        canon = canonical_name(name)
        return self.sources.get(canon, Source(canon))


def _metric(d: dict[str, Any]) -> Metric:
    label = safe(d.get("label", ""), 100)
    data = d.get("data")
    raw = d.get("value")
    if raw is None:
        raw = ND
    value = safe(raw, 130) or ND
    ispresent = (data is not None and value != ND) or (data is None and value not in (ND, ""))
    number = float(data) if finite(data) else None
    if ispresent and value == ND and finite(data):
        value = str(data)
    return Metric(label, value, number, ispresent)


def normalize(payload: object, *, origin: str = "JSON", now: float | None = None,
              file_mtime: float | None = None, stale_after: float = 20.0) -> View:
    """Acepta el esquema sources/fields del ZIP v0.1 y campos planos opcionales.

    Lo no reconocido se deja N/D. Nunca infiere alturas, recompensas o uso GPU.
    """
    if now is None:
        now = time.time()
    v = View(origin=safe(origin, 160))
    if not isinstance(payload, dict):
        v.error = "El JSON no contiene un objeto valido"
        return v
    v.clock = safe(payload.get("clock", ""), 25)
    generated_at = payload.get("generated_at")
    if finite(generated_at):
        v.created_at = float(generated_at)
    if file_mtime is not None and math.isfinite(file_mtime):
        v.stale = (now - file_mtime) > stale_after
    elif v.created_at is not None:
        v.stale = (now - v.created_at) > stale_after
    snapshots = payload.get("sources", [])
    if isinstance(snapshots, dict):
        snapshots = [dict(value, name=name) for name, value in snapshots.items()
                     if isinstance(value, dict)]
    if not isinstance(snapshots, list):
        snapshots = []
    for raw in snapshots[:20]:
        if not isinstance(raw, dict):
            continue
        name = canonical_name(raw.get("name", ""))
        if not name:
            continue
        src = Source(name, state(raw.get("status")), safe(raw.get("detail", ""), 180))
        fs = raw.get("fields", [])
        if isinstance(fs, dict):
            fs = [{"label": k, "value": x} for k,x in fs.items()]
        if isinstance(fs, list):
            for item in fs[:100]:
                if isinstance(item, dict):
                    m = _metric(item)
                    if m.label:
                        src.fields[m.label.casefold()] = m
        v.sources[name] = src
    # Compatibilidad cuidadosa con esquemas del tipo {"gpu": {"status":...}}.
    for key in ("gpu", "soat", "nodes", "nodos", "guardian", "guardian"):
        raw = payload.get(key)
        name = {"nodes": "NODOS", "nodos": "NODOS"}.get(key, key.upper())
        if name in v.sources or not isinstance(raw, dict):
            continue
        src = Source(name, state(raw.get("status")), safe(raw.get("detail", ""), 180))
        for label, value in raw.items():
            if label in ("status", "detail", "timestamp", "ts"):
                continue
            if isinstance(value, (str, int, float)) and not isinstance(value, bool):
                n = float(value) if finite(value) else None
                src.fields[label.casefold()] = Metric(safe(label), safe(value), n, True)
        v.sources[name] = src
    return v


def pick(v: View, source: str, *labels: str) -> Metric:
    """Obtiene un campo existente; no transforma unidades ni inventa datos."""
    return v.src(source).get(*labels)


def sources_summary(v: View) -> str:
    return "  ".join(f"{n}:{v.src(n).status}" for n in ("GPU", "SOAT", "NODOS", "GUARDIAN"))