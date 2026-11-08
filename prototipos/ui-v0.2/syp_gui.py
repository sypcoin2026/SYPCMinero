"""Interfaz grafica para snapshots JSON de SYPminer. Solo lectura, stdlib."""
from __future__ import annotations

import collections
import re
import tkinter as tk
from tkinter import font

from syp_view import ND, Metric, View, pick, safe
from syp_source import Reader

BG = "#080D17"; BG2 = "#0D1424"; PANEL = "#141B2C"; PANEL2 = "#19233A"
BORDER = "#2A3551"; PURPLE = "#9566FF"; CYAN = "#44D5F5"; GREEN = "#4DE29A"
YELLOW = "#F7C65B"; RED = "#F26C84"; TEXT = "#E8F0FF"; MUTED = "#91A0BA"


def display_metric(metric: Metric, stale: bool) -> str:
    if stale and metric.present:
        return metric.text + " · histórico"
    return metric.text


class MinerGUI:
    def __init__(self, root: tk.Tk, reader: Reader, interval_ms: int = 2500):
        self.root, self.reader = root, reader
        self.interval_ms = max(1000,int(interval_ms))
        self.root.title("SYPcoin Miner — Panel visual (solo lectura)")
        self.root.configure(bg=BG)
        self.root.geometry("1500x950")
        self.root.minsize(1024,750)
        self.history = collections.deque(maxlen=240)
        self.rate_unit = ""
        self.view = View()
        self.cards: dict[str, tk.Label] = {}
        self.rows: dict[str, dict[str, tk.Label]] = {}
        self.summary_label = None
        self._layout()
        self.tick()

    def label(self, parent, content="", size=11, fg=TEXT, weight="normal", bg=None, **kw):
        return tk.Label(parent,text=content,fg=fg,bg=bg or parent.cget("bg"),
                        font=("DejaVu Sans",size,weight),anchor="w",**kw)

    def panel(self, parent, title: str, *, row: int, col: int, span: int = 1) -> tk.Frame:
        outer = tk.Frame(parent,bg=BORDER,padx=1,pady=1)
        outer.grid(row=row,column=col,columnspan=span,sticky="nsew",padx=8,pady=8)
        frame = tk.Frame(outer,bg=PANEL,padx=18,pady=14)
        frame.pack(fill="both",expand=True)
        self.label(frame,title,size=13,weight="bold").pack(anchor="w",pady=(0,10))
        return frame

    def _layout(self):
        base = tk.Frame(self.root,bg=BG)
        base.pack(fill="both",expand=True)
        sidebar = tk.Frame(base,bg=BG2,width=205)
        sidebar.pack(side="left",fill="y"); sidebar.pack_propagate(False)
        mark = tk.Canvas(sidebar,bg=BG2,height=128,highlightthickness=0)
        mark.pack(fill="x",pady=(18,0))
        mark.create_oval(62,12,144,94,outline=PURPLE,width=4)
        mark.create_text(103,53,text="SYPC",font=("DejaVu Sans",23,"bold"),fill=CYAN)
        self.label(sidebar,"SYPcoin Miner",size=14,weight="bold",bg=BG2).pack(padx=18,anchor="w")
        self.label(sidebar,"Panel de seguimiento",size=10,fg=MUTED,bg=BG2).pack(padx=18,anchor="w",pady=(2,24))
        for item in ("▣  Vista general", "◈  GPU", "◇  SOAT", "⌘  Red / Nodos", "⊡  Registro"):
            fg=TEXT if "Vista general" in item else MUTED
            lbl=self.label(sidebar,item,size=11,fg=fg,bg=PANEL2 if fg==TEXT else BG2)
            lbl.pack(fill="x",padx=12,pady=4,ipadx=12,ipady=10)
        tk.Frame(sidebar,bg=BG2).pack(fill="both",expand=True)
        self.label(sidebar,"SYPC · Prototipo v0.2",size=10,fg=CYAN,bg=BG2).pack(padx=18,anchor="w")
        self.label(sidebar,"Solo lectura",size=10,fg=MUTED,bg=BG2).pack(padx=18,anchor="w",pady=(2,24))
        main = tk.Frame(base,bg=BG,padx=13,pady=10)
        main.pack(side="left",fill="both",expand=True)
        head=tk.Frame(main,bg=BG)
        head.pack(fill="x",pady=(6,14))
        self.label(head,"SYPcoin (SYPC)  —  Panel de minería",size=19,weight="bold").pack(anchor="w")
        self.summary_label=self.label(head,"Esperando telemetría verificada · solo lectura",size=10,fg=MUTED)
        self.summary_label.pack(anchor="w",pady=(6,0))
        metrics=tk.Frame(main,bg=BG)
        metrics.pack(fill="x",pady=(0,10))
        for idx,(key,title) in enumerate((("hash","HASHRATE SOAT"),("difficulty","DIFICULTAD"),
                ("height","ALTURA NODOS"),("reward","RECOMPENSA"),("peers","CONEXIONES P2P"))):
            outer=tk.Frame(metrics,bg=BORDER,padx=1,pady=1)
            outer.grid(row=0,column=idx,sticky="nsew",padx=5)
            inside=tk.Frame(outer,bg=PANEL,padx=14,pady=10)
            inside.pack(fill="both",expand=True)
            self.label(inside,title,size=9,fg=MUTED).pack(anchor="w")
            value=self.label(inside,ND,size=17,fg=GREEN if idx==0 else TEXT,weight="bold")
            value.pack(anchor="w",pady=(8,0))
            self.cards[key]=value
            metrics.grid_columnconfigure(idx,weight=1,uniform="metrics")
        sections=tk.Frame(main,bg=BG)
        sections.pack(fill="both",expand=True)
        sections.grid_columnconfigure(0,weight=3)
        sections.grid_columnconfigure(1,weight=2)
        for index in range(3):
            sections.grid_rowconfigure(index,weight=1)
        chart=self.panel(sections,"Rendimiento de SOAT · muestras observadas en esta ventana",row=0,col=0)
        self.chart=tk.Canvas(chart,bg=PANEL,highlightthickness=0,height=140)
        self.chart.pack(fill="both",expand=True)
        self.chart.bind("<Configure>",lambda _: self.paint_chart())
        status=self.panel(sections,"Estado de las fuentes",row=0,col=1)
        self.status_rows={}
        for key in ("GPU", "SOAT", "NODOS", "GUARDIAN"):
            line=self.label(status,f"{key}  ·  N/D",size=11,fg=MUTED)
            line.pack(fill="x",pady=7)
            self.status_rows[key]=line
        gpu=self.panel(sections,"GPU AMD · sensores del equipo",row=1,col=0)
        self.rows["GPU"]=self.field_rows(gpu,["Temperatura", "Hotspot", "Memoria", "Consumo", "Ventilador", "Uso GPU"])
        nodes=self.panel(sections,"Red / Nodos · sin inferir consenso",row=1,col=1)
        self.rows["NODOS"]=self.field_rows(nodes,["Productor", "Receptor", "Altura", "Bloques confirmados"])
        soat=self.panel(sections,"SOAT · trabajo y resultados",row=2,col=0)
        self.rows["SOAT"]=self.field_rows(soat,["Hashrate", "Aceptadas SOAT", "Rechazadas SOAT", "Nonces", "Backend"])
        events=self.panel(sections,"Registro de observación",row=2,col=1)
        self.activity=tk.Text(events,bg=PANEL,fg=MUTED,font=("DejaVu Sans Mono",10),
                              relief="flat",highlightthickness=0,wrap="word",height=5)
        self.activity.pack(fill="both",expand=True)
        self.activity.insert("end","La ventana mostrará exclusivamente observaciones del monitor.\n")
        self.activity.config(state="disabled")
        tk.Frame(main,bg=BORDER,height=1).pack(fill="x",pady=(11,7))
        self.footer=self.label(main,"N/D = dato no disponible · No controla minería ni GPU · No son bloques los contadores SOAT",size=9,fg=MUTED)
        self.footer.pack(fill="x")

    def field_rows(self,parent,names):
        result={}
        for label in names:
            row=tk.Frame(parent,bg=PANEL)
            row.pack(fill="x",pady=4)
            self.label(row,label,size=10,fg=MUTED).pack(side="left")
            out=self.label(row,ND,size=10,fg=TEXT,weight="bold")
            out.pack(side="right")
            result[label]=out
        return result

    def _event(self,message):
        import time
        self.activity.config(state="normal")
        self.activity.insert("end",time.strftime("%H:%M:%S")+"  "+safe(message,180)+"\n")
        lines=int(self.activity.index("end-1c").split(".")[0])
        if lines>70:
            self.activity.delete("1.0",f"{lines-60}.0")
        self.activity.see("end")
        self.activity.config(state="disabled")

    def _value(self,source,*names):
        return display_metric(pick(self.view,source,*names),self.view.stale)

    def tick(self):
        old=self.view
        self.view=self.reader.read()
        v=self.view
        self.summary_label.config(text=("DATOS ANTIGUOS · no representan actividad actual" if v.stale else
                    (v.error if v.error else "Lecturas de las fuentes · no implica mineria activa")),
                    fg=RED if v.stale else YELLOW if v.error else MUTED)
        metric=pick(v,"SOAT","hashrate","MH/s actuales","hashrate actual","rate")
        self.cards["hash"].config(text=display_metric(metric,v.stale),fg=YELLOW if v.stale else GREEN if metric.present else MUTED)
        for key in ("difficulty","height","reward","peers"):
            self.cards[key].config(text=ND,fg=MUTED)
        # Solo etiquetas verificadas; nunca altura de "registro" como altura de nodo.
        self.cards["height"].config(text=self._value("NODOS","altura actual","altura full","Productor · altura full"))
        self.cards["peers"].config(text=self._value("NODOS","P2P actual","peers","Productor · peers"))
        self.cards["difficulty"].config(text=self._value("SOAT","dificultad actual","difficulty"))
        self.cards["reward"].config(text=self._value("EMISION","recompensa del bloque","recompensa confirmada"))
        for key,widget in self.status_rows.items():
            src=v.src(key)
            value="DATOS ANTIGUOS" if v.stale and src.status=="OK" else src.status
            widget.config(text=key+"  ·  "+value,
                          fg=RED if value in ("DESCONECTADO","DATOS ANTIGUOS") else GREEN if value=="OK" else YELLOW)
        updates={
            "GPU":{"Temperatura":("temp edge","temperatura","temp"),"Hotspot":("temp junction","hotspot"),
                   "Memoria":("temp memoria","temp memoria GPU"),"Consumo":("potencia","potencia PPT"),
                   "Ventilador":("ventilador","ventilador RPM"),"Uso GPU":("uso gpu","gpu_busy_percent")},
            "NODOS":{"Productor":("Productor · estado","Productor · altura full"),
                     "Receptor":("Receptor · estado","Receptor · altura full"),
                     "Altura":("altura actual","altura full"),"Bloques confirmados":("bloques confirmados por ambos nodos","bloques confirmados")},
            "SOAT":{"Hashrate":("hashrate","MH/s actuales","rate"),
                    "Aceptadas SOAT":("shares acc","soluciones aceptadas","accepted"),
                    "Rechazadas SOAT":("shares rej","soluciones rechazadas","rejected"),
                    "Nonces":("nonces",), "Backend":("backend",)} }
        for section, mapping in updates.items():
            for label, names in mapping.items():
                self.rows[section][label].config(text=self._value(section,*names))
        if v.error and v.error!=old.error:
            self._event("Fuente JSON: " + v.error)
        if v.stale and not old.stale:
            self._event("Registro desactualizado. No se afirma mineria activa")
        if not v.stale and metric.present and metric.number is not None:
            # Nunca mezclar MH/s con otra unidad en el grafico.
            unit_match = re.match(r"^[+-]?\d+(?:[.,]\d+)?\s+(.+)$",metric.text)
            unit = safe(unit_match.group(1),20) if unit_match else ""
            if unit:
                if self.rate_unit and unit != self.rate_unit:
                    self.history.clear()
                self.rate_unit = unit
                self.history.append(metric.number)
        self.paint_chart()
        self.root.after(self.interval_ms,self.tick)

    def paint_chart(self):
        c=self.chart
        if not c.winfo_exists():
            return
        c.delete("all")
        w,h=max(60,c.winfo_width()),max(50,c.winfo_height())
        for t in range(1,5):
            y=15+(h-35)*t/5
            c.create_line(12,y,w-12,y,fill=BORDER)
        data=list(self.history)
        if len(data)<2:
            c.create_text(w/2,h/2,text="Sin historial suficiente (N/D)",fill=MUTED,
                          font=("DejaVu Sans",11))
            return
        low,high=min(data),max(data)
        if low==high:
            low-=max(1,abs(high)*0.1)
            high+=max(1,abs(high)*0.1)
        points=[]
        for i,x in enumerate(data):
            px=15+(w-30)*i/max(1,len(data)-1)
            py=h-18-(h-35)*(x-low)/(high-low)
            points.extend([px,py])
        if len(points)>=4:
            c.create_line(*points,fill=GREEN,width=2,smooth=False)
        c.create_text(15,6,anchor="nw",text="Muestras observadas · "+(self.rate_unit or "unidad N/D"),fill=MUTED,font=("DejaVu Sans",9))