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
  default = "t3.small"
}

variable "repo_url" {
  type        = string
  description = "GitHub URL"
  default     = "https://github.com/uiowaSEP2025/sep2025-project-team_001.git"
}

variable "repo_branch" {
  type        = string
  description = "GitHub branch"
  default     = "main"
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

variable "stripe_secret_key" {
  type      = string
  sensitive = true
  default   = "sk_test_51RAFr02cTgsJM4b1zq9w4tYcXuLKqwlvMGwEvW354FGgtknjwwV5OQgT5oLm1hfbGyZzecZn0r0kdfzr9ArKtwBW00uvzbCTbA"
}

variable "firebase_credentials_json" {
  type      = string
  sensitive = true
  default   = "ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAic3RyZWFtbGluZS1iYXItYXBwIiwKICAicHJpdmF0ZV9rZXlfaWQiOiAiOThkOGJmOTEyNTVlYWZjZTgzNmUxYTEyYjQ4OTE2MjZhYTE3YWRjMCIsCiAgInByaXZhdGVfa2V5IjogIi0tLS0tQkVHSU4gUFJJVkFURSBLRVktLS0tLVxuTUlJRXZRSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2N3Z2dTakFnRUFBb0lCQVFDYjdFaEJkSVpIYXZSU1xuaDIyV1B5eXR5b01vWVE1djN4bXRxaEtHc1ZrNmc0S1c3OC9haHdpQndSdFR3RTJRZG1JaGV2S3M5WFVwVVlTWVxuMHQ5dmxweTZ6a3dvR2VlcWZEUURNTXZWS09BeTZBNmhCUDQwZGRVZW5TcElyZXVLdEwxNGtTN3VHMUp5R1Y5bVxueFlJWHp4U2ovc0hPYmtsSGUvUWp4cDBvL1VzUzhibFl0MHZGWFVYRVFEUzRhR21nN2VHQk5pT1RNUncrTmY3WVxucjljUGxQeWc4QXZzVzNIWWZyUzZsdzRzY0hLS3RBMFNTa29EY0NqS2g4ZzVsQWMwQnJOOWFKVDQzblkydWNjYlxueXpMLzVzS2dEaEx3SlFOWnFUd1RZRzFBOFRqTFVDSWpNMU1oUXVqZFl2MTllOWk0aDZ4R1h1UEdiOElRTmpCRVxuaW53V0hDTnBBZ01CQUFFQ2dnRUFDblp3VWtrVkJoZU9rYmVoOGtBbXVib3lNeHhSSlU5YmlDQldpaWgrSCt1cFxuY0lLaXlFdUJsZ0JjMnJHM21yTWc2bFYzVVlVT2diRmxSQUo1YVFIYW5qdmYxeHlHNDdVZUlkMHRQazVWL2dCOVxuazg4emxoWldrTTF6eEFqOG1sUCt0MGVKdGtOSjFOdHdRQU9PazFXclVVWlQzNnZkbWJEKy9NUVQ4V2RPdVhSNVxuUGMyVGFkVERCZWZ6Y3R5Qi9vOFB6NHZCS011bHRQUGZQSDRYbDA3UXNrUXU1enAvanQ0NFZnYlQyYkxWOGpWYVxuK0R0OEtyRXg4SEJWWWxjMWNZYjZka1NXZUNLQStNczdueHpiV2NwK05kTTkwM0t2MjV4RDBPelQ0WFVaWmdBM1xuVFNKb3Rpb0FIbVZPSnV6RUhMVkNKaWFJWGwvR3dUczJXVGJXVjRqS2tRS0JnUURjYkhnUnhwMlhWQUR1aU92bFxuZ2VKZE5xUG9TdzBpK1ByMmFRcENWcGJtSG9CZFJtUG5VOUE0MGJMeEtsa1d3eTY1U0JvM2hCL0VsbThad2J0M1xuUm1NTjRqOWViM3RJL29DdGdNUm1HazNjdWN6MWNKUUwwZXFmMGxHQWFWNVRMSkh2SlgxUmtXajU4Nk8rUzl1alxuMnpvT0pTZEcyNkc4QkRCcUpzbmgzM3VPT1FLQmdRQzFGc0RYSEZ5Z0lVd0dKNUpwcFJsN0lZakwzYk9iZ3g4SlxuTTJZWU0vc1JYKzRhcnNOTXd3YTg2MmdUU1BnMm1iSmNBN3YxRDJvVnZTTG1wZmw2MVlXTklLMXNYdmRRMjU5NlxuN3JzdStrSHJqS2NGOUY3Uit0NWdreEtIK0piVDFJTENxNGZkMUV3Mzd0M3h2Q25kTmgxeWdSVjRRMG1wT2Jxb1xuM0c3OXp5VStzUUtCZ0VBaDN4MXM2RlVyUDhvblZGdEdXeEk3MzV5cW1YdmZiVVZjY251eXJkenVhdks0bEVDdVxuQmh0Q0NBcGJBK2kzaVZTblFkbDlPN0Q3QkFBK2Vjak9WZXVvTkQvSnQ5a1pFMTluNDd6QlVuNHlJUXdZWVRxL1xuTE1DcmRNTWo1U25XQWUvT3ZKT0s5endpUXpZTzVDemNrQnVsZTdRR0d4eVZLM0QzTUMzajFCTWhBb0dCQUpUalxuekZJUkk2Y1ZPV2ltQ0orTCsxTmQweGVyaFEwTDFleStzZWFjZG9WbWxtS2g1am1xOEZOTVNobnhHUVByZ3RaY1xueTZGRnR6ZUFkcjJsSVdaNVFJRTBxT0k5Z3FLY3NKZG15Y2hxUXVEa21EOHhHUFVVaXRwa2tndnh2REVXdlJ4SlxuNUQvaldYZHprbEE3SVVDY1NjSG5tRHQxTjQ5SHc4MHEwS2NtTmIxQkFvR0FVNlQ2UFVBZHJjb2tSRWhjU2tReFxuK0NnSnYyY21jV1o0Z0hyOHkvWFRTZ09YdDJ1eHd6M1g4SmJWWGl5UjlqSFc1WXYyN3ZKRk1YeHB3Q3hUdXhYdVxuOVhUZ0ZsZzV6ZW5tSUZCOXdRaUxvcGJ2QW1JVnJ0aTRqRG9jN0RqSWd3anVjcitGNUphRlRvVkh5R1FpdFVwWFxuVEZ5VUt0aGs3dWlpRTZGRTVwbkptYVk9XG4tLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tXG4iLAogICJjbGllbnRfZW1haWwiOiAiZmlyZWJhc2UtYWRtaW5zZGstZmJzdmNAc3RyZWFtbGluZS1iYXItYXBwLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAiY2xpZW50X2lkIjogIjEwMjEzNjgyNTQ5NDM2OTIzNDM0NSIsCiAgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwKICAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwKICAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsCiAgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvZmlyZWJhc2UtYWRtaW5zZGstZmJzdmMlNDBzdHJlYW1saW5lLWJhci1hcHAuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLAogICJ1bml2ZXJzZV9kb21haW4iOiAiZ29vZ2xlYXBpcy5jb20iCn0K"
}

variable "google_places_api_key" {
    type        = string
    description = "Google Places API key"
    default     = "AIzaSyDtuQZrrEzyvE3I6S5SChu1WABz0QQgenA"
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
