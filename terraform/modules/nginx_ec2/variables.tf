# modules/nginx_ec2/variables.tf

variable "vpc_id" {
  description = "VPC ID where the NGINX instance will be deployed"
  type        = string
}

variable "subnet_id" {
  description = "Public subnet ID for the NGINX instance"
  type        = string
}

variable "key_pair_name" {
  description = "EC2 key pair name for SSH access"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type for NGINX"
  type        = string
  default     = "t3.micro"
}

variable "name_prefix" {
  description = "Prefix for naming NGINX resources"
  type        = string
  default     = "nginx"
}

variable "domain_name" {
  description = "The domain name to be used in the NGINX configuration"
  type        = string
}

variable "admin_ip" {
  type        = string
  description = "Your IP address for SSH access"
  default     = "0.0.0.0/0"
}

variable "frontend_target" {
  description = "The private IP or DNS of the frontend (port 3000)."
  type        = string
}

variable "backend_target" {
  description = "The private IP or DNS of the backend (port 8000)."
  type        = string
}
