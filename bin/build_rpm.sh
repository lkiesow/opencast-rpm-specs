# Compile, install actual rpm version on centos6
cd ~

sudo yum groupinstall Base 'Development Tools'
sudo yum install zlib-devel nss-devel nspr-devel libarchive-devel db4-devel file-devel popt-devel

git clone git://rpm.org/rpm.git
cd  rpm
./autogen.sh --noconfigure
./configure --without-archive --with-external-db --without-lua CPPFLAGS="-I/usr/include/db4 -I/usr/include/nspr4 -I/usr/include/nss3"
make
sudo make install

# export LD_LIBRARY_PATH="$LD_LIBRARY_PATH /usr/local/lib"
#
# https://bugzilla.redhat.com/show_bug.cgi?id=54080/7
# $ rpmspec -q --buildrequires my.spec
#
# which should be just a convenient alias to
#
# $ rpmspec -q --srpm --requires my.spec
#
# Both worked for me with rpmspec from rpm-build-4.11.1-7.fc20.x86_64
# package.

# If yum takes long time to search the right mirrors:
#sudo rm -f /var/lib/rpm/__*
#sudo rpm --rebuilddb -v -v
#sudo yum clean all

