# modules/backend_ec2/variables.tf

variable "name_prefix" {
  type        = string
  description = "Prefix for naming resources"
  default     = "backend"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID where EC2 is deployed"
}

variable "subnet_id" {
  type        = string
  description = "Private subnet ID"
}

variable "key_pair_name" {
  type        = string
  description = "EC2 key pair"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "repo_url" {
  type        = string
  description = "GitHub URL"
  default     = "https://github.com/uiowaSEP2025/sep2025-project-team_001.git"
}

variable "repo_branch" {
  type        = string
  description = "GitHub branch"
  default     = "SCRUM-58-aws-security-part-2"
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

variable "frontend_sg_id" {
  type        = string
  description = "Security Group ID of the frontend EC2 instance"
}

variable "nginx_sg_id" {
  type        = string
  description = "Security Group ID of the NGINX EC2 instance"
}

variable "mobile_cidr_blocks" {
  type        = list(string)
  description = "Allowed CIDR blocks for mobile clients"
  default     = ["0.0.0.0/0"]  # Replace with specific IP ranges if possible
}

variable "admin_ip" {
  type        = string
  description = "Allowed IP address for SSH access"
  default     = "0.0.0.0/0"
}
