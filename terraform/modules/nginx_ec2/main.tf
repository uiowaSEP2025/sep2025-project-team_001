# modules/nginx_ec2/main.tf

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners = ["amazon"]

  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-x86_64-ebs"]
  }
}

resource "aws_security_group" "nginx_sg" {
  name        = "${var.name_prefix}-nginx-sg"
  description = "Allow HTTP traffic to NGINX reverse proxy"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS
  ingress {
    description = "Allow HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow SSH from trusted IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_ip]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "nginx" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  associate_public_ip_address = true
  key_name                    = var.key_pair_name
  vpc_security_group_ids      = [aws_security_group.nginx_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    set -xe

    # 1) Install updates, NGINX, certbot
    yum update -y
    amazon-linux-extras install nginx1 epel -y
    yum install -y certbot

    # 2) Start and then stop NGINX (so it creates default dirs)
    systemctl start nginx
    systemctl enable nginx
    systemctl stop nginx

    # 3) Obtain the SSL certificate (standalone mode uses port 80)
    certbot certonly --standalone -n --agree-tos \
      --email ardusercole@gmail.com \
      -d ${var.domain_name}

    # 4) Create an NGINX config for HTTP -> HTTPS and an HTTPS server
    cat <<EOT > /etc/nginx/conf.d/default.conf
    # Redirect all HTTP to HTTPS
    server {
      listen 80;
      server_name ${var.domain_name};
      return 301 https://\$host\$request_uri;
    }

    # HTTPS server
    server {
      listen 443 ssl;
      server_name ${var.domain_name};

      # SSL certificate from certbot
      ssl_certificate /etc/letsencrypt/live/${var.domain_name}/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/${var.domain_name}/privkey.pem;

      # Proxy to Frontend
      location / {
        proxy_pass http://${var.frontend_target}:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
      }

      # Proxy to Backend
      location /api/ {
        proxy_pass http://${var.backend_target}:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
      }
    }
    EOT

    # 5) Restart NGINX with SSL
    systemctl start nginx
    systemctl enable nginx
  EOF

  tags = {
    Name = "${var.name_prefix}-nginx"
  }
}
