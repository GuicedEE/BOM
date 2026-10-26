# Dependency refresh: 23 October 2026

Audited 262 central dependency properties covering 461 Maven coordinates in 214 GuicedEE POMs against live Maven Central metadata. Selected stable updates within existing major versions. Project release versions, build-plugin pins, enhancement-plugin pins and Javadoc-only pins are unchanged.

| Property | Previous | Selected |
| --- | --- | --- |
| `aspectj.version` | 1.9.25.1 | 1.9.26 |
| `batik.version` | 1.19 | 1.20 |
| `errorprone.version` | 2.50.0 | 2.51.0 |
| `fop.version` | 2.11 | 2.12 |
| `javafx.version` | 21.0.12 | 21.0.13 |
| `micrometer.version` | 1.17.1 | 1.17.2 |
| `okhttp.version` | 5.5.0 | 5.5.1 |
| `reactor.core.version` | 3.8.7 | 3.8.8 |
| `smallrye.mutiny.version` | 3.3.0 | 3.3.1 |
| `smallrye.reactive.version` | 4.0.2 | 4.1.0 |
| `spring.version` | 7.0.9 | 7.0.10 |
| `vertx.version` | 5.2.1 | 5.2.2 |

The [SmallRye bindings parent](https://repo.maven.apache.org/maven2/io/smallrye/reactive/smallrye-mutiny-vertx-bindings-projects/4.1.0/smallrye-mutiny-vertx-bindings-projects-4.1.0.pom) targets Vert.x 5.2.2 and Mutiny 3.3.1. The [FOP parent](https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/fop-parent/2.12/fop-parent-2.12.pom) targets Batik 1.20.

Groovy remains on 2.4.21 because the wrapper requires its JAR layout. Undertow remains on its existing coordinated pin: newer releases are not shared across all managed artifacts. Major-version migrations and legacy metadata gaps are retained for separate review.

Evidence is retained at the DevSuite root under `target/version-update-2026-10-23/`, including the original Versioner, live metadata, audit, selected versions, upstream POMs and build logs.

Validation completed:

- BOM and parent reactor installation passed.
- The 120-module GuicedEE BOM, JWebMP BOM, service-wrapper and framework reactor installed successfully with tests skipped. Javadoc generation was skipped.
- A subsequent 70-module service-wrapper reactor passed with `-Dmaven.jar.forceCreation=true`, ensuring incremental packaging did not reuse previously shaded JARs.
- Byte comparisons matched 934 Reactor classes, 157 Batik SVG generator classes and 70 Mutiny Vert.x core classes against the selected upstream JARs. The comparison excludes Reactor annotation metadata and the two existing Java-authored Mutiny overrides.
- The effective Vert.x consumer POM resolves Vert.x 5.2.2, Mutiny 3.3.1, bindings 4.1.0, Micrometer 1.17.2 and Jackson databind 3.2.4.
- All 42 tests across eight focused test classes passed with zero failures, errors or skips: Vert.x JSON, shutdown and event-bus behavior; metrics options; JDBC URL generation, named-client lookup and persistence lifecycle; SOAP integration.
- The Versioner diff contains exactly the 12 selected property changes, and `git diff --check` passes.

This is local build and focused test evidence; the full unrestricted test suite, production acceptance and publication were not run.
