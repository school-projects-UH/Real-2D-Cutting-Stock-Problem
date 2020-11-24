Expand-Archive -Force ($PSScriptRoot + "\w64.zip") 'C:\w64'
if (-not (Test-Path env:Path)) { 
    [System.Environment]::SetEnvironmentVariable('Path', 'C:\w64', [System.EnvironmentVariableTarget]::User)
} else {
    [System.Environment]::SetEnvironmentVariable('Path', ($Env:Path + ';C:\w64'), [System.EnvironmentVariableTarget]::User)
}
echo "GLPK instalado correctamente"
cmd /c pause