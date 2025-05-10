# -*- mode: python ; coding: utf-8 -*-

import platform

system = platform.system()

if system == "Darwin":
    lib_extension = ".dylib"
elif system == "Linux":
    lib_extension = ".so"
elif system == "Windows":
    lib_extension = ".dll"
else:
    raise RuntimeError(f"Unsupported platform: {system}")

lib_filename = f"libimage2icon{lib_extension}"

#target for cmake build
rust_target_dir = os.path.join(os.getcwd(), "rust_target", "release", "universal2")
lib_path = os.path.join(rust_target_dir, lib_filename)

if not os.path.exists(lib_path):
    raise RuntimeError(f"Library not found at expected path: {lib_path}")

binaries = [
    (lib_path, 'image2icon'),
]

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=[ 
        ('resources', 'resources'),
        ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='image2icon',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='universal2',
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon=['resources/image2icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='image2icon',
)
app = BUNDLE(
    coll,
    name='image2icon.app',
    icon='resources/image2icon.icns',
    bundle_identifier='com.example.image2icon',
    version='0.1.0',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'NSHighResolutionCapable': True,
        'CFBundleName': 'image2icon',
        'CFBundleShortVersionString': '0.1',
        'CFBundleVersion': '0.1.0',  
        'CFBundleIdentifier': 'com.example.image2icon',
    },
)
