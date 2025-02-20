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
# Create 2 Public Subnets in an Existing VPC
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

resource "aws_internet_gateway" "igw" {
  vpc_id = var.vpc_id

  tags = {
    Name = "IGW"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = var.vpc_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "PublicRouteTable"
  }
}

resource "aws_route_table_association" "public_rta_a" {
  route_table_id = aws_route_table.public_rt.id
  subnet_id      = aws_subnet.public_subnet_a.id
}

resource "aws_route_table_association" "public_rta_b" {
  route_table_id = aws_route_table.public_rt.id
  subnet_id      = aws_subnet.public_subnet_b.id
}

########################################
# Call the RDS Module
########################################
module "rds" {
  source = "./modules/rds"

  # Pass in VPC/Subnet for RDS
  vpc_id      = var.vpc_id
  subnet_ids  = [aws_subnet.public_subnet_a.id, aws_subnet.public_subnet_b.id]

  db_identifier = "postgres-db"
  db_name       = "TestDatabase"
  db_username   = "TestUser"
  db_password   = var.db_password

  # Make RDS publicly accessible for easy testing
  publicly_accessible = true

  # Allow wide open access (NOT for production!)
  allowed_cidr_blocks   = ["0.0.0.0/0"]
}
