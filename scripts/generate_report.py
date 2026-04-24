import json
import sys
from datetime import datetime

INPUT_FILE = "semgrep-results.json"
OUTPUT_FILE = "semgrep-report.html"

SEVERITY_META = {
    "ERROR":   {"label": "HIGH",   "color": "#e53e3e", "bg": "#fff5f5", "icon": "🔴"},
    "WARNING": {"label": "MEDIUM", "color": "#d69e2e", "bg": "#fffff0", "icon": "🟡"},
    "INFO":    {"label": "LOW",    "color": "#3182ce", "bg": "#ebf8ff", "icon": "🔵"},
}

def load_results(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] No se encontró {path}")
        sys.exit(1)

def severity_meta(sev):
    return SEVERITY_META.get(sev, {"label": sev, "color": "#718096", "bg": "#f7fafc", "icon": "⚪"})

def build_html(data):
    results  = data.get("results", [])
    errors   = data.get("errors", [])
    now      = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    for r in results:
        sev = r.get("extra", {}).get("severity", "INFO")
        counts[sev] = counts.get(sev, 0) + 1

    total = len(results)

    # ── hallazgos HTML ──────────────────────────────────────────────
    findings_html = ""
    if not results:
        findings_html = """
        <div style="text-align:center;padding:60px 20px;color:#48bb78;">
            <div style="font-size:64px;">✅</div>
            <h2 style="margin-top:16px;color:#2f855a;">Sin hallazgos detectados</h2>
            <p style="color:#718096;">Semgrep no encontró vulnerabilidades en el código analizado.</p>
        </div>"""
    else:
        for i, r in enumerate(results):
            sev  = r.get("extra", {}).get("severity", "INFO")
            meta = severity_meta(sev)
            msg  = r.get("extra", {}).get("message", "Sin descripción")
            path = r.get("path", "")
            line = r.get("start", {}).get("line", "?")
            rule = r.get("check_id", "")
            snippet = r.get("extra", {}).get("lines", "").strip()
            cwe_tags = r.get("extra", {}).get("metadata", {}).get("cwe", [])
            if isinstance(cwe_tags, str):
                cwe_tags = [cwe_tags]
            cwe_html = "".join(
                f'<span style="background:#ebf8ff;color:#2b6cb0;border-radius:4px;'
                f'padding:2px 8px;font-size:12px;margin-right:4px;">{c}</span>'
                for c in cwe_tags
            )
            snippet_html = (
                f'<pre style="background:#1a202c;color:#e2e8f0;padding:16px;'
                f'border-radius:8px;overflow-x:auto;font-size:13px;'
                f'margin-top:12px;">{snippet}</pre>'
                if snippet else ""
            )

            findings_html += f"""
            <div style="border:1px solid #e2e8f0;border-left:4px solid {meta['color']};
                        border-radius:8px;padding:20px;margin-bottom:16px;
                        background:{meta['bg']};">
                <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
                    <div style="display:flex;align-items:center;gap:10px;">
                        <span style="font-size:20px;">{meta['icon']}</span>
                        <span style="background:{meta['color']};color:white;padding:2px 10px;
                                     border-radius:12px;font-size:12px;font-weight:700;">
                            {meta['label']}
                        </span>
                        <span style="font-weight:600;color:#2d3748;">Hallazgo #{i+1}</span>
                    </div>
                    <span style="font-size:12px;color:#718096;font-family:monospace;">
                        {path}:{line}
                    </span>
                </div>
                <p style="margin:12px 0 8px;color:#4a5568;">{msg}</p>
                <div style="margin-bottom:8px;">
                    <span style="font-size:12px;color:#718096;">Regla: </span>
                    <code style="font-size:12px;background:#edf2f7;padding:2px 6px;
                                 border-radius:4px;color:#4a5568;">{rule}</code>
                </div>
                {f'<div style="margin-bottom:8px;">{cwe_html}</div>' if cwe_html else ""}
                {snippet_html}
            </div>"""

    # ── errores HTML ─────────────────────────────────────────────────
    errors_html = ""
    if errors:
        err_items = "".join(
            f'<li style="margin-bottom:6px;color:#742a2a;">{e.get("message","Error desconocido")}</li>'
            for e in errors
        )
        errors_html = f"""
        <div style="background:#fff5f5;border:1px solid #fc8181;border-radius:8px;
                    padding:16px;margin-bottom:24px;">
            <strong style="color:#c53030;">⚠️ Errores durante el análisis ({len(errors)})</strong>
            <ul style="margin:8px 0 0 16px;">{err_items}</ul>
        </div>"""

    # ── HTML completo ────────────────────────────────────────────────
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte SAST — Semgrep</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: #f7fafc;
            color: #2d3748;
            padding: 32px 16px;
        }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
            color: white;
            border-radius: 12px;
            padding: 32px;
            margin-bottom: 24px;
        }}
        .header h1 {{ font-size: 26px; margin-bottom: 6px; }}
        .header p  {{ color: #a0aec0; font-size: 14px; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .stat-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,.08);
            border-top: 4px solid var(--c);
        }}
        .stat-card .num  {{ font-size: 36px; font-weight: 800; color: var(--c); }}
        .stat-card .lbl  {{ font-size: 13px; color: #718096; margin-top: 4px; }}
        .section-title {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 16px;
            color: #1a202c;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }}
        .footer {{
            text-align: center;
            color: #a0aec0;
            font-size: 12px;
            margin-top: 32px;
            padding-top: 16px;
            border-top: 1px solid #e2e8f0;
        }}
    </style>
</head>
<body>
<div class="container">

    <div class="header">
        <h1>🔍 Reporte SAST — Semgrep</h1>
        <p>Generado el {now} &nbsp;|&nbsp; Pipeline DevSecOps</p>
    </div>

    <div class="stats">
        <div class="stat-card" style="--c:#4a5568;">
            <div class="num">{total}</div>
            <div class="lbl">Total hallazgos</div>
        </div>
        <div class="stat-card" style="--c:#e53e3e;">
            <div class="num">{counts.get('ERROR', 0)}</div>
            <div class="lbl">🔴 Alta criticidad</div>
        </div>
        <div class="stat-card" style="--c:#d69e2e;">
            <div class="num">{counts.get('WARNING', 0)}</div>
            <div class="lbl">🟡 Media criticidad</div>
        </div>
        <div class="stat-card" style="--c:#3182ce;">
            <div class="num">{counts.get('INFO', 0)}</div>
            <div class="lbl">🔵 Baja criticidad</div>
        </div>
    </div>

    {errors_html}

    <div class="section-title">Hallazgos detectados</div>
    {findings_html}

    <div class="footer">
        Generado automáticamente por el pipeline CI/CD &nbsp;·&nbsp; Semgrep SAST
    </div>

</div>
</body>
</html>"""

if __name__ == "__main__":
    data = load_results(INPUT_FILE)
    html = build_html(data)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Reporte generado: {OUTPUT_FILE}")
    results = data.get("results", [])
    print(f"   Total hallazgos: {len(results)}")
