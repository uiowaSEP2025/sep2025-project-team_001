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

resource "aws_s3_bucket_public_access_block" "allow_public" {
  bucket = aws_s3_bucket.images.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "public_read" {
  bucket = aws_s3_bucket.images.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "PublicReadGetObject",
        Effect    = "Allow",
        Principal = "*",
        Action    = "s3:GetObject",
        Resource  = "arn:aws:s3:::${aws_s3_bucket.images.bucket}/*"
      }
    ]
  })
  depends_on = [aws_s3_bucket_public_access_block.allow_public]
}