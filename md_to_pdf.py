from markdown_pdf import MarkdownPdf, Section

pdf = MarkdownPdf(toc_level=2)

with open("expenses_analysis.md", "r", encoding="utf-8") as f:
    md_content = f.read()

pdf.add_section(Section(md_content))

pdf.save("guide.pdf")