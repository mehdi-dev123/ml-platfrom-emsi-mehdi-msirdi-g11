# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('assets', 'assets')]
datas += collect_data_files('customtkinter')
datas += collect_data_files('matplotlib')
datas += collect_data_files('statsmodels')


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['matplotlib.backends.backend_tkagg'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pandas.tests', 'sklearn.tests', 'scipy.tests', 'matplotlib.tests'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Plateforme-IA-ML',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Plateforme-IA-ML',
)
