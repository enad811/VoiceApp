[app]
title = Voice App
package.name = voiceapp
package.domain = org.emad
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
version = 0.1
requirements = python3,kivy==2.3.0,gtts,cython==3.0.11
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
