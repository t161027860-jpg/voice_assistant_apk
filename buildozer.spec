[app]
title = Voice Assistant
package.name = voiceassistant
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,md

version = 0.1

requirements = python3,kivy,pyjnius,requests,urllib3,certifi,charset-normalizer,idna,android

android.permissions = RECORD_AUDIO,INTERNET,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,MODIFY_AUDIO_SETTINGS

android.minapi = 24
android.api = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

orientation = portrait
android.wakelock = True

[buildozer]
log_level = 2
warn_on_root = 0
