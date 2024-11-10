import os
import re
import markdown2
import pdfkit
from pyhtml2pdf import converter

import markdown2
import os

def handle_line_breaks(markdown_content):
    # Replace any newlines or carriage returns with HTML <br> tag for proper line breaks
    return markdown_content.replace('\n', '  \n')

# Function to read markdown file content
def read_markdown(md_file_path):
    with open(md_file_path, 'r') as file:
        markdown_content = file.read()
    return markdown_content

# Function to split the content into sections
def split_markdown_content(markdown_content):
    title = markdown_content.split('\n')[0]
    sub_title = markdown_content.split('\n')[1]
    markdown_content = '\n'.join(markdown_content.split('\n')[2:])
    split_content = markdown_content.split("---\n\n")
    return title, sub_title, split_content

# Function to categorize sections into columns
def categorize_sections(split_content):
    main_sections = []
    left_column_sections = ['\n']
    right_column_sections = ['\n']

    for section in split_content:
        if "SKILLS" in section or "CERTIFICATES" in section  or "EDUCATION" in section:
            left_column_sections.append(handle_line_breaks(section))
        elif "WORK EXPERIENCE" in section or "VOLUNTEER EXPERIENCE" in section:
            right_column_sections.append(handle_line_breaks(section))
        elif "SUMMARY" in section:
            main_sections.append(section)
    
    right_column_sections.append('\n')

    return main_sections, left_column_sections, right_column_sections

# Function to convert sections into HTML
def convert_to_html(title, sub_title, main_sections, left_column_sections, right_column_sections, pdf_title):
    # Converting sections to HTML
    title_content = markdown2.markdown(title)
    sub_title_content = markdown2.markdown(sub_title)
    main_section_html = markdown2.markdown("---\n\n".join(main_sections))
    left_column_html = markdown2.markdown("---\n\n".join(left_column_sections))
    right_column_html = markdown2.markdown("---\n\n".join(right_column_sections))

    # Updated CSS for the resume layout
    with open("./design/two_column_format.css", "r") as css_file:
        custom_css = css_file.read()

    # Create the full HTML content with a title
    html_content = f"""
        <html>
        <head>
            <title>{pdf_title}</title>
            <style>{custom_css}</style>
        </head>
        <body>
            <div class="header">
                {title_content}<br>
                {sub_title_content}
            </div>
            <div>
                {main_section_html}
            </div>
            <div class="container">
                <div class="left-column">
                    {left_column_html}
                </div>
                <div class="right-column">
                    {right_column_html}
                </div>
            </div>
        </body>
        </html>
    """
    return html_content

# Function to write HTML content to a temporary file
def write_html_to_file(html_content, temp_html_file):
    with open(temp_html_file, 'w') as file:
        file.write(html_content)

# Function to convert HTML to PDF
def convert_html_to_pdf(html_file, pdf_file):
    path = os.path.abspath(html_file)
    converter.convert(f'file:///{path}', pdf_file)  # call to an external tool
    print(f"Converted {html_file} to {pdf_file}")

# Main function to process markdown and generate PDF
def markdown_to_pdf(md_file_path, pdf_file_path):
    # Step 1: Read markdown content
    markdown_content = read_markdown(md_file_path)

    # Step 2: Split markdown into sections
    title, sub_title, split_content = split_markdown_content(markdown_content)

    # Step 3: Categorize sections into main, left, and right columns
    main_sections, left_column_sections, right_column_sections = categorize_sections(split_content)

    # Step 4: Convert content into HTML
    pdf_title = os.path.basename(pdf_file_path).replace(".pdf", "")  # Use the PDF filename as HTML title
    html_content = convert_to_html(title, sub_title, main_sections, left_column_sections, right_column_sections, pdf_title)

    # Step 5: Write HTML to a temporary file
    temp_html_file = 'temp_resume.html'
    write_html_to_file(html_content, temp_html_file)

    # Step 6: Convert the HTML file to a PDF
    convert_html_to_pdf(temp_html_file, pdf_file_path)

    # Step 7: Remove the temporary HTML file
    os.remove(temp_html_file)
    print("PDF successfully generated with two-column layout!")

def main():
    markdown_file = './content/sample_resume_markdown.txt'
    pdf_file = './files/Sample_Resume.pdf'
    markdown_to_pdf(markdown_file, pdf_file)

if __name__=="__main__":
    main()