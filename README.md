# WahidVR Kamera - Android Version

## Cara Build APK

### Persiapan (Ubuntu/Linux)
```bash
# Install dependencies
sudo apt update
sudo apt install -y build-essential git python3 python3-dev ffmpeg libsdl2-dev \
    libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev \
    libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev libgstreamer1.0 \
    gstreamer1.0-plugins-base automake autoconf libtool pkg-config \
    libgtk-3-dev libnotify-dev freeglut3-dev libgstreamer-plugins-base1.0-dev

# Install Buildozer
pip install buildozer

# Install Cython
pip install cython
```

### Build APK
```bash
# Masuk ke folder project
cd wahidvr-android

# Build APK (debug)
buildozer android debug

# APK akan ada di: bin/wahidvr-2.0-debug.apk

# Build APK (release)
buildozer android release
```

### Install di Android
```bash
# Via USB (aktifkan USB Debugging)
adb install bin/wahidvr-2.0-debug.apk

# Atau copy APK ke HP dan install manual
```

## Fitur
- 400+ Efek VR
- Kamera real-time
- Foto dengan efek
- Gallery bawaan
- Dark theme

## Spesifikasi
- Android 5.0+ (API 21)
- RAM: 2GB minimum
- Storage: 100MB

## Troubleshooting
1. Jika build gagal, coba: `buildozer android clean`
2. Pastikan semua dependencies terinstall
3. Gunakan Python 3.10 atau 3.11
4. Pastikan koneksi internet stabil saat build pertama kali
