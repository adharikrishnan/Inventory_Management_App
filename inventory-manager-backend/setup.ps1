
$ErrorActionPreference = "Stop"

$VENV_PATH = ".venv"
$VENV_CREATED = $false

try {
    Write-Host "Installing Python 3.12.0 via pyenv..." -ForegroundColor Cyan
    pyenv install 3.12.0

    Write-Host "Setting local Python version to 3.12.0..." -ForegroundColor Cyan
    pyenv local 3.12.0

    Write-Host "Creating virtual environment..."

    if (-not (Test-Path -Path $VENV_PATH -PathType Container)) {
        python -m venv $VENV_PATH
        $VENV_CREATED = $true
    }

    Write-Host "Activating virtual environment..."

    # Activate the virtual environment
    & "$VENV_PATH\Scripts\Activate.ps1"

    Write-Host "Upgrading pip..."

    # Uncomment to upgrade pip
    # python -m pip install --upgrade pip

    if (Test-Path "requirements.txt" -PathType Leaf) {
        Write-Host "Installing packages from requirements.txt..." -ForegroundColor Cyan
        python -m pip install -r requirements.txt
    }
    else {
        Write-Warning "requirements.txt not found. Skipping package installation."
    }

    Write-Host "`nVirtual environment is ready and packages are installed!" -ForegroundColor Green
}
catch {
    Write-Host "`nAn error occurred during setup. Rolling back..." -ForegroundColor Red

    if ($VENV_CREATED -and (Test-Path -Path $VENV_PATH -PathType Container)) {
        Write-Host "Removing incomplete virtual environment ($VENV_PATH)..."
        Remove-Item -Path $VENV_PATH -Recurse -Force
    }

    Write-Host "Setup failed." -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red

    exit 1
}
