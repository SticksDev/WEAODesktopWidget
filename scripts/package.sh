iconAbsPath=$(realpath "assets/logo.ico")
assetsAbsPath=$(realpath "assets")

# Get the customtkinter path from pip show customtkinter
customtkinterAbsPath=$(python -c "import os; import customtkinter; print(os.path.dirname(customtkinter.__file__))")

# Check if this is a release build or a dev build
if [ -z "$GITHUB_REF" ]; then
    # This is a dev build
    echo "Building dev build"
    pyinstaller --noconfirm --onefile --windowed --icon "$iconAbsPath" --add-data "$assetsAbsPath;assets/" --add-data "$customtkinterAbsPath;customtkinter/" app.py -n "WEAO-${{ github.sha }}-nightly"

    export filename="WEAO-${{ github.sha }}-nightly"
else
    # This is a release build
    echo "Building release build"
    pyinstaller --noconfirm --onefile --windowed --icon "$iconAbsPath" --add-data "$assetsAbsPath;assets/" --add-data "$customtkinterAbsPath;customtkinter/" app.py -n "WEAO-${{ github.ref }}-release"

    export filename="WEAO-${{ github.ref }}-release"
fi