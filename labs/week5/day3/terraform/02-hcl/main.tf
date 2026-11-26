# 2 · 3교시 · 변수 · locals · 데이터 소스 · for_each · 자원 사이의 참조

data "aws_caller_identity" "me" {}

data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  prefix = "devmart-${var.owner}"
}

resource "aws_s3_bucket" "this" {
  for_each = var.buckets
  bucket   = "${local.prefix}-${each.key}"

  force_destroy = true # 실습용 — destroy할 때 안의 파일 · 버전까지 지운다 (운영에서는 false)
}

resource "aws_s3_bucket_versioning" "this" {
  for_each = var.buckets
  bucket   = aws_s3_bucket.this[each.key].id # ← 참조가 곧 의존 관계

  versioning_configuration {
    status = each.value.versioning ? "Enabled" : "Suspended"
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  for_each = var.buckets
  bucket   = aws_s3_bucket.this[each.key].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "notice" {
  bucket       = aws_s3_bucket.this["assets"].id
  key          = "notice.txt"
  content      = "DevMart 공지 — Terraform이 올렸다 (계정 ${data.aws_caller_identity.me.account_id})"
  content_type = "text/plain; charset=utf-8"
}
