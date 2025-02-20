########################################
# Security Group for EC2
########################################
resource "aws_security_group" "ec2_sg" {
  name        = "ec2-docker-sg"
  description = "Allow inbound traffic for SSH, HTTP, React(3000), Django(8000)"
  vpc_id      = var.vpc_id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "React dev port"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Django dev port"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ec2-docker-sg"
  }
}

########################################
# EC2 Instance
########################################
resource "aws_instance" "docker_ec2" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  # Pick the first public subnet for the EC2 instance
  subnet_id = var.public_subnet_ids[0]

  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  key_name                    = var.key_pair_name
  associate_public_ip_address = true

  # user_data installs Docker, Docker Compose, etc.
  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    amazon-linux-extras install docker -y
    service docker start
    usermod -aG docker ec2-user

    # Install Docker Compose v2
    curl -SL https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose

    # (Optional) If you want to pass RDS_ENDPOINT as an env variable, you can:
    echo "export RDS_ENDPOINT=${var.rds_endpoint}" >> /home/ec2-user/.bashrc

    # You can clone your repo or pull images from ECR here if you like.

    echo "EC2 module setup complete" > /home/ec2-user/setup.log
  EOF

  tags = {
    Name = "docker-compose-ec2"
  }
}
