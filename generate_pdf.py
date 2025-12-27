import subprocess
import os

def build_pdf(tex_file):
    tex_file = os.path.abspath(tex_file)
    output_dir = os.path.dirname(tex_file)

    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_file],
        cwd=output_dir,
        check=True
    )

    return tex_file.replace(".tex", ".pdf")
