# modules/rds/variables.tf

variable "vpc_id" {
  type        = string
  description = "VPC ID for RDS security group"
}

variable "subnet_ids" {
  type        = list(string)
  description = "List of subnets for the DB Subnet Group"
}

variable "db_identifier" {
  type        = string
  description = "Name of the RDS instance"
  default     = "my-postgres-db"
}

variable "db_name" {
  type        = string
  description = "Database name"
  default     = "db"
}

variable "db_username" {
  type        = string
  description = "Master username"
  default     = "user"
}

variable "db_password" {
  type        = string
  description = "Master password"
  sensitive   = true
}

variable "allocated_storage" {
  type        = number
  description = "DB allocated storage in GB"
  default     = 20
}

variable "engine" {
  type    = string
  default = "postgres"
}

variable "engine_version" {
  type    = string
  default = "14"
}

variable "instance_class" {
  type    = string
  default = "db.t3.micro"
}

variable "publicly_accessible" {
  type    = bool
  default = false
}

variable "skip_final_snapshot" {
  type    = bool
  default = true
}

variable "backend_sg_id" {
  type        = string
  description = "Security Group ID of the backend EC2 instance"
}
