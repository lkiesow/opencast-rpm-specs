#!/bin/sh

specdir=$HOME/matterhorn-rpms/specs/
sourcedir=~/rpmbuild/SOURCES/

# Get spec files
#cd ~
#git clone https://github.com/lkiesow/matterhorn-rpms.git

# Setup build dirs
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Setup spectool
yum install -y rpmdevtools
yum install -y vim

# Get sources from spec files

# orc: spectool lädt patches nicht herunter
# schroedinger: no spec
# enca: no spec
# lame: archive missing
# libfaac -> faac, disable patch

# Patches
cd "$sourcedir"
cp $HOME/matterhorn-rpms/patch/*.patch ./

# We have patches for these mackages
list1="a52dec faac faad2 gavl gpac libgdither libmad x264"

for rpm in $list1; do
    # Get source(s)
    cd "$sourcedir" && spectool --all --get-files "$specdir/${rpm}.spec"

    # Get dependencies
    cd "$specdir" && sudo yum-builddep -y ${rpm}.spec

    # Build package
    rpmbuild -ba "$specdir/${rpm}.spec"

    # Install package
    sudo rpm -i ~/rpmbuild/RPMS/x86_64/*${rpm}*
done

exit 0



# SRPMs
#wget ftp://download1.rpmfusion.org/pub/free/el/updates/6/SRPMS/gpac-0.4.6-0.13.cvs20100527.el6.3.src.rpm
#wget http://dl.atrpms.net/src/el6-x86_64/atrpms/stable/x264-0.142-20_20140406.2245.src.rpm


# rtmpdump
# -> need to install *rtmp* afterwards!

# libvpx
# removed second source: libvpx.ver

# frei0r-plugins: requires gavl-devel
# Uses an old version
# URL gives bad filename

# gavl: libgdither-devel

# libgdither.spec

# gpac: found srpm in the internet -> using it for rebuilding
# including the patches!

# x264: bootstrap

# by using the build deps of ffmpeg
for rpm in a52dec faad2 lame rtmpdump soxr libvpx opencore-amr \
    libgdither gavl frei0r-plugins vo-aacenc ; do

    sudo rpm -i  ~/rpmbuild-matterhorn/RPMS/x86_64/*$rpm*
done

for rpm in xvidcore vo-aacenc soxr fdk-aac faac; do
    # Get source(s)
    cd "$sourcedir" && spectool --all --get-files "$specdir/${rpm}.spec"

    # Get dependencies
    cd "$specdir" && sudo yum-builddep -y ${rpm}.spec

    # Build package
    rpmbuild -ba "$specdir/${rpm}.spec"

    # Install package
    sudo rpm -i ~/rpmbuild/RPMS/x86_64/*${rpm}*

    # Install package?
    #[root@vagrant-centos65 specs]# r=lame; yum-builddep -y ${r}.spec; rpmbuild -ba ${r}.spec; rpm -i ~/rpmbuild/RPMS/x86_64/*${r}*

done

# ffmpeg-nonfree ffmpeg-nonfree-libs fribidi lame libass librtmp libva libvpx libx264_138 openal-soft opencore-amr opus orc
