<#
.SYNOPSIS
    Build LaTeX CVs and cover letters to PDF.
.DESCRIPTION
    Compiles .tex files in the Latex-CV project using pdflatex or latexmk.
.PARAMETER Path
    Path to a specific application folder or .tex file to build.
.PARAMETER All
    Build all .tex files in all application folders.
.PARAMETER Clean
    Remove LaTeX build artifacts (.aux, .log, .fls, .fdb_latexmk, .out, .synctex.gz).
.PARAMETER Templates
    Also build files in the templates/ folder.
.EXAMPLE
    .\build.ps1 -Path applications\Frontend_React
    .\build.ps1 -Path applications\Frontend_React\EN\cv_frontend_react_en.tex
    .\build.ps1 -All
    .\build.ps1 -Clean
    .\build.ps1 -Clean -Path applications\Frontend_React
#>

param(
    [string]$Path,
    [switch]$All,
    [switch]$Clean,
    [switch]$Templates
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot

# LaTeX artifact extensions to clean
$ArtifactExtensions = @("*.aux", "*.log", "*.fls", "*.fdb_latexmk", "*.out",
    "*.synctex.gz", "*.synctex", "*.bbl", "*.blg", "*.toc",
    "*.lof", "*.lot", "*.nav", "*.snm", "*.vrb", "*.run.xml")

function Find-TexFiles {
    param([string]$SearchPath)
    Get-ChildItem -Path $SearchPath -Filter "*.tex" -Recurse |
    Where-Object { $_.Directory.FullName -notmatch '\\\.git\\' }
}

function Build-TexFile {
    param([string]$TexFile)

    $dir = Split-Path $TexFile -Parent
    $name = Split-Path $TexFile -Leaf

    Write-Host "  Building: $name" -ForegroundColor Cyan

    Push-Location $dir
    try {
        # Check if latexmk is available
        $useLatexmk = Get-Command latexmk -ErrorAction SilentlyContinue

        if ($useLatexmk) {
            & latexmk -pdf -interaction=nonstopmode $name 2>&1 | Out-Null
        }
        else {
            # Run pdflatex twice for references
            & pdflatex -interaction=nonstopmode $name 2>&1 | Out-Null
            & pdflatex -interaction=nonstopmode $name 2>&1 | Out-Null
        }

        $pdfName = [System.IO.Path]::ChangeExtension($name, ".pdf")
        if (Test-Path $pdfName) {
            Write-Host "  OK: $pdfName" -ForegroundColor Green
        }
        else {
            Write-Host "  FAILED: $name (no PDF produced)" -ForegroundColor Red
        }
    }
    finally {
        Pop-Location
    }
}

function Remove-Artifacts {
    param([string]$SearchPath)

    $count = 0
    foreach ($ext in $ArtifactExtensions) {
        $files = Get-ChildItem -Path $SearchPath -Filter $ext -Recurse -ErrorAction SilentlyContinue
        foreach ($f in $files) {
            Remove-Item $f.FullName -Force
            $count++
        }
    }
    Write-Host "Cleaned $count artifact files from $SearchPath" -ForegroundColor Yellow
}

# --- Main ---

if ($Clean) {
    if ($Path) {
        $target = Join-Path $ProjectRoot $Path
        if (-not (Test-Path $target)) { Write-Error "Path not found: $target"; exit 1 }
        Remove-Artifacts -SearchPath $target
    }
    else {
        Remove-Artifacts -SearchPath (Join-Path $ProjectRoot "applications")
        Remove-Artifacts -SearchPath (Join-Path $ProjectRoot "templates")
    }
    exit 0
}

$texFiles = @()

if ($Path) {
    $target = Join-Path $ProjectRoot $Path
    if (-not (Test-Path $target)) { Write-Error "Path not found: $target"; exit 1 }

    if ($target -match '\.tex$') {
        $texFiles += $target
    }
    else {
        $texFiles += (Find-TexFiles -SearchPath $target).FullName
    }
}
elseif ($All) {
    $texFiles += (Find-TexFiles -SearchPath (Join-Path $ProjectRoot "applications")).FullName
    if ($Templates) {
        $texFiles += (Find-TexFiles -SearchPath (Join-Path $ProjectRoot "templates")).FullName
    }
}
else {
    Write-Host "Usage:" -ForegroundColor White
    Write-Host "  .\build.ps1 -Path applications\Frontend_React   # Build one folder"
    Write-Host "  .\build.ps1 -Path applications\Frontend_React\EN\cv_frontend_react_en.tex  # Build one file"
    Write-Host "  .\build.ps1 -All                                 # Build all applications"
    Write-Host "  .\build.ps1 -All -Templates                      # Build all including templates"
    Write-Host "  .\build.ps1 -Clean                               # Clean all artifacts"
    Write-Host "  .\build.ps1 -Clean -Path applications\Frontend_React  # Clean one folder"
    exit 0
}

if ($texFiles.Count -eq 0) {
    Write-Host "No .tex files found." -ForegroundColor Yellow
    exit 0
}

Write-Host "`nBuilding $($texFiles.Count) file(s)...`n" -ForegroundColor White

foreach ($tex in $texFiles) {
    Build-TexFile -TexFile $tex
}

Write-Host "`nDone." -ForegroundColor Green
