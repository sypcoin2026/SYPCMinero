"""Vista Terminal PRO, solo render. No sondea dispositivos ni arranca mineria."""
from __future__ import annotations

from syp_view import ND, View, Source, safe, pick, sources_summary

C = {"cyan":"\x1b[96m", "green":"\x1b[92m", "yellow":"\x1b[93m", "red":"\x1b[91m",
     "grey":"\x1b[90m", "white":"\x1b[97m", "reset":"\x1b[0m"}


def _color(text: str, name: str, on: bool) -> str:
    return C.get(name, "") + text + C["reset"] if on else text


def _fit(s: object, width: int) -> str:
    v = safe(s, 1000)
    return v[:max(0, width-1)] + "…" if len(v) > width else v


def _section(src: Source, title: str, width: int, *, color: bool) -> list[str]:
    inner = width-2
    status_color = {"OK":"green", "N/D":"yellow", "DESCONECTADO":"red", "DESACTIVADO":"grey"}
    heading = _fit(f"{title}  [{src.status}]", inner-2)
    out = ["┌"+"─"*inner+"┐", "│ "+_color(heading,"cyan",color).ljust(0) + " "*(inner-2-len(heading))+" │"]
    for metric in list(src.fields.values())[:12]:
        label = _fit(metric.label, max(8, inner//2))
        val = _fit(metric.text, max(5, inner-4-len(label)))
        space = max(1, inner-3-len(label)-len(val))
        out.append("│ "+label+" "*space+val+" │")
    if not src.fields:
        note = _fit(src.detail or ND, inner-2)
        out.append("│ "+note+" "*(inner-2-len(note))+" │")
    out.append("└"+"─"*inner+"┘")
    return out


def _join(a: list[str], b: list[str], gap: int = 2) -> list[str]:
    left = max(len(line) for line in a)
    height = max(len(a),len(b))
    a = a+[" "*left]*(height-len(a))
    b = b+[" "*len(b[0])]*(height-len(b))
    # Color escapes are stripped for padding computation (only headers contain ANSI).
    import re
    return [x+" "*(max(0,left-len(re.sub(r'\x1b\[[0-9;]*m','',x))))+" "*gap+y for x,y in zip(a,b)]


def render(v: View, width: int = 110, color: bool = True) -> str:
    width = max(48, min(int(width), 180))
    lines = [_color("SYPcoin (SYPC)  ·  SYPminer Terminal PRO", "cyan", color),
             "Autolykos2  ·  MONITOR DE SOLO LECTURA  ·  Sin datos inventados",
             _fit(sources_summary(v), width), "═"*width]
    if v.error:
        lines.append(_color(_fit("AVISO: "+v.error, width),"yellow",color))
    if v.stale:
        lines.append(_color("DATOS ANTIGUOS: estas cifras NO son actividad actual", "red",color))
    if width>=94:
        left = width*42//100
        right = width-left-2
        gpu = _section(v.src("GPU"), "GPU AMD", left,color=color)
        soat = _section(v.src("SOAT"), "TRABAJO / SOAT", right,color=color)
        lines += _join(gpu,soat)
        lines.append("")
        nodes = _section(v.src("NODOS"), "RED / NODOS", right,color=color)
        guardian = _section(v.src("GUARDIAN"), "GUARDIAN", left,color=color)
        lines += _join(guardian,nodes)
    else:
        for name,title in [("GPU","GPU AMD"),("SOAT","TRABAJO / SOAT"),
                           ("NODOS","RED / NODOS"),("GUARDIAN","GUARDIAN")]:
            lines += _section(v.src(name),title,width,color=color)
    lines += ["",_color("N/D = no disponible  ·  Ninguna solucion SOAT implica bloque confirmado", "grey",color)]
    return "\n".join(lines)