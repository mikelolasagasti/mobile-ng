#!/usr/bin/env bash

git clone https://gitlab.gnome.org/GNOME/mobile-broadband-provider-info

python parse-and-create-content.py

wget https://github.com/gohugoio/hugo/releases/download/v0.121.1/hugo_0.121.1_Linux-64bit.tar.gz
tar xf hugo_0.121.1_Linux-64bit.tar.gz
cd web/
../hugo server --buildDrafts --disableFastRender --renderToDisk

