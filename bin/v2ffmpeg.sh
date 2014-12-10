#!/bin/bash -e

# Variables
specdir=$HOME/matterhorn-rpms/specs/
sourcedir=~/rpmbuild/SOURCES/

# separator
oldIFS="$IFS"

function message()
{
    echo "$(date +%F-%T) M: $@"
}

function install_specs()
{
    rpm="$1"	

    message "Install specs $rpm"

    # application installed from local rpm?
    if yum list installed $rpm | egrep "^$rpm.*(@/$rpm|installed)" >& /dev/null; then
	echo "package $rpm installed from specs, continue"
	continue
    else
	echo "package $prm installed via online repo, remove and install via specs"
	sudo yum remove -y $rpm
    fi

    # Get source(s)
    cd "$sourcedir" && spectool --all --get-files "$specdir/${rpm}.spec"

    # Get dependencies
    cd "$specdir" && sudo yum-builddep -y ${rpm}.spec

    # Build package
    rpmbuild -ba "$specdir/${rpm}.spec"

    # Install package
    sudo yum localinstall -y ~/rpmbuild/RPMS/x86_64/*${rpm}*
}

# Install basic packages
sudo yum install -y rpmdevtools.noarch rpmlint.noarch createrepo.noarch vim

# Setup build dirs
cd ~
rpmdev-setuptree

# Enable EPEL and Rpmforge repositories.
#sudo yum localinstall --nogpgcheck \
#  http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm

if ! yum list installed epel-release.noarch >& /dev/null; then
    cd /tmp/
    wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    sudo rpm -Uvh epel-release-6*.rpm
fi

# Copy patches to working directory
cd "$sourcedir"
cp $HOME/matterhorn-rpms/patch/*.patch ./

# We solve dependencies with this order
# 1) make rpm via specs, required if patches are needed
# 2) online repository, yum install
# 3) download rpm,  yum localinstall

# external rpms dependencies. RPMS storage is inside direcotry ./rpms
# package depends_on_rpms
#faad2 id3lib*
#gpac js-*
bdependencies="
"
IFS="
"
for d in $bdependencies; do
    target="$(echo "$d" | cut -d' ' -f1)"
    rpms="$(echo "$d" | cut -d' ' -f2-)"
    message "Install localinstall $rpms"
    sudo yum localinstall ~/matterhorn-rpms/rpms/$rpms
done

# First install these specs packages
# package depends_on_specs
#gpac xvidcore
sdependencies="
"
for d in $sdependencies; do
    target="$(echo "$d" | cut -d' ' -f1)"
    specs="$(echo "$d" | cut -d' ' -f2-)"
    for s in $specs; do
        install_specs $s
    done
done

# We have patches for these packages, install it via specs
# Packages order is important
# Remove gpack, can not download sources and 
#pack_with_patches="libgdither libmad a52dec faac faad2 gavl gpac x264"
pack_with_patches="libgdither libmad a52dec faac faad2 gavl x264"

# Install specs in this order
list="$pack_with_patches"

IFS="$oldIFS"
for rpm in $list; do
    install_specs $rpm
done
