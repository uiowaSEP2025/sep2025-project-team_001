resource "aws_s3_bucket" "images" {
  bucket        = "${var.name_prefix}-images"
  force_destroy = true
}

resource "aws_s3_bucket_cors_configuration" "cors" {
  bucket = aws_s3_bucket.images.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT"]
    allowed_origins = ["*"]
    max_age_seconds = 3000
  }
}
