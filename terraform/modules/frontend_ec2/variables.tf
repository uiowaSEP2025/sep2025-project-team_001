variable "name_prefix" {
  type        = string
  description = "Prefix for naming frontend resources"
  default     = "my-frontend"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID where the frontend EC2 instance will be deployed"
}

variable "subnet_id" {
  type        = string
  description = "Public subnet ID for the frontend EC2 instance"
}

variable "key_pair_name" {
  type        = string
  description = "EC2 key pair name for SSH access"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t3.micro"
}

variable "repo_url" {
  type        = string
  description = "Git repository URL for the frontend application"
  default     = "https://github.com/uiowaSEP2025/sep2025-project-team_001.git"
}

variable "repo_branch" {
  type        = string
  description = "Git branch to clone for the frontend application"
  default     = "main"
}

variable "admin_ip" {
  type        = string
  description = "Your IP address for SSH access"
  default     = "0.0.0.0/0"
}

variable "nginx_sg_id" {
  description = "Security Group ID of the NGINX instance"
  type        = string
}
