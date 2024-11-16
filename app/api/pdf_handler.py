import os
from dotenv import load_dotenv
import boto3 # for S3
from botocore.exceptions import NoCredentialsError
import fitz  # PyMuPDF

# Load env
load_dotenv()

# Initialize S3 client
s3_client = boto3.client(
    's3',
    region_name=os.getenv("S3_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from a PDF file"""
    text = ""
    # Create a PDF document from bytes
    pdf_document = fitz.open("pdf", pdf_bytes)
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()
    return text

def upload_pdf_to_s3(file_data: bytes, filename: str) -> str:
    """Upload the PDF file to S3 and return the S3 public URL"""
    try:
        # Upload PDF to S3 bucket
        s3_client.put_object(
            Bucket=os.getenv("S3_BUCKET_NAME"),
            Key=f'pdfs/{filename}',  # Store in the 'pdfs' folder within the bucket
            Body=file_data,
            ContentType="application/pdf"
        )
        # Return the public URL of the uploaded file
        s3_url = f"https://{os.getenv('S3_BUCKET_NAME')}.s3.{os.getenv('S3_REGION')}.amazonaws.com/pdfs/{filename}"
        return s3_url
    except NoCredentialsError:
        raise Exception("AWS credentials not found")
    except Exception as e:
        raise Exception(f"Error uploading PDF to S3: {e}")
