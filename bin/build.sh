#!/bin/bash 

# Idea
#
# install()
# {
#       spec file exists? {
#               for all needed packages in spec file call install(package)
#               returns if package is installed localy from spec
#               compile, build, install rpm 
#       } else {
#               if package is not installed, then install it via yum
#       }
# }

# paths
specdir=$HOME/matterhorn-rpms/specs/
sourcedir=~/rpmbuild/SOURCES/
# default /usr/local is prefered
export PATH="/bin:/sbin:/usr/bin:/usr/sbin:$PATH"

# debug, be more verbose
debug="1"

# compilation flags
# compile in N threads
export MAKEOPTS="-j5"
#export CFLAGS="-O2 -pipe"
#export CXXFLAGS="${CFLAGS}"
#export CHOST="x86_64-pc-linux-gnu"

# reporting message
function message()
{
    echo "$(date +%F-%T) M: $@"
}

# error, exit script
function error()
{
    echo "$(date +%F-%T) E: $@"
    exit 1
}

# code execution, automatic error handler
function xeval()
{
    cmd=$@
    [ "$debug" == "1" ] && echo "$(date +%F-%T) D: $cmd"
    eval $cmd || error "$cmd"
}

# install spec file
function install_specs()
{
    rpm="$1"
    specfile="$2"

    message "Install spec $specfile, rpm $rpm"

    line="$(yum list installed $rpm | egrep "^$rpm.*")" 
    message "Package list item from yum: $line"

    # application was installed locally? (via rpm from spec file)
    if echo "$line" | egrep "^$rpm.*(@/$rpm|installed)" >& /dev/null; then
	echo "Package $rpm installed from spec, skip package"
	return 0
    elif [ -n "$line" ]; then
	echo "package $prm installed via online repo, remove and install via specs"
	# remove package without dependencies
	#sudo yum remove -y $rpm
	xeval "sudo rpm -e $rpm --nodeps"
    fi

    # Get source(s)
    cd "$sourcedir"
    xeval "spectool --all --get-files $specfile"

    # Get dependencies
    cd "$specdir" 
    xeval "sudo yum-builddep -y $specfile"

    # Build package
    xeval "rpmbuild -ba $specfile"

    # Install package
    xeval "sudo yum localinstall -y ~/rpmbuild/RPMS/x86_64/*${rpm}*"
}

# Install required packages pro running 
function init()
{
    # Install basic packages
    xeval "sudo yum install -y rpmdevtools.noarch rpmlint.noarch createrepo.noarch vim"

    # Setup build dirs
    cd ~
    xeval "rpmdev-setuptree"

    # Enable EPEL and Rpmforge repositories.
    #sudo yum localinstall --nogpgcheck \
    #  http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
    if ! yum list installed epel-release.noarch >& /dev/null; then
        cd /tmp/
        xeval "wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
        xeval "sudo rpm -Uvh epel-release-6*.rpm"
    fi

    # Copy patches to working directory
    cd "$sourcedir"
    xeval "cp $HOME/matterhorn-rpms/patch/*.patch ./"
    
    # make tmdir for spectool from localy compiled rpm
    [ ! -d "/usr/local/var/tmp/" ] && 
        xeval "sudo mkdir -p /usr/local/var/tmp/"
    xeval "chmod 1777 /usr/local/var/tmp/"
}

# help
function help()
{
    echo "$0 init | package"
    echo "$0 init"
    echo "$0 ffmpeg"
    exit 0
}

# main function, the base of recursion
function main() 
{
    local target="$1"

    message "Start with target $target"

    # spec file exists?
    # remove -devel suffix (devel version goes from its original package)
    # add suffix .spec
    local specfile="$specdir/${target%%-devel}.spec"
    if [ -f "$specfile" ]; then
        message "Specfile $specfile exists, following dependencies"
        # Solve dependencies via rekursion calls
        breqs="$(/usr/local/bin/rpmspec -q --buildrequires $specfile)"
        rc=$?
        [ "$rc" != "0" ] && error "rpmspec -q --buildrequires returns $rc"
        for breq in $(echo "$breqs" | cut -d' ' -f1); do
            message "Run main $breq"
            main $breq
        done
        install_specs $target $specfile 
    else
        message "Install target $target via yum"
        xeval "sudo yum install -y -q $target"
    fi
}

# get user target 
target="$1"

# target is required
[ -z "$target" ] && help

# init
if [ "$target" = "init" ]; then
    init
    exit 0
fi

# start interation no 1
main $target

