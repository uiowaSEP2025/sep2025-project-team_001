terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Kubernetes Provider
provider "kubernetes" {
  host                   = var.activate_eks ? module.eks.eks_cluster_endpoint : ""
  cluster_ca_certificate = var.activate_eks ? base64decode(module.eks.cluster_ca_certificate) : ""
  token                  = var.activate_eks ? module.eks.cluster_auth_token : ""
}

# VPC
resource "aws_vpc" "main_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "main_subnet_1" {
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "main-subnet-1"
  }
}

resource "aws_subnet" "main_subnet_2" {
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "main-subnet-2"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "main-igw"
  }
}

# Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public-rt"
  }
}

# Associate Route Table with Subnets
resource "aws_route_table_association" "public_rt_assoc_1" {
  subnet_id      = aws_subnet.main_subnet_1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_rt_assoc_2" {
  subnet_id      = aws_subnet.main_subnet_2.id
  route_table_id = aws_route_table.public_rt.id
}

# EKS Module
module "eks" {
  source       = "./modules/eks"
  subnet_ids   = [aws_subnet.main_subnet_1.id, aws_subnet.main_subnet_2.id]
  activate_eks = var.activate_eks
}

# Django Module
module "django" {
  source    = "./modules/django"
  image_url = "418272801449.dkr.ecr.us-east-1.amazonaws.com/django-api:latest"
  count     = var.deploy_django_api ? 1 : 0
}

# RDS Module
module "rds" {
  source      = "./modules/rds"
  subnet_ids  = [aws_subnet.main_subnet_1.id, aws_subnet.main_subnet_2.id]
  activate_rds = var.activate_rds
  db_username = "admin"
  db_password = "password123"
}

# Outputs
output "vpc_id" {
  value = aws_vpc.main_vpc.id
}

output "subnet_ids" {
  value = [aws_subnet.main_subnet_1.id, aws_subnet.main_subnet_2.id]
}

output "internet_gateway_id" {
  value = aws_internet_gateway.igw.id
}