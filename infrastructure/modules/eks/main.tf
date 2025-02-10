# modules/eks/main.tf

# EKS IAM Role
resource "aws_iam_role" "eks_cluster_role" {
  count = var.activate_eks ? 1 : 0

  name = "eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

# Attach EKS Policy to Role
resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  count      = var.activate_eks ? 1 : 0
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster_role[0].name
}

# EKS Cluster
resource "aws_eks_cluster" "project_cluster" {
  count    = var.activate_eks ? 1 : 0
  name     = "project-cluster"
  role_arn = aws_iam_role.eks_cluster_role[0].arn

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

# Data Source: EKS Cluster Information
data "aws_eks_cluster" "cluster" {
  count = var.activate_eks ? 1 : 0
  name  = aws_eks_cluster.project_cluster[0].name
}

# Data Source: Authentication Token for EKS
data "aws_eks_cluster_auth" "cluster" {
  count = var.activate_eks ? 1 : 0
  name  = aws_eks_cluster.project_cluster[0].name
}
