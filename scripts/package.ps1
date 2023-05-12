# Get abousolute path of assets/
$assets = (Get-Item -Path ".\assets").FullName

# Get abousolute path for assets/logo.ico
$logo = (Get-Item -Path ".\assets\logo.ico").FullName

# Get the customtkinter path from pip show customtkinter
$customtkinter = (pip show customtkinter | Select-String -Pattern "Location" | Select-Object -Last 1).ToString().Split(": ")[-1]

# Check if this is a release build or a dev build (GITHUB_REF is only set on dev builds)

if ($env:GITHUB_REF) {
    # This is a dev build
    $version = "dev"
    $version += (Get-Date).ToString("yyyyMMddHHmmss")
    Write-Output "BUILD: $version - dev build"
    # Run build command
    pyinstaller --noconfirm --onefile --windowed --icon "$logo" --add-data "$assets;assets/" --add-data "$customtkinter;customtkinter/" app.py -n "WEAO-${{ github.sha }}-nightly"

    # Set filename for next step
    $env:FILENAME = "WEAO-${{ github.sha }}-nightly.exe"s
} else {
    # This is a release build
    $version = $env:GITHUB_REF.Split("/")[-1]
    Write-Output "BUILD: $version - release build"

    # Run build command
    pyinstaller --noconfirm --onefile --windowed --icon "$iconAbsPath" --add-data "$assetsAbsPath;assets/" --add-data "$customtkinterAbsPath;customtkinter/" app.py -n "WEAO-${{ github.ref }}-release"

    # Set filename for next step
    $env:FILENAME = "WEAO-${{ github.ref }}-release.exe"
}