# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# Get the directory of the .spec file
spec_dir = os.path.dirname(os.path.abspath(SPEC))

# Define the main app script
app_script = os.path.join(spec_dir, 'app.py')
launcher_script = os.path.join(spec_dir, 'launcher.py')

# Define data files to include
data_files = [
    # Main JSON data
    (os.path.join(spec_dir, 'troubleshooting_data.json'), '.'),
    
    # Images and resources folders (include everything inside)
    (os.path.join(spec_dir, 'images'), 'images'),
    (os.path.join(spec_dir, 'downloads'), 'downloads'),
    
    # Logo
    (os.path.join(spec_dir, 'logo.png'), '.'),
]

# Add the app.py script to the collection
a = Analysis(
    [launcher_script],  # Use launcher.py as the main script
    pathex=[spec_dir],
    binaries=[],
    datas=data_files,
    hiddenimports=['streamlit', 'streamlit.web', 'streamlit.runtime'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add the app.py script to the data files
a.datas += [('app.py', os.path.join(spec_dir, 'app.py'), 'DATA')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ATE_Operator_Helper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for non-console app (but keep True for debugging)
    icon=os.path.join(spec_dir, 'logo.png') if os.path.exists(os.path.join(spec_dir, 'logo.png')) else None,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
