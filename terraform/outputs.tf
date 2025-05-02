# outputs.tf

output "public_subnet_a_id" {
  description = "ID of the newly created public subnet a"
  value       = aws_subnet.public_subnet_a.id
}

output "public_subnet_b_id" {
  description = "ID of the newly created public subnet b"
  value       = aws_subnet.public_subnet_b.id
}

output "rds_endpoint" {
  description = "Endpoint of the RDS instance from the module"
  value       = module.rds.db_endpoint
}

output "backend_dns" {
  description = "DNS name for the backend"
  value       = aws_route53_record.backend_private_dns.fqdn
}

output "frontend_dns" {
  description = "DNS name for the frontend"
  value       = aws_route53_record.frontend.fqdn
}

output "s3_image_bucket_name" {
  value = module.s3_images.bucket_name
}

