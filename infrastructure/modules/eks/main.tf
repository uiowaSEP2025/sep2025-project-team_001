# modules/eks/main.tf

resource "aws_iam_role" "eks_cluster_role" {
  count = var.activate_eks ? 1 : 0  # Activate/Deactivate EKS

  name = "eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = { Service = "eks.amazonaws.com" },
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  count = var.activate_eks ? 1 : 0  # Activate/Deactivate EKS

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster_role[0].name
}

resource "aws_eks_cluster" "project_cluster" {
  count    = var.activate_eks ? 1 : 0  # Activate/Deactivate EKS
  name     = "project-cluster"
  role_arn = aws_iam_role.eks_cluster_role[0].arn

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

output "eks_cluster_endpoint" {
  value       = var.activate_eks ? aws_eks_cluster.project_cluster[0].endpoint : ""
  description = "EKS Cluster API endpoint"
}
