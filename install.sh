# #!/bin/bash

echo "== Installing Package =="
python -m pip install --upgrade pip
pip install requests==2.32.3
pip install beautifulsoup4==4.12.3
pip install selenium==4.22.0
pip install fastapi==0.111.0
pip install "uvicorn[standard]"

echo "== Installation Complete!! =="