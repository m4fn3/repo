apt-ftparchive packages ./debs > Packages
bzip2 -kf Packages
gzip -c Packages > Packages.gz