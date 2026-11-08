"""Pruebas con datos SINTETICOS; jamas consultan SOAT ni sensores reales."""
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from syp_view import normalize, pick, safe
from syp_source import Reader
from syp_tui import render


class Tests(unittest.TestCase):
    def test_no_source(self):
        v=Reader().read()
        self.assertTrue(v.error)
        self.assertEqual(pick(v,"SOAT","hashrate").text,"N/D")

    def test_actual_numeric(self):
        snap={"sources":[{"name":"SOAT","status":"OK","fields":[{"label":"hashrate","value":"182.5 MH/s","data":182.5}]}]}
        v=normalize(snap,now=100)
        self.assertEqual(v.src("SOAT").status,"OK")
        self.assertEqual(pick(v,"SOAT","hashrate").text,"182.5 MH/s")
        self.assertIsNone(pick(v,"SOAT","altura").number)

    def test_stale(self):
        v=normalize({"sources":[]},now=999,file_mtime=1,stale_after=20)
        self.assertTrue(v.stale)

    def test_no_infer_blocks(self):
        snap={"sources":[{"name":"SOAT","status":"OK","fields":[{"label":"shares acc","value":"18","data":18}]}]}
        v=normalize(snap)
        self.assertEqual(pick(v,"NODOS","bloques confirmados").text,"N/D")

    def test_status_reject_unknown(self):
        v=normalize({"sources":[{"name":"SOAT","status":"minando","fields":[]}]})
        self.assertEqual(v.src("SOAT").status,"N/D")

    def test_sanitize_ansi(self):
        self.assertNotIn("\x1b",safe("hash\x1b]0;malicioso\x07\nvalor"))
        self.assertNotIn("\n",safe("hola\nresto"))

    def test_file_read(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/"synthetic.json"
            p.write_text(json.dumps({"sources":[]}),encoding="utf-8")
            self.assertFalse(Reader(str(p)).read().error)

    def test_file_size_limit(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/"synthetic.json"
            p.write_bytes(b"a"*(2*1024*1024+1))
            self.assertIn("2 MiB",Reader(str(p)).read().error)

    def test_tui_compact_and_wide(self):
        v=normalize({"sources":[{"name":"GPU","status":"OK","fields":[{"label":"potencia","value":"200 W","data":200}]}]})
        for width in (60,110):
            s=render(v,width,color=False)
            self.assertIn("200 W",s)
            self.assertIn("N/D",s)
            self.assertNotIn("\x1b",s)

    def test_gui_import_without_launch(self):
        try:
            from syp_gui import display_metric
        except ImportError:
            self.skipTest("tkinter no disponible")
        v=normalize({"sources":[]})
        self.assertEqual(display_metric(pick(v,"SOAT","hashrate"),False),"N/D")


if __name__=="__main__":
    unittest.main()

class NamesTests(unittest.TestCase):
    def test_guardian_with_accent(self):
        v=normalize({"sources":[{"name":"GUARDIÁN","status":"N/D","fields":[]}]})
        self.assertIn("GUARDIAN",v.sources)