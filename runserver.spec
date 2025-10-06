# server.spec
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.build_main import Analysis, PYZ, EXE
from PyInstaller.building.datastruct import TOC
from PyInstaller.compat import is_win
import os

datas = []
# Include Django project package data (templates, etc.)
datas += collect_data_files('yourproj', includes=['**/*.html','**/*.css','**/*.js','**/*.png','**/*.jpg','**/*.svg'])
# Include collected static
datas += [(os.path.join('yourproj','staticfiles'), os.path.join('yourproj','staticfiles'), 'DATA')]

a = Analysis(
    ['server.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['django','waitress'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='YourDjangoBackend',
    console=False,
)
