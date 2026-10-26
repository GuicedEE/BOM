# Final dependency refresh for GuicedEE 2.4.0

Reviewed on 14 October 2026 against live Maven Central metadata and upstream
release documentation. This refresh keeps the release coordinates at 2.4.0.
Maven plugin versions, plugin-only helpers and the Hibernate enhancement plugin
pin remain unchanged. ASM is a runtime library used by the managed dependency graph.

## Selected versions

| Dependency | Previous | Selected |
| --- | --- | --- |
| ASM | 9.10.1 | 9.11 |
| OWASP Java HTML Sanitizer | 20260924.2 | 20261011.1 |
| Byte Buddy | 1.18.14 | 1.18.15 |
| Apache Tika | 3.3.2 | 3.3.3 |
| SpotBugs and its annotations | 4.10.4 | 4.10.5 |
| Hibernate Validator | 9.1.4.Final | 9.1.5.Final |
| Commons Codec | 1.22.1 | 1.23.0 |
| Jakarta JSON Binding API | 3.0.3 | 3.0.4 |
| Kafka clients | 4.3.1 | 4.4.0 |
| IBM MQ clients | 10.0.0.5 | 10.0.1.0 |
| CloudEvents | 5.0.0 | 5.1.0 |
| Keycloak provider APIs | 26.8.0 | 26.8.1 |
| Spring Framework | 6.2.19 | 7.0.9 |
| FastDoubleParser | 1.0.90 | 2.0.1 |

The OWASP version is date based; this is a newer stable release, rather than a
semantic major-version migration. Byte Buddy uses its normal Java artifact,
without the legacy `jdk5` variant. All members of managed dependency families
must publish the selected version.

## Major version decisions

Spring 7.0.9 matches the version declared by the existing Apache CXF 4.2.4
[parent POM](https://repo.maven.apache.org/maven2/org/apache/cxf/cxf-parent/4.2.4/cxf-parent-4.2.4.pom).
ApacheCXFBOM imports Spring's framework BOM so consumers receive the complete
coordinated family alongside the explicit Spring dependencies in the CXF wrappers.
Its wrapper and SOAP consumer are checked against the selected runtime.

FastDoubleParser 2 retains the existing parser classes in the upstream JAR;
the [2.0.0 release](https://github.com/wrandelshofer/FastDoubleParser/releases/tag/v2.0.0)
adds configurable locale parsing, and
[2.0.1](https://github.com/wrandelshofer/FastDoubleParser/releases/tag/v2.0.1)
corrects configurable-parser edge cases. The Hazelcast wrapper is its current consumer.

Other major-version candidates stay on their existing compatible lines:

- SmallRye Config 4 adds a separate MicroProfile integration artifact. The current
  wrapper publishes the combined API and SPI surface, so that migration needs its own port.
- XML Resolver 6 removes public resource, resolver and cache classes from version 5.
  CXF's existing wrapper retains the version 5 API surface.
- JLine 4 removes JNA/Jansi terminal providers. The existing Hazelcast terminal
  integration retains JLine 3; changing provider behavior needs separate runtime validation.
- CDI 5, Tika 4 and JavaFX 26 would advance broader platform contracts beyond the
  current Jakarta, content-parsing and JavaFX baselines.
- Groovy 2.5 and 3 publish `groovy-all` as a POM, while the Hazelcast wrapper needs
  the 2.4 JAR. Updating this requires changing the dependency layout rather than its version.
- The Swagger fork's available version families do not align across all currently
  managed Jakarta artifacts; keep the coordinated 3.0.0 family.

Nightlies, timestamp builds, snapshots and prereleases were excluded. Historical
and unavailable legacy coordinates were retained rather than guessed.

## Evidence and verification

Metadata, candidate lists, selected properties and build logs are recorded under
`target/release-2.4.0/dependency-refresh`. Maven Central metadata is the version source,
for example [Kafka clients](https://repo.maven.apache.org/maven2/org/apache/kafka/kafka-clients/maven-metadata.xml)
and [Keycloak APIs](https://repo.maven.apache.org/maven2/org/keycloak/keycloak-core/maven-metadata.xml).
The pre-refresh Versioner snapshot records the unchanged plugin pins.

Same-version packaging preserves generated artifacts before rebuilding so the
shade plugin consumes fresh project JARs and sources. The artifact audit and
consumer checks must run against these new outputs, not the preserved archive.

The completed refresh passed:

- Full release packaging and the 117-component / 102-JPMS-JAR artifact audit.
- Installation of the 71-module consumer reactor, plus website backend and other
  website compilation checks.
- 47 focused framework tests, including SOAP requests, broker-backed Kafka and
  IBM MQ messaging, Hazelcast startup/maps, and ClassGraph/Hibernate discovery.
- Nine MCP protocol and transport tests.
- Java 25 runtime checks for Spring bean creation/shutdown, legacy and locale-aware
  number parsing, Byte Buddy class generation and ASM class reading.
- Website Java generation and the production Angular build, with the selected
  versions present in the generated release content.

All 36 recorded plugin-related version pins match the pre-refresh snapshot.
Maven Central publication completed on 14 October 2026: all 117 release components
and 423 public files were verified against the prepared SHA-256 hashes. The website
frontend was subsequently deployed and verified on 14 October 2026. IntelliJ
Marketplace publication remains pending. See
[the release guide](../RELEASE-2.4.0.md#publication) for deployment IDs and Central's
monthly publishing-limit warning.
