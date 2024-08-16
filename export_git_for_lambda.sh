# run inside the development container
ldd $(which git)
mkdir -p my_git/usr/bin
cp $(which git) my_git/usr/bin/
mkdir -p my_git/lib
for lib in $(ldd $(which git) | grep "=> /" | awk '{print $3}'); do cp --parents "$lib" my_git/; done
cp -r /etc/gitconfig my_git/etc/
cp -r ~/.config/git my_git/.config/