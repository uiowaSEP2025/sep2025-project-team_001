# infrastructure/variables.tf

variable "activate_eks" {
  description = "Toggle to activate (true) or deactivate (false) the EKS cluster"
  type        = bool
  default     = true
}

variable "activate_rds" {
  description = "Toggle to activate (true) or deactivate (false) the RDS database"
  type        = bool
  default     = true
}

variable "deploy_django_api" {
  description = "Toggle to deploy (true) or not deploy (false) the Django REST API"
  type        = bool
  default     = true
}

variable "subnet_ids" {
  description = "List of subnet IDs for EKS and RDS"
  type        = list(string)
  default     = []
}

variable "replicas_count" {
  description = "Number of replicas for Django API server, EKS cluster, and RDS database"
  type        = number
  default     = 1
}