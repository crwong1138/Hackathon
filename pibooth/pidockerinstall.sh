#!/bin/sh

bin=$( basename "${0}" )


# http://blog.hypriot.com/post/run-docker-rpi3-with-wifi/
ssh pi@raspberrypi.local
sudo apt-get install -y apt-transport-https
wget -q https://packagecloud.io/gpg.key -O - | sudo apt-key add -
echo 'deb https://packagecloud.io/Hypriot/Schatzkiste/debian/ wheezy main' | sudo tee
/etc/apt/sources.list.d/hypriot.list
sudo apt-get update
sudo apt-get install -y docker-hypriot
sudo systemctl enable docker

cd "${HOME}/tmp"
git clone git@github.com:lispmeister/rpi-nginx.git
cd rpi-nginx
sudo make
sudo make build
sudo make version
sudo docker run -d -p 80:80 hypriot/rpi-busybox-httpd
