import os
from urllib.parse import urlparse
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractOcrOptions
import boto3

s3 = boto3.client("s3")

def parse_s3_url(s3_url: str):
    parsed = urlparse(s3_url)
    bucket = parsed.netloc
    key = parsed.path.lstrip("/")
    return bucket, key

def handler(event, context):
    s3_url = event["s3_url"]
    input_bucket, input_key = parse_s3_url(s3_url)

    filename = os.path.basename(input_key)
    name_without_ext = os.path.splitext(filename)[0]

    local_pdf = f"/tmp/{filename}"
    local_md = f"/tmp/{name_without_ext}.md"

    # Descargar PDF desde S3
    s3.download_file(input_bucket, input_key, local_pdf)

    # Configurar pipeline SIN OCR
    # RapidOCR está instalado pero no se usa porque do_ocr=False
    pipeline_options = PdfPipelineOptions(do_ocr=False)

    # Crear converter
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options
            )
        }
    )

    # Convertir PDF a Markdown
    result = converter.convert(local_pdf)

    with open(local_md, "w", encoding="utf-8") as f:
        f.write(result.document.export_to_markdown())

    # Subir resultado a S3
    output_key = f"output/{name_without_ext}.md"

    s3.upload_file(
        local_md,
        input_bucket,
        output_key,
        ExtraArgs={"ContentType": "text/markdown"}
    )

    return {
        "status": "200",
        "input": s3_url,
        "output": f"s3://{input_bucket}/{output_key}"
    }