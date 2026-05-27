import boto3
import json
from botocore.config import Config

s3 = boto3.client("s3")
lambda_client = boto3.client(               
    "lambda",
    config=Config(
        read_timeout=900,
        connect_timeout=10,
        retries={"max_attempts": 0}
    )
)

BUCKET = "docling-papers-tutorial"
DOCLING_LAMBDA = "docling-lambda" 

def lambda_handler(event, context):
    
    # 1. List PDFs en el bucket
    response = s3.list_objects_v2(
        Bucket=BUCKET
    )
    
    pdfs = [
        obj["Key"]
        for obj in response.get("Contents", [])
        if obj["Key"].endswith(".pdf")
    ]
    
    print(f"PDFs found: {len(pdfs)}")
    # 2. Invoke Lambda for each PDF
    results = []
    for pdf_key in pdfs:
        s3_url = f"s3://{BUCKET}/{pdf_key}"
        print(f"Procesando: {s3_url}")
        
        response = lambda_client.invoke(
            FunctionName=DOCLING_LAMBDA,
            InvocationType="RequestResponse",  
            Payload=json.dumps({"s3_url": s3_url})
        )
        
        result = json.loads(response["Payload"].read())
        results.append({
            "input": s3_url,
            "output": result.get("output"),
            "status": result.get("status")
        })
        print(f"✓ {pdf_key} → {result.get('output')}")
    
    return {
        "processed": len(results),
        "results": results
    }