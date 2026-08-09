# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

import pygame

python_license = Path(sys.base_prefix) / 'LICENSE.txt'
pygame_license = Path(pygame.__file__).resolve().parent / 'docs' / 'generated' / 'LGPL.txt'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('PRIVACY.md', '.'),
        ('SUPPORT.md', '.'),
        ('THIRD_PARTY_NOTICES.md', '.'),
        (str(python_license), 'licenses'),
        (str(pygame_license), 'licenses'),
        ('licenses/POPPINS-OFL.txt', 'licenses'),
    ],
    hiddenimports=['typing_extensions'],
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
    name='Sudoku Wizard',
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
    icon=['assets\\images\\game_logo.ico'],
    version='version_info.txt',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Sudoku Wizard',
)
