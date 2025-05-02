import os
import uuid
import base64
from pathlib import Path
from django.conf import settings
import boto3

# Check settings.py to decide whether to use S3 or local media
USE_S3 = getattr(settings, "USE_S3", False)
S3_BUCKET = getattr(settings, "S3_BUCKET_NAME", "")

if USE_S3:
    s3 = boto3.client("s3")


def save_image_from_base64(base64_str: str, folder: str, ref_id: int) -> str:
    if not base64_str:
        return ""

    # Parse out image type and decode data
    header, data = base64_str.split(",", 1) if "," in base64_str else ("", base64_str)
    ext = header.split("/")[1].split(";")[0] if "/" in header else "jpg"
    filename = f"{folder}/{ref_id}_{uuid.uuid4().hex}.{ext}"

    image_bytes = base64.b64decode(data)

    if USE_S3:
        # Upload to S3
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=filename,
            Body=image_bytes,
            ContentType=f"image/{ext}"
        )
        return f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
    else:
        # Save to local media/ folder
        path = Path("media") / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            f.write(image_bytes)
        return f"/media/{filename}"


def delete_s3_image(image_url: str):
    """
    Deletes an image from S3 if it exists and is from your bucket.
    """
    if not (USE_S3 and image_url and S3_BUCKET in image_url):
        return

    key = image_url.split(f"{S3_BUCKET}.s3.amazonaws.com/")[-1]
    try:
        s3.delete_object(Bucket=S3_BUCKET, Key=key)
    except Exception as e:
        print(f"[Warning] Failed to delete S3 image: {e}")
