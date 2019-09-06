# OpenShift 4 integration with RH-SSO (MySQL Persistent) OIDC.

Brief steps taken:
* 1. Deploy RHSSO on OpenShift4
* 2. Configure RHSSO OIDC
* 3. Add RHSSO OIDC as oAuth provider

## Deploying RHSSO on OpenShift 4
* 1. create working dir
```
#> mkdir rhsso
#> cd rhsso
```

* 2. Create JKS and CA (for self-signed CA else known CA) for RHSSO use.
Create CA certificate for self-sign:
```
#> export SECRETS_KEYSTORE_PASSWORD=mystrongpasswordnoonecanbreakin
#> openssl req -new -newkey rsa:4096 -x509 -keyout xpaas.key -out xpaas.crt -days 365 -subj "/CN=xpaas-redhat-sso.ca" -passin pass:${SECRETS_KEYSTORE_PASSWORD} -passout pass:${SECRETS_KEYSTORE_PASSWORD}
```

Create keypair (replace CN with your route for SSO FQDN value):
```
#> keytool -genkeypair -keyalg RSA -keysize 2048 -dname "CN=secure-sso-<namespace>.<app_route_domain>" -alias sso-https-key -keystore sso-https.jks -storepass ${SECRETS_KEYSTORE_PASSWORD}
```  

Create CSR for signing:
```
#> keytool -certreq -keyalg rsa -alias sso-https-key -keystore sso-https.jks -file sso.csr -storepass ${SECRETS_KEYSTORE_PASSWORD}
```

Now, sign the CSR using CA created earlier:
```
#> openssl x509 -req -CA xpaas.crt -CAkey xpaas.key -in sso.csr -out sso.crt -days 365 -CAcreateserial -passin pass:${SECRETS_KEYSTORE_PASSWORD}
```

Create JKS for RHSSO use:
```
#> keytool -import -file xpaas.crt -alias xpaas.ca -keystore sso-https.jks -storepass ${SECRETS_KEYSTORE_PASSWORD}
#> keytool -import -file sso.crt -alias sso-https-key -keystore sso-https.jks -storepass ${SECRETS_KEYSTORE_PASSWORD}
#> keytool -import -file xpaas.crt -alias xpaas.ca -keystore truststore.jks -storepass ${SECRETS_KEYSTORE_PASSWORD}
#> keytool -genseckey -alias jgroups -storetype JCEKS -keystore jgroups.jceks -storepass ${SECRETS_KEYSTORE_PASSWORD}
```

* 3. Create new project and associate object for RHSSO:
```
#> oc new-project rhsso
#> oc create serviceaccount sso-sa
#> oc secret new sso-jgroup-secret jgroups.jceks
#> oc secret new sso-ssl-secret sso-https.jks truststore.jks
#> oc secrets link sso-sa sso-jgroup-secret sso-ssl-secret
```


* 4. Deploy new RHSSO apps:
```
#> oc new-app --template=sso73-mysql-persistent \
  -p APPLICATION_NAME=sso \
  -p HTTPS_KEYSTORE=sso-https.jks \
  -p HTTPS_PASSWORD=${SECRETS_KEYSTORE_PASSWORD} \
  -p HTTPS_SECRET=sso-ssl-secret \
  -p SSO_TRUSTSTORE_SECRET=sso-ssl-secret \
  -p JGROUPS_ENCRYPT_KEYSTORE=jgroups.jceks \
  -p JGROUPS_ENCRYPT_PASSWORD=${SECRETS_KEYSTORE_PASSWORD} \
  -p JGROUPS_ENCRYPT_SECRET=sso-jgroup-secret \
  -p SSO_REALM=OpenShift \
  -p SSO_SERVICE_USERNAME=openshift-admin \
  -p SSO_SERVICE_PASSWORD=$(openssl rand -base64 512 | tr -dc A-Z-a-z-0-9 | head -c 17) \
  -p SSO_ADMIN_USERNAME=admin \
  -p SSO_ADMIN_PASSWORD=admin123 \
  -p SSO_TRUSTSTORE=truststore.jks \
  -p SSO_TRUSTSTORE_SECRET=sso-ssl-secret \
  -p SSO_TRUSTSTORE_PASSWORD=${SECRETS_KEYSTORE_PASSWORD}
```

## Configuring RHSSO OIDC
* 1. Login to RHSSO via exposed HTTPS route using admin/password set above.

* 2. Select "OpenShift" realm, add user for login test later:
```
Manage > Users > Add User > Fill in all info > Save
```

* 3.Set password for the user. Always ensure 'Temporary' button always OFF.
```
Credentials > Enter New Password
```


* 4. Create and configure OIDC Client
```
Manage > Clients > Create > Client ID as "OpenShift" > Client Protocol as "openid-connect" > Access Type as "confidential" > Valid Redirect URIs  as "https://oauth-openshift.apps.ocp4.local.bytewise.my/*"
```

* 5. Get the clientSecret from the Credentials tab from above page and create as a secret:
```
#>  oc create secret  generic  rhsso-oidc-secret --from-literal=clientSecret=secret_here -n openshift-config
```

* 6. Configure OpenShift oAuth to include RHSSO OID:
```
#> cat oauth.yaml
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
    - mappingMethod: claim
      name: OPENID-IDP-01
      openID:
        ca:
          name: openid-ca-lkx8q
        claims:
          email:
            - email
          name:
            - name
          preferredUsername:
            - preferred_username
        clientID: openshift
        clientSecret:
          name: rhsso-oidc-secret
        extraScopes: []
        issuer: >-
          https://secure-sso-rhsso.apps.ocp4.local.bytewise.my/auth/realms/OpenShift
      type: OpenID 

#> oc apply -f oauth.yaml
```

* 7. After the oauth pods progressing with new config, console should have new OIDC login option.

## Troubleshooting

For troubleshooting:
```
Administration > Cluster Settings > Cluster Operators > authentication > Conditions
```
