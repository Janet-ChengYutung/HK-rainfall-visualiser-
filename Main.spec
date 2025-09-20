# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Main.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/janet/Downloads/pfad/HK-rainfall-visualiser-/image', 'image'), ('/Users/janet/Downloads/pfad/HK-rainfall-visualiser-/rainfall_charts', 'rainfall_chart'), ('/Users/janet/Downloads/pfad/HK-rainfall-visualiser-/data/monthlyElement.xml', '.'), ('/Users/janet/Downloads/pfad/HK-rainfall-visualiser-/GoogleSansCode-VariableFont_wght.ttf', '.')],
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
    a.binaries,
    a.datas,
    [],
    name='Main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='Main.app',
    icon=None,
    bundle_identifier=None,
)
