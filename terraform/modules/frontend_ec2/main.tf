# modules/frontend_ec2/main.tf

############################
# Security Group for Frontend
############################
resource "aws_security_group" "frontend_sg" {
  name        = "${var.name_prefix}-frontend-sg"
  description = "Allow HTTPS traffic and restrict SSH access"
  vpc_id      = var.vpc_id

  # Allow HTTPS (port 443) from anywhere (for secure frontend access)
  ingress {
    description = "Allow HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Restrict SSH to only your IP
  ingress {
    description = "Allow SSH from trusted IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_ip]
  }

  # Allow outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.name_prefix}-frontend-sg"
  }
}


############################
# Data Source for Amazon Linux AMI
############################
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-ebs"]
  }
}

############################
# EC2 Instance for Frontend
############################
resource "aws_instance" "frontend_ec2" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.frontend_sg.id]
  key_name                    = var.key_pair_name
  associate_public_ip_address = true

  user_data = <<-EOF
    #!/bin/bash
    # Update OS and install required packages
    yum update -y
    amazon-linux-extras install docker -y
    service docker start
    usermod -aG docker ec2-user
    yum install -y git

    # Clone the frontend repository
    cd /home/ec2-user
    git clone -b ${var.repo_branch} ${var.repo_url} repo
    cd repo
    cd web_app

    # Create .env file for frontend environment variables (e.g., backend API URL)
    echo "REACT_APP_API_URL=${var.backend_api_url}" > .env

    # Build the Docker image for the frontend
    docker build -t frontend-image .

    # Run the frontend container, mapping container port 3000 to host port 3000
    docker run -d -p 3000:3000 --env-file .env frontend-image
  EOF

  tags = {
    Name = "${var.name_prefix}-frontend-ec2"
  }
}
