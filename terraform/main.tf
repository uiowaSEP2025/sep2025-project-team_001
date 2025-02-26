# main.tf

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
# Public Subnets
########################################
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

########################################
# Private Subnets
########################################
resource "aws_subnet" "private_subnet_a" {
  vpc_id                  = var.vpc_id
  cidr_block              = "172.31.112.0/20"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = false

  tags = {
    Name = "PrivateSubnet1A"
  }
}

resource "aws_subnet" "private_subnet_b" {
  vpc_id                  = var.vpc_id
  cidr_block              = "172.31.128.0/20"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = false

  tags = {
    Name = "PrivateSubnet1B"
  }
}

resource "aws_route_table_association" "public_rta_a" {
  route_table_id = var.rtb_id
  subnet_id      = aws_subnet.public_subnet_a.id
}

resource "aws_route_table_association" "public_rta_b" {
  route_table_id = var.rtb_id
  subnet_id      = aws_subnet.public_subnet_b.id
}

########################################
# RDS Module
########################################
module "rds" {
  source = "./modules/rds"

  vpc_id      = var.vpc_id
  subnet_ids  = [aws_subnet.private_subnet_a.id, aws_subnet.private_subnet_b.id]

  db_identifier = "postgres-db"
  db_name       = "TestDatabase"
  db_username   = "TestUser"
  db_password   = var.db_password

  publicly_accessible = true
  allowed_cidr_blocks   = []

  backend_sg_id = module.backend_ec2.backend_sg_id
}

########################################
# Backend EC2 Module
########################################
module "backend_ec2" {
  source       = "./modules/backend_ec2"
  name_prefix  = "backend"
  vpc_id       = var.vpc_id
  subnet_id    = aws_subnet.public_subnet_a.id
  key_pair_name = var.key_pair_name

  db_host       = module.rds.db_endpoint
  db_port       = module.rds.db_port
  db_name       = "TestDatabase"
  db_user       = "TestUser"
  db_pass       = var.db_password
  dj_secret_key = "mysecretkey123"

  repo_url     = var.repo_url
  repo_branch  = var.repo_branch

  frontend_sg_id      = module.frontend_ec2.frontend_sg_id
  mobile_cidr_blocks  = var.mobile_cidr_blocks
  admin_ip            = var.admin_ip
}


########################################
# Frontend EC2 Module
########################################
module "frontend_ec2" {
  source         = "./modules/frontend_ec2"
  name_prefix    = "frontend"
  vpc_id         = var.vpc_id
  subnet_id      = aws_subnet.public_subnet_a.id
  key_pair_name  = var.key_pair_name
  instance_type  = "t3.micro"
  backend_api_url   = "http://api.streamlinebars.com:8000"

  repo_url = var.repo_url
  repo_branch = var.repo_branch
}

resource "aws_route53_record" "backend" {
  zone_id = var.route53_zone_id
  name    = "api.streamlinebars.com"
  type    = "A"
  ttl     = 300
  records = [module.backend_ec2.public_ip]
}

resource "aws_route53_record" "frontend" {
  zone_id = var.route53_zone_id
  name    = "streamlinebars.com"
  type    = "A"
  ttl     = 300
  records = [module.frontend_ec2.public_ip]
}
