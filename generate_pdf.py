import os
import subprocess
import markdown_it

md_path = r"C:\Users\Acer\Documents\aivi_ai_engineering_challenge\AIVI_AI_ENGINEERING_REPORT_CONSOLIDATED.md"
html_path = r"C:\Users\Acer\Documents\aivi_ai_engineering_challenge\report_styled.html"
pdf_path = r"C:\Users\Acer\Documents\aivi_ai_engineering_challenge\AIVI_AI_ENGINEERING_REPORT_CONSOLIDATED.pdf"

with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

# Enable table support in markdown_it
md = markdown_it.MarkdownIt().enable("table")
body_html = md.render(md_content)

styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AIVI Intelligence — AI Engineering Challenge Report</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {{
      content: counter(page) " / " counter(pages);
      font-size: 9pt;
      color: #718096;
    }}
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1a202c;
    background-color: #ffffff;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }}
  .header-banner {{
    border-bottom: 2px solid #3182ce;
    padding-bottom: 12px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }}
  .brand-title {{
    font-size: 16pt;
    font-weight: 800;
    color: #2b6cb0;
    letter-spacing: 0.5px;
    margin: 0 0 4px 0;
    text-transform: uppercase;
  }}
  .brand-subtitle {{
    font-size: 8.5pt;
    font-weight: 600;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin: 0;
  }}
  .badge-container {{
    text-align: right;
  }}
  .badge {{
    display: inline-block;
    padding: 3px 8px;
    font-size: 8pt;
    font-weight: 700;
    border-radius: 4px;
    margin-left: 4px;
    text-transform: uppercase;
  }}
  .badge-blue {{
    background-color: #ebf8ff;
    color: #2b6cb0;
    border: 1px solid #bee3f8;
  }}
  .badge-green {{
    background-color: #f0fff4;
    color: #276749;
    border: 1px solid #c6f6d5;
  }}
  .badge-dark {{
    background-color: #edf2f7;
    color: #2d3748;
    border: 1px solid #e2e8f0;
  }}
  h1 {{
    font-size: 15pt;
    color: #1a365d;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 6px;
    margin-top: 22px;
    margin-bottom: 12px;
    page-break-after: avoid;
  }}
  h2 {{
    font-size: 12pt;
    color: #2b6cb0;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 10.5pt;
    color: #2d3748;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}
  p, li {{
    color: #2d3748;
    font-size: 9.5pt;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #cbd5e0;
    padding: 7px 10px;
    text-align: left;
  }}
  th {{
    background-color: #edf2f7;
    color: #1a202c;
    font-weight: 700;
  }}
  tr:nth-child(even) {{
    background-color: #f7fafc;
  }}
  code {{
    font-family: "Consolas", "Courier New", monospace;
    font-size: 8.5pt;
    background-color: #edf2f7;
    padding: 2px 4px;
    border-radius: 3px;
    color: #805ad5;
  }}
  pre {{
    background-color: #1a202c;
    color: #edf2f7;
    padding: 10px 14px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 8.5pt;
    line-height: 1.45;
    page-break-inside: avoid;
    margin: 10px 0;
  }}
  pre code {{
    background-color: transparent;
    color: #edf2f7;
    padding: 0;
    border-radius: 0;
  }}
  hr {{
    border: 0;
    height: 1px;
    background: #e2e8f0;
    margin: 18px 0;
  }}
  ul, ol {{
    margin-top: 6px;
    margin-bottom: 10px;
    padding-left: 20px;
  }}
  li {{
    margin-bottom: 4px;
  }}
  .meta-box {{
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #3182ce;
    padding: 10px 14px;
    border-radius: 4px;
    margin-bottom: 16px;
    font-size: 9pt;
  }}
</style>
</head>
<body>
<div class="header-banner">
  <div>
    <div class="brand-title">AIVI Intelligence</div>
    <div class="brand-subtitle">Sovereign AI Software Platforms • Bharat-First Architecture</div>
  </div>
  <div class="badge-container">
    <span class="badge badge-green">✔ DPIIT #DIPP271794</span>
    <span class="badge badge-blue">AI Engineering Challenge</span>
    <span class="badge badge-dark">48h SLA</span>
  </div>
</div>

<div class="meta-box">
  <strong>Candidate Name:</strong> Nihal Hegde &nbsp;|&nbsp; 
  <strong>Role Evaluated:</strong> AI Engineer Intern &nbsp;|&nbsp;
  <strong>Repository:</strong> <a href="https://github.com/nihalhegde12/aivi-ai-engineering-challenge">github.com/nihalhegde12/aivi-ai-engineering-challenge</a>
</div>

{body_html}

<div style="margin-top: 30px; padding-top: 12px; border-top: 1px solid #e2e8f0; font-size: 8pt; color: #a0aec0; text-align: center;">
  AIVI Intelligence Private Limited • Talent Acquisition & Technical Evaluation • Confidential Assessment
</div>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(styled_html)

print("HTML generated successfully. Invoking Microsoft Edge for PDF rendering...")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    f"file:///{html_path.replace(os.sep, '/')}"
]

res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
    print(f"PDF generated successfully! Size: {os.path.getsize(pdf_path)} bytes at {pdf_path}")
else:
    print(f"Error generating PDF. Return code: {res.returncode}")
    print(f"Stderr: {res.stderr}")
