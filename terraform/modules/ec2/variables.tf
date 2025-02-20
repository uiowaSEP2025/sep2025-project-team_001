variable "vpc_id" {
  type        = string
  description = "VPC ID where EC2 is deployed"
}

variable "public_subnet_ids" {
  type        = list(string)
  description = "List of public subnet IDs"
}

variable "key_pair_name" {
  type        = string
  description = "EC2 key pair"
}

variable "rds_endpoint" {
  type        = string
  description = "RDS endpoint (optional)"
  default     = ""
}