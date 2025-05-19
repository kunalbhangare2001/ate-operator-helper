# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\ATE_Operator_Helper\\ATE_Operator_Helper\\launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\ATE_Operator_Helper\\ATE_Operator_Helper\\app.py', '.'), ('D:\\ATE_Operator_Helper\\ATE_Operator_Helper\\troubleshooting_data.json', '.'), ('D:\\ATE_Operator_Helper\\ATE_Operator_Helper\\logo.png', '.'), ('D:\\ATE_Operator_Helper\\ATE_Operator_Helper\\images', 'images'), ('D:\\ATE_Operator_Helper\\ATE_Operator_Helper\\downloads', 'downloads')],
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
    name='launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
