# https://hub.docker.com/_/centos?tab=tags
FROM centos:7

MAINTAINER ben

LABEL remarks="an example"

RUN yum -y install \
   python3 \
   python3-devel \
   zlib-devel \
   libjpeg-devel \
   centos-release-scl \
   python3-pip \
   poppler-utils \
   cmake3

RUN yum -y groupinstall 'Development Tools'

# cmake is required by poppler
# cmake3 is required. The build process looks for "cmake" instead of "cmake3"
# https://stackoverflow.com/a/59998607/1164295
#RUN ln -s /usr/bin/cmake3 /usr/bin/cmake


RUN alternatives --install /usr/local/bin/cmake cmake /usr/bin/cmake 10 \
--slave /usr/local/bin/ctest ctest /usr/bin/ctest \
--slave /usr/local/bin/cpack cpack /usr/bin/cpack \
--slave /usr/local/bin/ccmake ccmake /usr/bin/ccmake \
--family cmake

RUN alternatives --install /usr/local/bin/cmake cmake /usr/bin/cmake3 20 \
--slave /usr/local/bin/ctest ctest /usr/bin/ctest3 \
--slave /usr/local/bin/cpack cpack /usr/bin/cpack3 \
--slave /usr/local/bin/ccmake ccmake /usr/bin/ccmake3 \
--family cmake

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


