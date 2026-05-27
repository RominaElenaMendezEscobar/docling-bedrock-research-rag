"""
Pre-download Docling models during Docker build.

This script initializes a DocumentConverter which triggers the automatic
download of all required models (layout detection, table structure, etc.)
to the specified artifacts path.

This is necessary because AWS Lambda has a read-only filesystem, so models
must be downloaded during the Docker build phase, not at runtime.
"""

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from pathlib import Path


def main():
    artifacts_path = Path("/opt/docling-models")
    print(f"Downloading Docling models to {artifacts_path}...")

    # Configure pipeline with artifacts path
    pipeline_options = PdfPipelineOptions(
        artifacts_path=artifacts_path,
        do_ocr=False  # Disable OCR to avoid RapidOCR model downloads
    )

    # Initialize converter - this triggers model downloads
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options
            )
        }
    )
    
    print("✓ Models downloaded successfully")


if __name__ == "__main__":
    main()