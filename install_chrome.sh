#!/bin/bash
echo "Instalando Chrome..."
wget -q -O chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update
apt-get install -y ./chrome.deb
rm chrome.deb
echo "Chrome instalado correctamente."