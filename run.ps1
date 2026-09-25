#requires -Version 5.1
<#
.SYNOPSIS
    Set up the Quetza Python starter and open run.py.
.DESCRIPTION
    Creates or reuses a real .venv beside this script.
    Creates requirements.txt only if it does not already exist.
    Installs the example packages into .venv, then starts run.py.
    Requires Windows and Python 3.12 or later with Tcl/Tk support.
    The first package installation needs an internet connection.

    Put run.ps1 beside run.py. Run this command from that folder:
        powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run.ps1

    The script uses the virtual environment's Python directly.
    A separate activation command is not needed.
.PARAMETER SkipInstall
    Skip package installation and use an existing environment.
.PARAMETER PythonPath
    Select a Python executable when creating a new environment.
    An existing .venv continues to use its original interpreter.
.EXAMPLE
    .\run.ps1
.EXAMPLE
    .\run.ps1 -SkipInstall
.EXAMPLE
    .\run.ps1 -PythonPath "C:\Python312\python.exe"
.NOTES
    The blank window does not need these extra packages.
    They prepare the environment for the import examples in run.py.
    Installing a package does not enable a commented import or add a feature.

    References:
    https://docs.python.org/3/library/venv.html
    https://pip.pypa.io/en/stable/cli/pip_install/
    https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_automatic_variables
#>

[CmdletBinding()]
param(
    [switch]$SkipInstall,
    [string]$PythonPath = ""
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = "Stop"

# Keep all project files together, even when called from another folder.
$projectDirectory = $PSScriptRoot
$appPath = Join-Path $projectDirectory "run.py"
$environmentDirectory = Join-Path $projectDirectory ".venv"
$environmentPython = Join-Path $environmentDirectory "Scripts\python.exe"
$environmentConfig = Join-Path $environmentDirectory "pyvenv.cfg"
$requirementsPath = Join-Path $projectDirectory "requirements.txt"

# A failed Python command must stop setup instead of silently continuing.
function Invoke-PythonStep {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Executable,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,

        [Parameter(Mandatory = $true)]
        [string]$FailureMessage
    )

    & $Executable @Arguments
    $nativeExitCode = $LASTEXITCODE
    if ($nativeExitCode -ne 0) {
        throw "$FailureMessage (exit code $nativeExitCode)"
    }
}

$locationChanged = $false
$scriptExitCode = 0

try {
    if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
        throw "This launcher requires Windows."
    }
    if (-not (Test-Path -LiteralPath $appPath -PathType Leaf)) {
        throw "Put run.ps1 in the same folder as run.py."
    }

    Push-Location -LiteralPath $projectDirectory
    $locationChanged = $true

    Write-Host ""
    Write-Host "QUETZA | PYTHON STARTER" -ForegroundColor Cyan
    Write-Host "Project: $projectDirectory" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "[1/4] Prepare the virtual environment" -ForegroundColor Cyan

    if (Test-Path -LiteralPath $environmentDirectory) {
