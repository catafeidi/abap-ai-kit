<#
.SYNOPSIS
  Creates a project folder with the standard notes structure (kit guidelines/notes.md).

.EXAMPLE
  scripts\new-project.ps1 -Name VICTRON
  scripts\new-project.ps1 -Name TRAVEL -Parent D:\work
#>
param(
    [Parameter(Mandatory = $true)][string]$Name,
    [string]$Parent
)

$ErrorActionPreference = 'Stop'
# Windows PowerShell 5.1 leaves $PSScriptRoot empty inside param() defaults; resolve it here
$Kit = Split-Path -Parent $PSScriptRoot
if (-not $Parent) { $Parent = $Kit }
$Template = "$Kit\templates\project"
$Target = Join-Path $Parent $Name

foreach ($dir in 'support\cases', 'support\kb', 'products', 'implementations', 'bugs', 'docs', 'tools', '_inbox', '.claude\skills', '.claude\agents') {
    New-Item -ItemType Directory -Force -Path (Join-Path $Target $dir) | Out-Null
}

Get-ChildItem -Recurse -File $Template | ForEach-Object {
    $relative = $_.FullName.Substring($Template.Length + 1)
    $destination = Join-Path $Target $relative
    if (Test-Path -LiteralPath $destination) { Write-Output "keep   $relative (exists)"; return }
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destination) | Out-Null
    $text = (Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8) -replace '\{\{NAME\}\}', $Name
    [System.IO.File]::WriteAllText($destination, $text, (New-Object System.Text.UTF8Encoding($false)))
    Write-Output "create $relative"
}

$continuity = Join-Path $Target '.claude\CONTINUITY.md'
if (-not (Test-Path -LiteralPath $continuity)) {
    Copy-Item "$Kit\templates\CONTINUITY.md.template" $continuity
    Write-Output 'create .claude\CONTINUITY.md'
}
# Own local git repository (never pushed): AI tools key project memory and project-scoped MCP
# servers on the git root, and the kit folder above is a repository too.
if (-not (Test-Path -LiteralPath (Join-Path $Target '.git'))) {
    git -C $Target init -q -b main
    git -C $Target add -A
    git -C $Target commit -q -m "Project skeleton"
    if ($LASTEXITCODE -ne 0) { Write-Output 'WARNING: first commit failed (git user.name / user.email set?); run git commit in the project yourself' }
    else { Write-Output 'create local git repository (no remote)' }
}
Write-Output "Project ready: $Target. Fill in AGENTS.md first."
