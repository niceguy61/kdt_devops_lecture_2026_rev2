$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$env:PYTHONPATH = Join-Path $Root "src"

python -c "import importlib.util; print('mcp installed:', importlib.util.find_spec('mcp') is not None)"

