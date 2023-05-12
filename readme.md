<p align="center">
<img src="https://github.com/SticksDev/WEAODesktopWidget/assets/5618953/b006d247-8c23-4475-8bf7-7ffd81668565"></img>
</p>



# WEAO Desktop Widget
This is a Desktop client for the exploit checker website [whatexploitsare.online](https://whatexploitsare.online/). It is built using [Python](https://www.python.org/) and [customtkinter](https://customtkinter.tomschimansky.com/)

## Demo

[On Streamable](https://streamable.com/tkcl4f)

## Installation

This app should support all platforms that support Python and tkinter. However, it has only been tested on Windows 11. There's two ways to install this app:

### 1. Download the executable
You can download the executable from the [releases page](https://github.com/SticksDev/WEAODesktopWidget/releases) and run it. This is the easiest way to install the app, and it includes all the dependencies.

### 2. Build from source

> **Warning**
> This method is isn't recommended for normal users! You must have a terminal window open to run the app this way! 

If you don't trust the executable, or you want to make changes to the app, you can build it from source. To do this, you need to have Python 3.10 installed. You can download it from [here](https://www.python.org/downloads/). Make sure to check the box that says "Add Python 3.10 to PATH". Then, download the source code from the [releases page](https://github.com/SticksDev/WEAODesktopWidget/releases)

Then run the following commands in the directory you downloaded the source code to:
```
pip install -r requirements.txt
python app.py
```

The app should now be running. You can make changes to the source code and run the app again to see the changes.


## Contributing

If you want to contribute to this project, you can fork the repository and make a pull request. If you want to make a big change, ask me in the WEAO discord server first (sticks#2701). When making a pull request, make sure to include a description of what you changed and why, and also follow the below guidelines:

- Do not edit the version.json file. This is automatically updated by the build script.
- Do not edit any CI pipelines without express permission from me.
- Do not edit the version in the app.py file. This is automatically updated by the build script.

## License
This project is licensed under the MIT license. See the [LICENSE](LICENSE) file for more info.
