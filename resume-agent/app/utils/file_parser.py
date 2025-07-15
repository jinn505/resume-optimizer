import fitz

def extract_text_from_pdf_file(upload_file) -> str:
    file_bytes = upload_file.file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

async def load_jd(upload_file):
    content = await upload_file.read()
    return content.decode()

