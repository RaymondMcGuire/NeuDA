cd ..

uv python install 3.9

uv python pin 3.9

uv venv

uv lock
uv sync

uv pip install --index-url https://download.pytorch.org/whl/cu128 torch==2.8.0 torchvision==0.23.0

uv pip install --no-build-isolation -e submodules/pytorch3d

pause
