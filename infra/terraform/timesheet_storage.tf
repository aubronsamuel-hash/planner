// Placeholder storage bucket for timesheet exports.
resource "aws_s3_bucket" "timesheet_exports" {
  bucket = "planner-timesheet-exports-demo"
  acl    = "private"
}
