FROM golang:1.8
MAINTAINER jacob_shih "jacob_shih@hotmail.com"

# update ubuntu software repository
RUN apt-get update

# install necessary tools
RUN apt-get install -y \
    apache2 \
    python-pip \
    python3 python3-pip \
    vim \
    tzdata \
    sudo

# add user
RUN useradd -c 'docker user' -m -d /home/user -s /bin/bash user

# allow sudo usage
RUN echo "user ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/user
RUN chmod 0440 /etc/sudoers.d/user

# reconfigure to use bash
RUN echo no | dpkg-reconfigure dash

# initialize the user profile from the skeleton profile
RUN cp /etc/skel/.bashrc /home/user/.bashrc \
  && echo 'PATH="/usr/local/go/bin:$GOPATH/bin:$HOME/bin:$PATH"' >> /home/user/.bashrc

# apache2 settings are from https://github.com/pyohei/docker-cgi-python
# http settings
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
RUN mkdir -p $APACHE_RUN_DIR $APACHE_LOCK_DIR $APACHE_LOG_DIR

# copy apache2 configuration files.
#   apache2/apache2.conf
#   apache2/sites-available/000-default.conf
#   apache2/sites-available/default-ssl.conf
#   apache2/conf-available/serve-cgi-bin.conf
#   apache2/mods-available/mime.conf
COPY apache2 /etc/apache2
RUN ln -s /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled/cgi.load

# setup alias for folders
ENV HOME /home/user
ENV MAXI22 $HOME/maxi22

# create working folders
RUN mkdir -p \
    $MAXI22 \
    $MAXI22/muffin \
    $MAXI22/pastry \
    $MAXI22/lychee \
    $MAXI22/go

# setup go path
ENV GOPATH $MAXI22/go
RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"

# setup http document folder
ENV MAXI22_ROOT      $MAXI22
ENV MAXI22_HTML_ROOT $MAXI22_ROOT/muffin
ENV MAXI22_CGI_ROOT  $MAXI22_ROOT/pastry
ENV MAXI22_LIB_ROOT  $MAXI22_ROOT/lychee

# setup working directories
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH
WORKDIR $MAXI22

# set timezone
# ENV TZ=Asia/Taipei
# RUN dpkg-reconfigure -f noninteractive tzdata

# run as a user
# CMD ["su", "user", "-c", "/bin/bash"]

# http port
EXPOSE 80

STOPSIGNAL SIGTERM

ENTRYPOINT [ "/usr/sbin/apache2" ]
CMD ["-D", "FOREGROUND"]
