# variables.tf

variable "region" {
  type        = string
  description = "AWS region to create resources in"
  default     = "us-east-1"
}

variable "vpc_id" {
  type        = string
  description = "Existing VPC ID where we create the public subnet and RDS"
  default     = "vpc-08c7b9b0ac1b101bc"
}

variable "rtb_id" {
    type        = string
    description = "Route Table ID for the public subnet"
    default     = "rtb-00e3d8888e26c0c91"
}

variable "db_password" {
  type        = string
  description = "Master password for the RDS instance"
  sensitive   = true
  default     = "password"
}

variable "key_pair_name" {
  type        = string
  description = "EC2 key pair for SSH"
  default     = "terraform-key-pair"
}