# Dependency refresh 2026-11-13

Updated 12 central dependency and third-party plugin properties. Official Apache Maven plugin versions, project release versions and JDK versions are unchanged. Existing workspace edits preserved.

## Changes

| Setting | Before | After |
|---|---|---|
| animalsniffer.version | 1.29 | 1.29.1 |
| azure-security-keyvault-keys.version | 4.12.1 | 4.13.0 |
| bcprov.18.version | 1.86 | 1.87 |
| bouncycastle.version | 1.86 | 1.87 |
| build.helper.maven.plugin.version | 3.7.0 | 3.8.0 |
| exec-maven-plugin.version | 3.6.4 | 3.7.0 |
| graphql.java.version | 26.1 | 26.2 |
| jandex.version | 3.6.0 | 3.6.1 |
| lang.version | 3.21.0 | 3.22.0 |
| maven.versions.version | 2.24.0 | 2.25.1 |
| microprofile.jwt.version | 2.2 | 2.2.1 |
| msal4j.version | 1.26.0 | 1.26.1 |

## Audit and retained settings

Live Maven Central metadata checked for 474 coordinates governed by 274 central properties across 461 POMs; zero XML scan errors and zero unresolved coordinate usages. Evidence is in `target/version-update-2026-11-13/`. This central-property audit does not establish exhaustive freshness of local overrides or hardcoded versions.

Groovy retained for packaging compatibility; Undertow retained because its coordinated artifacts have differing available versions. Major upgrades retained for separate migration work. No downgrades or suffix-only changes applied. Hibernate ORM/enhancer, ASM and OpenTelemetry have no eligible coordinated update.

Unmapped numeric settings retained (no discovered central coordinate usage; no freshness claim):

- `maven.jar.version`: `3.5.0`
- `maven-shade-transformers`: `0.0.3`
- `aop.version`: `1.0.0`
- `dropwizard.version`: `4.2.40`
- `bcprov.15.version`: `1.70`
- `bcprov.16.version`: `1.46`
- `slf4j.log4j2.version`: `2.26.1`
- `maven.hibernate.jpa.persistence.version`: `1.0.2.Final`
- `jackson.annotations.version`: `2.22`
- `jakarta.com.sun.activation.version`: `2.0.1`
- `jakarta.xml.jaxws.api.version`: `4.0.3`
- `primefaces.version`: `11.0.24`
- `qdox.version`: `2.2.0`
- `jcache.api.version`: `1.1.1`
- `mssql.driver.jdbc`: `11.2.4`
- `logmanager.processor.version`: `3.0.4.Final`
- `jbosslog.version`: `3.6.3.Final`
- `junit.platform.version`: `6.1.3`
- `selenium.jupiter.version`: `5.1.1`
- `flatten-maven-plugin.version`: `2.0`
- `vertx.mutiny.version`: `3.23.1`

Metadata exceptions retained without version changes:

- `antlr:antlr`: current version absent from metadata
- `net.sourceforge.barbecue:barbecue`: HTTP Error 404: Not Found
- `net.sf.barcode4j:barcode4j-light`: HTTP Error 404: Not Found
- `org.glassfish:jakarta.el`: current version absent from metadata
- `jakarta.faces:jakarta.faces-api`: current version absent from metadata
- `org.glassfish.web:jakarta.servlet.jsp`: current version absent from metadata
- `net.shibboleth.utilities:java-support`: current version absent from metadata
- `org.hibernate.common:hibernate-commons-annotations`: current version absent from metadata
- `ca.juliusdavies:not-yet-commons-ssl`: current version absent from metadata
- `org.opensaml:openws`: current version absent from metadata
- `org.opensaml:opensaml-xmlsec-api`: current version absent from metadata
- `org.opensaml:opensaml-core`: current version absent from metadata
- `org.opensaml:opensaml-messaging-api`: current version absent from metadata
- `org.opensaml:opensaml-security-api`: current version absent from metadata
- `io.undertow:undertow-parser-generator`: current version absent from metadata
- `org.apache.wss4j:wss4j-bindings-wss10`: current version absent from metadata
- `org.apache.wss4j:wss4j-bindings-wsu10`: current version absent from metadata
- `org.apache.wss4j:wss4j-bindings-wss11`: current version absent from metadata
- `org.apache.wss4j:wss4j-bindings-wssc`: current version absent from metadata

## Validation

- BOM/parent reactor install passed with Maven wrapper 4.0.0-rc-7.
- Persistence effective POM generated successfully.
- Client tests: 137 passed, zero failures/errors/skips.
- Frozen central plugin properties verified unchanged against the pre-audit snapshot.
- Framework/services forced JAR rebuild and install: all 118 reactor projects passed (tests and Javadoc skipped; 4 minutes 55 seconds).
- No publication or production verification performed.

Persistence tests attempted after rebuild: 32 tests, zero failures, 9 errors, 1 skipped. Testcontainers could not find a valid Docker environment; this is an environment-blocked run, not a test pass. See persistence-tests.log.

