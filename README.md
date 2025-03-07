# 🛠️ Installedfix

Sometimes when installing software on Windows via a package manager or when uninstalling something just by deleting the files, it results in a lot of broken entries in the "Installed apps" section of the settings. This script helps you clean up those invalid uninstallers from the registry.

## 🚀 Features

- 🕵️‍♂️ Automatically detects invalid uninstallers
- 🗑️ Removes invalid registry entries
- 📋 Logs removed entries

## 📋 How to Use

1. **Run as Administrator**: The script needs admin privileges to make changes to the registry. If not run as admin, it will prompt the user with a UAC.
2. **Backup Registry**: Before running the script, make a backup of your registry by running `regedit` and clicking on `File -> Export -> All`. [More info](#backupping-the-registry)
3. **Execute Script**: Run the script and follow the prompts to remove invalid uninstallers.

> [!CAUTION]
> Always ensure you have a backup of your registry before making any changes.

## 📦 Backupping the Registry

To avoid backing up the entire registry, you can also backup just the following paths:

- `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall`
- `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall`
- `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall`
- `HKEY_CURRENT_USER\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall`

## 📄 License

This project is licensed under the MIT License.
