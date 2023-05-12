# Get abousolute path of assets/
$assets = (Get-Item -Path ".\assets").FullName

# Get abousolute path for assets/logo.ico
$logo = (Get-Item -Path ".\assets\logo.ico").FullName

# Get the customtkinter path from pip show customtkinter
$customtkinter = (pip show customtkinter | Select-String -Pattern "Location" | Select-Object -Last 1).ToString().Split(": ")[-1]
$githubshashort = $env:GITHUB_SHA.Substring(0, 7)

if ($env:GITHUB_REF) {
    # This is a dev build
    $version = "dev"
    $version += (Get-Date).ToString("yyyyMMddHHmmss")
    Write-Output "BUILD: $version - dev build"
    # Run build command
    pyinstaller --noconfirm --onefile --windowed --icon "$logo" --add-data "$assets;assets/" --add-data "$customtkinter;customtkinter/" app.py -n "WEAO-$githubshashort-$version-nightly"

    # Set filename for next step
    $env:FILENAME = "WEAO-$githubshashort-$version-nightly"
} else {
    # This is a release build
    $version = $env:GITHUB_REF.Split("/")[-1]
    Write-Output "BUILD: $version - release build"

    # Run build command
    pyinstaller --noconfirm --onefile --windowed --icon "$iconAbsPath" --add-data "$assetsAbsPath;assets/" --add-data "$customtkinterAbsPath;customtkinter/" app.py -n "WEAO-$githubshashort-release"

    # Set filename for next step
    $env:FILENAME = "WEAO-$githubshashort-release"
}