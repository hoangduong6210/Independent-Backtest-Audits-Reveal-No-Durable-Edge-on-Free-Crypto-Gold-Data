# One-command reproduce (Windows). Seeds fixed.
$ErrorActionPreference = "Stop"
$Py = $env:PYTHON
if (-not $Py) { foreach ($c in @("py","python3","python")) { try { & $c --version *> $null; if ($LASTEXITCODE -eq 0) { $Py=$c; break } } catch {} } }
& $Py "$PSScriptRoot/make_figures.py"
& $Py "$PSScriptRoot/run_stats.py"
