FROM ubuntu:devel

ARG BAT_VERSION
ARG FD_VERSION

COPY ogham-exa/ /opt/exa
COPY dalance-procs/ /opt/procs
COPY bat-v$BAT_VERSION-x86_64-unknown-linux-gnu/ /opt/bat
COPY fd-v$FD_VERSION-x86_64-unknown-linux-gnu/ /opt/fd

RUN mkdir -p /home/user && echo "user:x:1000:1000:user:/home/user:/bin/bash" >> /etc/passwd \
    && chown -R user /home/user \
    && echo "PATH=/opt/exa/bin/:/opt/procs/:/opt/bat/:/opt/fd/:$PATH" >> /home/user/.bashrc \
    && echo "alias cat=bat" >> /home/user/.bashrc \
    && echo "alias find=fd" >> /home/user/.bashrc \
    && echo "alias ps=procs" >> /home/user/.bashrc \
    && echo "alias ls=exa" >> /home/user/.bashrc \
    && chmod a+x /opt/exa/bin/exa \
    && chmod a+x /opt/procs/procs \
    && chmod a+x /opt/bat/bat \
    && chmod a+x /opt/fd/fd

WORKDIR /home/user
USER user
