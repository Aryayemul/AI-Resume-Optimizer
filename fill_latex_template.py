# def fill_latex_template(template_path, context, output_path):
#     with open(template_path, "r", encoding="utf-8") as f:
#         content = f.read()

#     for key, value in context.items():
         
#      if not key.startswith("HAS_"):
#         content = content.replace(f"\\{key}", value)

#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write(content)
def fill_latex_template(template_path, context, output_path):
    with open(template_path, "r", encoding="utf-8") as f:
        tex = f.read()

    for key, value in context.items():
        tex = tex.replace(f"\\{key}", value)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tex)




