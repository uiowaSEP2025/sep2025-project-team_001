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

# resource "aws_internet_gateway" "igw" {
#   vpc_id = var.vpc_id
#
#   tags = {
#     Name = "IGW"
#   }
# }

resource "aws_route_table_association" "public_rta_a" {
  route_table_id = var.rtb_id
  subnet_id      = aws_subnet.public_subnet_a.id
}

resource "aws_route_table_association" "public_rta_b" {
  route_table_id = var.rtb_id
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

########################################
# Call the EC2 Module
########################################
module "backend_ec2" {
  source = "./modules/ec2"

  name_prefix = "my-backend"
  vpc_id      = var.vpc_id
  subnet_id   = aws_subnet.public_subnet_a.id

  key_pair_name = var.key_pair_name

  # RDS info from the rds module
  db_host = module.rds.db_endpoint
  db_name = "TestDatabase"
  db_user = "TestUser"
  db_pass = var.db_password
  dj_secret_key = "mysecretkey123"
}
