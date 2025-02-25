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
  default     = "moving-to-aws"
}

variable "backend_api_url" {
  type        = string
  description = "The URL of the backend API that the frontend will call (e.g., http://api.yourcompany.com:8000)"
}
