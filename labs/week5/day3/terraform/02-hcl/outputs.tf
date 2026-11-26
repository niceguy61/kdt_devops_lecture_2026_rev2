output "account_id" {
  value = data.aws_caller_identity.me.account_id
}

output "azs" {
  value = data.aws_availability_zones.available.names
}

output "bucket_names" {
  value = { for k, b in aws_s3_bucket.this : k => b.bucket }
}
