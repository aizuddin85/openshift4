FROM registry.redhat.io/ubi8/ubi:latest

#This is provided as-is with no support from Red Hat.
MAINTAINER "Muhammad Aizuddin Zali" <mzali@redhat.com>

# specify the version string of the oc release
ENV OC_VERSION "4.1.9"


# install the oc client tools
ADD https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux-$OC_VERSION.tar.gz /usr/bin/openshift-client-linux-$OC_VERSION.tar.gz
RUN tar --strip-components=1 -xzvf  /usr/bin/openshift-client-linux-$OC_VERSION.tar.g  -C /usr/bin && \
    chmod +x /usr/bin/oc

USER 1001
