variable "image_url" {
  description = "Docker image URL from ECR"
  type        = string
}

variable "replicas_count" {
  description = "Number of replicas for the Django API server"
  type        = number
  default     = 1
}