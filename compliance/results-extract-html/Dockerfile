FROM registry.access.redhat.com/ubi8/ubi

RUN dnf install openscap-scanner -y --nodocs; dnf clean all

ENTRYPOINT [ "sleep 10" ]
