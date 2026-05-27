FROM public.ecr.aws/lambda/python:3.12

# Install system dependencies
RUN dnf install -y gcc gcc-c++ poppler-utils mesa-libGL && dnf clean all

# Set environment variables for model caching
ENV DOCLING_MODELS_PATH=/opt/docling-models
ENV HF_HOME=/tmp
ENV TRANSFORMERS_CACHE=/tmp
ENV HF_HUB_CACHE=/tmp

# Install Python dependencies
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    "numpy<2.0" \
    boto3==1.35.76 \
    docling==2.66.0

# Copy and run model download script
COPY download_models.py /tmp/download_models.py
RUN mkdir -p /opt/docling-models && \
    python3.12 /tmp/download_models.py && \
    rm /tmp/download_models.py

# Clean up temporary files to reduce image size
RUN find /var/lang/lib/python3.12/site-packages -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /var/lang/lib/python3.12/site-packages -type f -name "*.pyc" -delete

# Copy Lambda function
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

CMD ["lambda_function.handler"]