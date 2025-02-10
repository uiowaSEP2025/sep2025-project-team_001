# modules/eks/variables.tf

variable "activate_eks" {
  description = "Toggle to activate (true) or deactivate (false) the EKS cluster"
  type        = bool
  default     = false
}

variable "subnet_ids" {
  description = "List of subnet IDs for the EKS cluster"
  type        = list(string)
}
