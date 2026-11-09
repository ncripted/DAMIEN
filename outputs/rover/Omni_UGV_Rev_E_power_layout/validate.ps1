# Repeat configured checks using installed KiCad10; no live editor connection.
$ErrorActionPreference = 'Stop'
$roverRoot = $PSScriptRoot
$kicadCli = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
if (-not (Test-Path -LiteralPath $kicadCli)) { throw 'Set kicadCli to your installed CLI path.' }
$env:KICAD_DOCUMENTS_HOME = Join-Path $roverRoot '.validation-runtime\documents'
$env:KICAD_CONFIG_HOME = Join-Path $roverRoot '.validation-runtime\config'
$reportDir = Join-Path $roverRoot 'validation\current'
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
& $kicadCli pcb drc --schematic-parity --severity-all --refill-zones --format json -o (Join-Path $reportDir 'drc.json') (Join-Path $roverRoot 'omni_ugv.kicad_pcb')
if ($LASTEXITCODE -ne 0) { throw 'DRC execution failed.' }
& $kicadCli sch erc --format json -o (Join-Path $reportDir 'erc.json') (Join-Path $roverRoot 'omni_ugv.kicad_sch')
if ($LASTEXITCODE -ne 0) { throw 'ERC execution failed.' }
$drcReport = Get-Content -LiteralPath (Join-Path $reportDir 'drc.json') -Raw | ConvertFrom-Json
$ercReport = Get-Content -LiteralPath (Join-Path $reportDir 'erc.json') -Raw | ConvertFrom-Json
[pscustomobject]@{
    DrcErrors = @($drcReport.violations | Where-Object severity -eq error).Count
    DrcWarnings = @($drcReport.violations | Where-Object severity -eq warning).Count
    Unconnected = @($drcReport.unconnected_items).Count
    ParityIssues = @($drcReport.schematic_parity).Count
    ErcViolations = @($ercReport.sheets | ForEach-Object { $_.violations }).Count
}
