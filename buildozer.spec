[app]

# App information
title = English Word Study
package.name = wordstudy
package.domain = org.study
source.dir = ./studyapp
source.include_exts = py,png,jpg,kv,atlas,json,ttf,ttc,otf,mp3,wav
version = 1.0

# Requirements (Python modules)
requirements = python3,kivy==2.3.0,edge-tts,pyjnius,android,asyncio

# App orientation
orientation = portrait
fullscreen = 0

# Android configuration
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = arm64-v8a
android.allow_backup = True

# Android permissions
android.permissions = INTERNET

# Include assets (fonts, data, images)
android.include_exts = py,png,jpg,jpeg,ttf,ttc,otf,json,kv

[buildozer]
log_level = 2
warn_on_root = 0