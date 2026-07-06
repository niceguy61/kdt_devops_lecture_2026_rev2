param(
    [string]$Topic = "EKS Pod Identity",
    [int]$Limit = 2
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$env:PYTHONPATH = Join-Path $Root "src"

Write-Host "Running unit tests..."
python -m unittest discover -s (Join-Path $Root "tests")

Write-Host "Running live AWS docs search..."
python -m aws_doc_research_agent.cli search $Topic --limit $Limit

Write-Host "Running citation pack generation..."
python -m aws_doc_research_agent.cli citation-pack $Topic --limit $Limit

