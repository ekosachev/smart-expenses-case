from markdown_pdf import MarkdownPdf, Section


def convert_md_to_pdf(input_path: str, output_path: str):
    pdf = MarkdownPdf(toc_level=2)

    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    pdf.add_section(Section(md_content))

    pdf.save(output_path)
