# modules/backend_ec2/main.tf

############################
# Security Group
############################
resource "aws_security_group" "backend_sg" {
  name        = "${var.name_prefix}-backend-sg"
  description = "Allow inbound traffic only from frontend EC2 and mobile app"
  vpc_id      = var.vpc_id

  # Allow SSH only from your IP (for admin access)
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
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.backend_sg.id]
  key_name               = var.key_pair_name
  associate_public_ip_address = false

  user_data = <<-EOF
    #!/bin/bash
    # Update OS
    yum update -y

    # Install Docker
    amazon-linux-extras install docker -y
    service docker start
    usermod -aG docker ec2-user

    # Install Git if you need to clone your repo
    yum install -y git

    # Clone your backend code
    cd /home/ec2-user
    git clone -b ${var.repo_branch} ${var.repo_url} repo
    cd repo
    cd backend

    # If you need environment variables for RDS, create an .env or pass them at runtime
    echo "DB_HOST=${var.db_host}" >> .env
    echo "DB_PORT=${var.db_port}" >> .env
    echo "DB_NAME=${var.db_name}" >> .env
    echo "DB_USER=${var.db_user}" >> .env
    echo "DB_PASS=${var.db_pass}" >> .env
    echo "DJANGO_SECRET_KEY=${var.dj_secret_key}" >> .env

    # Build Docker image from Dockerfile in your backend folder
    docker build -t backend-image .

    # Run container on port 8000, passing .env as environment variables
    docker run -d -p 8000:8000 --env-file .env backend-image
  EOF

  tags = {
    Name = "${var.name_prefix}-backend-ec2"
  }
}
