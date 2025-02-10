# modules/rds/variables.tf

variable "activate_rds" {
  description = "Toggle to activate (true) or deactivate (false) the RDS database"
  type        = bool
  default     = false
}

variable "subnet_ids" {
  description = "List of subnet IDs for the RDS database"
  type        = list(string)
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Database password"
  type        = string
  default     = "password123"
}
