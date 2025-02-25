# modules/backend_ec2/variables.tf

variable "name_prefix" {
  type        = string
  description = "Prefix for naming resources"
  default     = "my-backend"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID where EC2 is deployed"
}

variable "subnet_id" {
  type        = string
  description = "Public subnet ID"
}

variable "key_pair_name" {
  type        = string
  description = "EC2 key pair"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "backend_repo_url" {
  type        = string
  description = "GitHub URL"
  default     = "https://github.com/uiowaSEP2025/sep2025-project-team_001.git"
}

variable "db_host" {
  type        = string
  description = "RDS endpoint"
  default     = ""
}

variable "db_port" {
  type        = string
  description = "The database port"
  default     = "5432"
}

variable "db_name" {
  type        = string
  default     = "TestDatabase"
}

variable "db_user" {
  type        = string
  default     = "TestUser"
}

variable "db_pass" {
  type      = string
  sensitive = true
  default   = "password"
}

variable "dj_secret_key" {
  type      = string
  sensitive = true
  default   = "mysecretkey"
}
