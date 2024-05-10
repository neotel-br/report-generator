from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
import json
import os
import PyPDF2

template_path = "templates"
output_folder = "results/"
# Modular templates
templates = [
    {
        "template_name": "cover.html",
        "output_file": output_folder + "cover.pdf",
        "style": True,
        "css_name": "static/css/cover.css",
        "data": True,
    },
    {
        "template_name": "content.html",
        "output_file": output_folder + "content.pdf",
        "style": True,
        "css_name": "static/css/style.css",
        "data": True,
    },
]
output_filename = "results/report.pdf"
data_file = "data.json"
merger = PyPDF2.PdfMerger()


def generate_pdf(template_path, data_file, templates):
    env = Environment(loader=FileSystemLoader(template_path))
    # print("Environment initialized.")
    with open(data_file, "r") as file:
        data = json.load(file)
    create_folder_output()
    for template in templates:
        template_name = template["template_name"]
        output_filename = template["output_file"]
        css_name = template["css_name"]
        template_file = env.get_template(template_name)
        if template["data"]:
            html = template_file.render(data=data)
        else:
            html = template_file.render()
        # print("Rendered html")
        # print(output_filename)
        if template["style"]:
            css = CSS(filename=css_name)

            HTML(string=html, base_url=template_path).write_pdf(
                target=output_filename,
                stylesheets=[
                    css,
                    "static/css/layout.css",
                ],
            )
        else:
            HTML(string=html, base_url=template_path).write_pdf(target=output_filename)
    # print("Generated template")
    # print(template)
    # print(template_name)
    # print("Template rendered successfully.")


def create_folder_output():
    folder_path = output_folder
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        print("Created folder:", folder_path)
    else:
        print("Folder exists:", folder_path)


def merge_pdf(templates, output_filename):
    # print("Merging:")
    # Create a PdfMerger object to merge the PDFs
    merger = PyPDF2.PdfMerger()
    for template in templates:
        # print(template["output_file"])
        merger.append(template["output_file"])
        # Write the merged PDF to the output file

    with open(output_filename, "wb") as output_file:
        merger.write(output_file)


if __name__ == "__main__":
    generate_pdf(template_path, data_file, templates)
    merge_pdf(templates, output_filename)
    print("PDF generated successfully.")
