# scripts/build_graph.ps1
# Loads .env, creates junctions for the 15 knowledge directories, and executes graphify.

$ErrorActionPreference = "Stop"

# 1. Load .env environment variables
if (Test-Path ".env") {
    Write-Host "Loading .env file..." -ForegroundColor Cyan
    Get-Content ".env" | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#")) {
            if ($line -match '^([^=]+)=(.*)$') {
                $key = $Matches[1].Trim()
                $value = $Matches[2].Trim()
                # Remove quotes if present
                if ($value -match '^["''](.*)["'']$') { $value = $Matches[1] }
                [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
            }
        }
    }
}

# Verify GEMINI_API_KEY
if (-not $env:GEMINI_API_KEY) {
    Write-Error "GEMINI_API_KEY environment variable is not set in .env."
}

# 2. Setup Graphify Corpus Folder
$corpusDir = "graphify_corpus"
if (Test-Path $corpusDir) {
    Write-Host "Cleaning up old corpus links..." -ForegroundColor Yellow
    Get-ChildItem $corpusDir | ForEach-Object {
        if ($_.Attributes -match "ReparsePoint") {
            # Safely remove symbolic link/junction
            [System.IO.Directory]::Delete($_.FullName)
        } else {
            Remove-Item -Path $_.FullName -Recurse -Force
        }
    }
} else {
    New-Item -ItemType Directory -Path $corpusDir | Out-Null
}

# 3. Define the 15 directories to link
$directories = @(
    @{ Name = "obsidian-vault"; Path = "obsidian-vault" },
    @{ Name = "Cognitive Architecture"; Path = "Cognitive Architecture" },
    @{ Name = "System Architecture"; Path = "System Architecture" },
    @{ Name = "System Laws"; Path = "System Laws" },
    @{ Name = "System Specs"; Path = "System Specs" },
    @{ Name = "Intelligence Layer"; Path = "Intelligence Layer" },
    @{ Name = "Glossary trilogy"; Path = "Glossary trilogy" },
    @{ Name = "Knowledge engine expansion"; Path = "Knowledge engine expansion" },
    @{ Name = "Ontology"; Path = "Visual-Intelligence/knowledge/ontology" }
)

# 4. Create junctions
Write-Host "Linking knowledge directories..." -ForegroundColor Cyan
foreach ($dir in $directories) {
    $targetPath = Resolve-Path $dir.Path -ErrorAction SilentlyContinue
    if ($targetPath) {
        $linkPath = Join-Path $corpusDir $dir.Name
        Write-Host "Creating junction: $linkPath -> $targetPath"
        # Create junction using cmd /c mklink /j to ensure robust Windows behavior
        cmd /c mklink /j "$linkPath" "$targetPath" > $null
    } else {
        Write-Warning "Directory not found: $($dir.Path)"
    }
}

# 5. Run Graphify Pipeline
Write-Host "Executing Graphify extraction and building knowledge graph..." -ForegroundColor Green
# We run graphify through uv tool run to guarantee clean package isolation
uv tool run --from graphifyy graphify $corpusDir --model gemini-3.6-flash

Write-Host "Graphify execution complete." -ForegroundColor Green
