# Dependency refresh: 19 October 2026

Checked 262 central dependency properties covering 461 coordinates in 214 GuicedEE POMs against live Maven Central metadata. Applied stable same-major updates; retained plugin, enhancement-plugin, Javadoc and compatibility pins. Project release versions remain unchanged.

| Dependency | Previous | Selected |
| --- | --- | --- |
| Jackson 3 | 3.2.3 | 3.2.4 |
| Hibernate Reactive | 4.5.10.Final | 4.5.11.Final |
| Microsoft SQL Server JDBC and native authentication | 13.6.0 | 13.6.1 |
| OWASP Encoder | 1.5.0 | 1.6.0 |

Jackson's BOM continues to manage annotations at 2.22. Reactive 4.5.11.Final declares Hibernate ORM 7.4.13.Final, matching the existing central ORM pin. SQL Server's JRE 11 driver and x64 authentication artifact remain aligned through the shared property.

Groovy remains at 2.4.21 because newer `groovy-all` releases use POM packaging rather than the JAR required by the current dependency layout. Undertow remains at 2.3.26.Final: its newer core release is not shared by the managed servlet and WebSocket artifacts. Legacy metadata gaps and major-version candidates remain unchanged.

Validation: GuicedEE and JWebMP BOM/parent reactor installation, SQL Server wrapper packaging and local installation, 20 focused persistence tests, and the ClassGraph migration test passed. The effective persistence POM aligns Jackson 3 artifacts at 3.2.4. The unrestricted injection test run encountered `Guice context is stopped`; unrestricted suites were stopped before completion, so full-suite validation is not claimed.

Raw metadata, per-coordinate findings, source snapshot and build/test logs are retained locally under `target/version-update-2026-10-19/` at the DevSuite root.

Sources: [Jackson BOM](https://repo.maven.apache.org/maven2/tools/jackson/jackson-bom/3.2.4/jackson-bom-3.2.4.pom), [Hibernate Reactive POM](https://repo.maven.apache.org/maven2/org/hibernate/reactive/hibernate-reactive-core/4.5.11.Final/hibernate-reactive-core-4.5.11.Final.pom), [SQL Server metadata](https://repo.maven.apache.org/maven2/com/microsoft/sqlserver/mssql-jdbc/maven-metadata.xml), [OWASP Encoder metadata](https://repo.maven.apache.org/maven2/org/owasp/encoder/encoder/maven-metadata.xml).
