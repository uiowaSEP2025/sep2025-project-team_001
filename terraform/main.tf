########################################
# Terraform & Provider Configuration
########################################
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.region
}

########################################
# Networking Resources
########################################

# Public Subnets
resource "aws_subnet" "public_subnet_a" {
  vpc_id                  = var.vpc_id
  cidr_block              = "172.31.80.0/20"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "PublicSubnet1A"
  }
}

resource "aws_subnet" "public_subnet_b" {
  vpc_id                  = var.vpc_id
  cidr_block              = "172.31.96.0/20"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "PublicSubnet1B"
  }
}

# Private Subnets (for your EC2 and RDS instances)
resource "aws_subnet" "private_subnet_frontend" {
  vpc_id                  = var.vpc_id
  cidr_block              = "172.31.144.0/20"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = false

  tags = {
    Name = "PrivateSubnetFrontend"
  }
}

resource "aws_subnet" "private_subnet_backend" {
  vpc_id                  = var.vpc_id
  cidr_block              = "172.31.112.0/20"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = false

  tags = {
    Name = "PrivateSubnetBackend"
  }
}

resource "aws_subnet" "private_subnet_rds_1" {
  vpc_id                  = var.vpc_id
  cidr_block              = "172.31.128.0/20"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = false

  tags = {
    Name = "PrivateSubnetRDS1"
  }
}

resource "aws_subnet" "private_subnet_rds_2" {
  vpc_id                  = var.vpc_id
  cidr_block              = "172.31.160.0/20"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = false

  tags = {
    Name = "PrivateSubnetRDS2"
  }
}

# NAT Gateway for outbound connectivity from private subnets
resource "aws_eip" "nat" {
  vpc = true
}

resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_subnet_a.id

  tags = {
    Name = "NAT-Gateway"
  }
}

# Route Tables

## Public Route Table Associations
resource "aws_route_table_association" "public_rta_a" {
  route_table_id = var.rtb_id
  subnet_id      = aws_subnet.public_subnet_a.id
}

resource "aws_route_table_association" "public_rta_b" {
  route_table_id = var.rtb_id
  subnet_id      = aws_subnet.public_subnet_b.id
}

## Private Route Table
resource "aws_route_table" "private_route_table" {
  vpc_id = var.vpc_id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway.id
  }

  tags = {
    Name = "PrivateRouteTable"
  }
}

resource "aws_route_table_association" "private_backend" {
  subnet_id      = aws_subnet.private_subnet_backend.id
  route_table_id = aws_route_table.private_route_table.id
}

resource "aws_route_table_association" "private_frontend" {
  subnet_id      = aws_subnet.private_subnet_frontend.id
  route_table_id = aws_route_table.private_route_table.id
}

resource "aws_route_table_association" "private_rds_1" {
  subnet_id      = aws_subnet.private_subnet_rds_1.id
  route_table_id = aws_route_table.private_route_table.id
}

resource "aws_route_table_association" "private_rds_2" {
  subnet_id      = aws_subnet.private_subnet_rds_2.id
  route_table_id = aws_route_table.private_route_table.id
}

########################################
# Modules
########################################

# RDS Module
module "rds" {
  source = "./modules/rds"

  vpc_id      = var.vpc_id
  subnet_ids  = [aws_subnet.private_subnet_rds_1.id, aws_subnet.private_subnet_rds_2.id]

  db_identifier = "postgres-db"
  db_name       = "TestDatabase"
  db_username   = "TestUser"
  db_password   = var.db_password

  publicly_accessible   = false
  backend_sg_id         = module.backend_ec2.backend_sg_id
}

# Backend EC2 Module
module "backend_ec2" {
  source       = "./modules/backend_ec2"
  name_prefix  = "streamlinebars"
  vpc_id       = var.vpc_id
  subnet_id    = aws_subnet.private_subnet_backend.id
  key_pair_name = var.key_pair_name

  db_host       = module.rds.db_endpoint
  db_port       = module.rds.db_port
  db_name       = "TestDatabase"
  db_user       = "TestUser"
  db_pass       = var.db_password
  dj_secret_key = "mysecretkey123"
  stripe_secret_key = "sk_test_51RAFr02cTgsJM4b1zq9w4tYcXuLKqwlvMGwEvW354FGgtknjwwV5OQgT5oLm1hfbGyZzecZn0r0kdfzr9ArKtwBW00uvzbCTbA"
  s3_bucket_name = module.s3_images.bucket_name

  repo_url            = var.repo_url
  repo_branch         = var.repo_branch
  frontend_sg_id      = module.frontend_ec2.frontend_sg_id
  nginx_sg_id         = module.nginx_ec2.nginx_sg_id
  mobile_cidr_blocks  = var.mobile_cidr_blocks
  admin_ip            = var.admin_ip
}

# Frontend EC2 Module
module "frontend_ec2" {
  source         = "./modules/frontend_ec2"
  name_prefix    = "streamlinebars"
  vpc_id         = var.vpc_id
  subnet_id      = aws_subnet.private_subnet_frontend.id
  key_pair_name  = var.key_pair_name
  instance_type  = "t3.micro"

  repo_url    = var.repo_url
  repo_branch = var.repo_branch

  nginx_sg_id = module.nginx_ec2.nginx_sg_id
}

module "nginx_ec2" {
  source         = "./modules/nginx_ec2"
  vpc_id         = var.vpc_id
  subnet_id      = aws_subnet.public_subnet_a.id
  key_pair_name  = var.key_pair_name
  instance_type  = "t3.micro"
  name_prefix    = "streamlinebars"
  domain_name    = "streamlinebars.com"

  frontend_target = module.frontend_ec2.private_ip
  backend_target  = module.backend_ec2.private_ip
}

module "s3_images" {
  source      = "./modules/s3_images"
  name_prefix = "streamlinebars"
}

########################################
# DNS & Certificate
########################################

# Private Route53 Zone for backend API
resource "aws_route53_zone" "private_api" {
  name = "api.streamlinebars.com"
  vpc {
    vpc_id = var.vpc_id
  }
}

resource "aws_route53_record" "backend_private_dns" {
  zone_id = aws_route53_zone.private_api.zone_id
  name    = "api.streamlinebars.com"
  type    = "A"
  ttl     = 300
  records = [module.backend_ec2.private_ip]
}

# Public Route53 Record for frontend
resource "aws_route53_record" "frontend" {
  zone_id = var.route53_zone_id
  name    = "streamlinebars.com"
  type    = "A"
  ttl     = 300
  records = [module.nginx_ec2.public_ip]
}

# ACM Certificate for your domains
resource "aws_acm_certificate" "frontend_cert" {
  domain_name               = "streamlinebars.com"
  subject_alternative_names = ["api.streamlinebars.com"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}
