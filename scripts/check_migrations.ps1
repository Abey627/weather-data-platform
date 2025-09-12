# PowerShell script to check and apply migrations in a CI/CD or build process
# This script runs the bash script inside the Docker container

param (
    [switch]$Apply
)

$ApplyFlag = ""
if ($Apply) {
    $ApplyFlag = "--apply"
    Write-Host "Will apply migrations if needed."
}

Write-Host "=== Checking Django migrations ==="

# Make sure the script is executable inside the container
docker-compose exec backend chmod +x /app/scripts/check_apply_migrations.sh

# Run the migration check script inside the container
$Result = docker-compose exec backend /app/scripts/check_apply_migrations.sh $ApplyFlag

# Display the output
$Result

# Check the exit code to determine if there were issues
if ($LASTEXITCODE -eq 0) {
    Write-Host "Migration check successful."
} elseif ($LASTEXITCODE -eq 1) {
    Write-Host "ERROR: New migrations need to be created."
    exit 1
} elseif ($LASTEXITCODE -eq 2) {
    Write-Host "WARNING: Pending migrations need to be applied."
    exit 2
} else {
    Write-Host "Unknown error during migration check."
    exit $LASTEXITCODE
}