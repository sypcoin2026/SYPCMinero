"""Obtiene un JSON existente, sin shell ni acciones mineras implícitas."""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from syp_view import View, normalize, safe

MAX_BYTES = 2 * 1024 * 1024


def _json_bytes(data: bytes) -> object:
    if len(data) > MAX_BYTES:
        raise ValueError("La respuesta JSON supera 2 MiB")
    def reject_constant(value: str) -> None:
        raise ValueError("Numero no finito: " + value)
    return json.loads(data.decode("utf-8"), parse_constant=reject_constant)


class Reader:
    """En modo comando solo ejecuta la orden explicita que configura el usuario.

    No abre sockets, no inicia SOAT, y nunca entra en namespaces.
    """
    def __init__(self, path: str | None = None, command: list[str] | None = None,
                 cwd: str | None = None, max_age_s: float = 20.0):
        if path and command:
            raise ValueError("Elige --json-file o --command, no ambos")
        self.path, self.command, self.cwd = path, command or [], cwd
        self.max_age_s = max_age_s

    def read(self) -> View:
        now = time.time()
        if not self.path and not self.command:
            return View(error="Sin origen configurado; todas las cifras son N/D")
        try:
            if self.path:
                p = Path(self.path)
                with p.open("rb") as fh:
                    data = fh.read(MAX_BYTES + 1)
                mtime = p.stat().st_mtime
                return normalize(_json_bytes(data), origin="archivo JSON", now=now,
                                 file_mtime=mtime, stale_after=self.max_age_s)
            # NO shell=True. No permisos elevados. No se fija un minero por defecto.
            run = subprocess.run(self.command, cwd=self.cwd or None, shell=False,
                                 capture_output=True, timeout=4.0, check=False)
            if run.returncode != 0:
                return View(error="El comando de lectura devolvio error %d" % run.returncode,
                            origin="comando JSON")
            return normalize(_json_bytes(run.stdout), origin="comando JSON", now=now,
                             stale_after=self.max_age_s)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError,
                subprocess.TimeoutExpired) as ex:
            return View(origin="fuente no disponible", error=safe(ex, 140))