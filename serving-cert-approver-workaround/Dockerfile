#FROM registry.redhat.io/ubi8/ubi:latest
FROM image-registry.openshift-image-registry.svc:5000/openshift/ubi8:latest

#This is provided as-is with no support from Red Hat.
MAINTAINER "Muhammad Aizuddin Zali" <mzali@redhat.com>

# specify the version string of the oc release, set in the buildconfig environment.
# ENV OC_VERSION "4.1.9"

# install the oc client tools
ADD https://mirror.openshift.com/pub/openshift-v4/clients/ocp/$OC_VERSION/openshift-client-linux-$OC_VERSION.tar.gz /usr/bin/openshift-client-linux-$OC_VERSION.tar.gz
RUN tar -xzvf  /usr/bin/openshift-client-linux-$OC_VERSION.tar.gz  -C /usr/bin && \
    chmod +x /usr/bin/oc
   
USER 1001
