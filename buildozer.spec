[app]

# Title of your application
title = DLG

# Package name
package.name = dlg

# Package domain (needed for android/ios packaging)
package.domain = org.dlg

# Source code directory where the main.py lives
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas

# Application versioning
version = 0.1

# Application requirements
requirements = python3,kivy

# Supported orientations
orientation = portrait

# Android specific settings
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# List of assets to put in the apk assets directory
android.add_assets = url.zip:assets

# Buildozer specific settings
log_level = 2
warn_on_root = 1

[buildozer]

# Path to build artifact storage
# build_dir = ./.buildozer

# Path to build output storage
# bin_dir = ./bin
