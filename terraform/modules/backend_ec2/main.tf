# modules/backend_ec2/main.tf

############################
# Security Group
############################
resource "aws_security_group" "backend_sg" {
  name        = "${var.name_prefix}-backend-sg"
  description = "Allow inbound traffic only from frontend EC2 and mobile app"
  vpc_id      = var.vpc_id

  # Allow SSH only from Admin IP
  ingress {
    description = "Allow SSH from trusted IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_ip]
  }

  # Allow backend requests only from Frontend EC2
  ingress {
    description = "Allow backend API access from Frontend"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    security_groups = [var.frontend_sg_id]
  }

  # Allow backend requests from NGINX
  ingress {
    description     = "Allow backend API access from NGINX"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [var.nginx_sg_id]
  }

  # Allow backend API access from mobile clients (modify this for security)
  ingress {
    description = "Allow backend API access from Mobile App"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = var.mobile_cidr_blocks  # Restrict to known mobile networks if possible
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.name_prefix}-backend-sg"
  }
}


data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-ebs"]
  }
}

############################
# EC2 Instance
############################
resource "aws_instance" "backend_ec2" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  credit_specification {
    cpu_credits = "unlimited"
  }
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.backend_sg.id]
  key_name               = var.key_pair_name
  associate_public_ip_address = false
  iam_instance_profile = aws_iam_instance_profile.backend_instance_profile.name

  user_data = <<-EOF
    #!/bin/bash
    # Update OS
    yum update -y

    # Install Docker
    amazon-linux-extras install docker -y
    service docker start
    usermod -aG docker ec2-user

    # Install Git
    yum install -y git

    # Clone Repo and Build Docker Image
    cd /home/ec2-user
    git clone -b ${var.repo_branch} ${var.repo_url} repo
    cd repo
    cd backend

    echo "DB_HOST=${var.db_host}" >> .env
    echo "DB_PORT=${var.db_port}" >> .env
    echo "DB_NAME=${var.db_name}" >> .env
    echo "DB_USER=${var.db_user}" >> .env
    echo "DB_PASS=${var.db_pass}" >> .env
    echo "DJANGO_SECRET_KEY=${var.dj_secret_key}" >> .env
    echo "STRIPE_SECRET_KEY=${var.stripe_secret_key}" >> .env
    echo "FIREBASE_CREDENTIALS_JSON=${var.firebase_credentials_json}" >> .env
    echo "GOOGLE_PLACES_API_KEY=${var.google_places_api_key}" >> .env
    echo "S3_BUCKET_NAME=${var.s3_bucket_name}" >> .env
    echo "ENVIRONMENT=production" >> .env

    # Build Docker image from Dockerfile in your backend folder
    docker build -t backend-image .

    # Run container on port 8000, passing .env as environment variables
    docker run -d -p 8000:8000 --env-file .env backend-image
  EOF

  tags = {
    Name = "${var.name_prefix}-backend-ec2"
  }
}

resource "aws_iam_instance_profile" "backend_instance_profile" {
  name = "${var.name_prefix}-backend-instance-profile"
  role = aws_iam_role.backend_instance_role.name
}

resource "aws_iam_role" "backend_instance_role" {
  name = "${var.name_prefix}-backend-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "backend_s3_policy" {
  name = "${var.name_prefix}-backend-s3-policy"
  role = aws_iam_role.backend_instance_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject"
        ],
        Resource = "arn:aws:s3:::${var.s3_bucket_name}/*"
      }
    ]
  })
}
