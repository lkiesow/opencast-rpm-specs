#!/bin/sh

specdir=$HOME/matterhorn-rpms/specs/
sourcedir=~/rpmbuild/SOURCES/

#specdir=$HOME/matterhorn-rpms/specs/
#sourcedir=~/rpmbuild/SOURCES/

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
wget http://www.linuxfromscratch.org/patches/blfs/svn/faac-1.28-glibc_fixes-1.patch -O faac-1.28-excessivedefines.patch
wget https://raw.githubusercontent.com/PhantomX/slackbuilds/master/a52dec/patches/a52dec-configure-optflags.patch -O a52dec-configure-optflags.patch
wget 'http://cvs.rpmfusion.org/viewvc/*checkout*/rpms/a52dec/devel/a52dec-0.7.4-rpath64.patch?revision=1.1&root=free' -O a52dec-0.7.4-rpath64.patch
wget 'http://cvs.rpmfusion.org/viewvc/*checkout*/rpms/faad2/F-17/faad2-pic.patch?root=free' -O faad2-pic.patch
wget 'https://raw.githubusercontent.com/PhantomX/slackbuilds/master/libgdither/patches/libgdither-0.6-default.patch' -O libgdither-0.6-default.patch
wget 'https://raw.githubusercontent.com/PhantomX/slackbuilds/master/libgdither/patches/libgdither-0.6-gavl.patch'
wget 'https://raw.githubusercontent.com/PhantomX/slackbuilds/master/gavl/patches/gavl-1.1.1-system_libgdither.patch'
wget 'http://cvs.rpmfusion.org/viewvc/*checkout*/rpms/x264/F-17/x264-nover.patch?revision=1.6&root=free' -O x264-nover.patch
wget 'http://cvs.rpmfusion.org/viewvc/*checkout*/rpms/x264/devel/x264-gpac.patch?root=free' -O x264-gpac.patch

wget 'http://cvs.rpmfusion.org/viewvc/*checkout*/rpms/libmad/devel/libmad-0.15.1b-multiarch.patch?revision=1.2&root=free' -O libmad-0.15.1b-multiarch.patch
wget 'http://cvs.rpmfusion.org/viewvc/*checkout*/rpms/libmad/devel/libmad-0.15.1b-ppc.patch?revision=1.1&root=free' -O libmad-0.15.1b-ppc.patch

# SRPMs
wget ftp://download1.rpmfusion.org/pub/free/el/updates/6/SRPMS/gpac-0.4.6-0.13.cvs20100527.el6.3.src.rpm
wget http://dl.atrpms.net/src/el6-x86_64/atrpms/stable/x264-0.142-20_20140406.2245.src.rpm


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
