# modules/eks/outputs.tf

output "eks_cluster_endpoint" {
  description = "EKS Cluster API endpoint"
  value       = var.activate_eks ? data.aws_eks_cluster.cluster[0].endpoint : ""
}

output "cluster_ca_certificate" {
  description = "EKS Cluster CA Certificate"
  value       = var.activate_eks ? data.aws_eks_cluster.cluster[0].certificate_authority[0].data : ""
}

output "cluster_auth_token" {
  description = "EKS Cluster Authentication Token"
  value       = var.activate_eks ? data.aws_eks_cluster_auth.cluster[0].token : ""
}
