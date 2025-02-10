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

variable "subnet_ids" {
  description = "List of subnet IDs for EKS and RDS"
  type        = list(string)
  default     = []
}