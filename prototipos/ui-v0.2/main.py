"""Lanzador seguro para el prototipo visual de SYPminer."""
from __future__ import annotations

import argparse
import sys
import time

from syp_source import Reader
from syp_tui import render


def parser():
    p=argparse.ArgumentParser(description="SYPminer UI v0.2 · presentacion sin control minero")
    mode=p.add_mutually_exclusive_group()
    mode.add_argument("--gui",action="store_true",help="Interfaz de ventanas Tk")
    mode.add_argument("--terminal",action="store_true",help="Interfaz ANSI")
    src=p.add_mutually_exclusive_group()
    src.add_argument("--json-file",metavar="RUTA",help="Leer exportacion JSON")
    src.add_argument("--command",nargs=argparse.REMAINDER,help="Comando explicito que imprime JSON y termina, sin shell")
    p.add_argument("--cwd",help="Directorio de trabajo del comando JSON explicito")
    p.add_argument("--once",action="store_true",help="Una sola lectura en modo terminal")
    p.add_argument("--width",type=int,default=110)
    p.add_argument("--refresh",type=float,default=2.5)
    p.add_argument("--max-age",type=float,default=20.0,help="Antiguedad maxima de una lectura JSON")
    p.add_argument("--no-color",action="store_true")
    return p


def main(argv=None):
    args=parser().parse_args(argv)
    if not (0.5<=args.refresh<=60.0) or not (1<=args.max_age<=3600):
        parser().error("--refresh y --max-age fuera de rango")
    if args.command and args.command[0]=="--":
        args.command=args.command[1:]
    if args.command is not None and not args.command:
        parser().error("--command necesita un ejecutable explicito")
    reader=Reader(path=args.json_file,command=args.command,cwd=args.cwd,max_age_s=args.max_age)
    if not args.terminal:
        try:
            import tkinter as tk
            from syp_gui import MinerGUI
        except ImportError as ex:
            print("Tkinter no disponible: %s. Prueba --terminal."%ex,file=sys.stderr)
            return 2
        try:
            root=tk.Tk()
            MinerGUI(root,reader,int(args.refresh*1000))
            root.mainloop()
            return 0
        except tk.TclError as ex:
            print("La GUI necesita entorno grafico: %s. Prueba --terminal."%ex,file=sys.stderr)
            return 2
    if args.once:
        print(render(reader.read(),args.width,color=not args.no_color and sys.stdout.isatty()))
        return 0
    try:
        while True:
            frame=render(reader.read(),args.width,color=not args.no_color and sys.stdout.isatty())
            sys.stdout.write("\x1b[2J\x1b[H"+frame+"\n")
            sys.stdout.flush()
            time.sleep(args.refresh)
    except KeyboardInterrupt:
        print("\nMonitor detenido. No se ha detenido la mineria.")
        return 0

if __name__=="__main__":
    raise SystemExit(main())