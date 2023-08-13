from cx_Freeze import setup, Executable

exe = [Executable("main.py")]

setup(
    name = "claimx_mbk",
    version = "0.1",
    description = "bot for claimx mbk",
    executables = exe
)