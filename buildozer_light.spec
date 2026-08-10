[app]
title = WahidVR Kamera
package.name = wahidvr
package.domain = com.wahidvr
source.dir = .
source.include_exts = py,png,jpg,kv
version = 2.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33
android.arch = arm64-v8a
presplash.filename = %(source.dir)s/presplash.png
presplash.color = 0,0.52,0.83,1
icon.filename = %(source.dir)s/icon.png
