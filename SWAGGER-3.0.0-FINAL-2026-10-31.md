# Swagger Core 3.0.0 final

Replaced `io.swagger.version`'s timestamped snapshot with the Maven Central
release `3.0.0`. `io.swagger.jakarta.version` continues to alias it, so all six
official Swagger artifacts stay aligned. Removed the snapshot repository from
the shaded wrapper. GuicedEE release versions and other dependency pins are
unchanged.

Validated on Java 25 using the pinned Maven 4.0.0-rc-7 wrapper:

- Installed Versioner and Swagger BOM; checked the effective wrapper POM.
- Rebuilt and installed Swagger and CXF OpenAPI wrappers, including sources and
  Javadocs, forcing fresh JAR creation.
- Passed all 82 affected tests: OpenAPI 7, REST 74, Swagger UI 1; no failures,
  errors or skips.
- Verified all 333 embedded Swagger classes against the five official release
  JARs and verified those JARs against Maven Central checksums.
- Verified matching SHA-256 hashes for the built, installed and tested wrapper.
- Confirmed the named wrapper descriptor and absence of upstream Swagger runtime
  dependencies or snapshot repositories in its installed POM.
- Passed the CXF classpath smoke for extension discovery, feature construction
  and REST context construction.

Evidence: `DevSuite/target/swagger-final-2026-10-31/`.
See `GuicedEE/openapi/docs/swagger-core-3-migration.md` for details and retained
limitations. No publication or deployment is claimed.

Related thread: https://github.com/swagger-api/swagger-core/issues/4991.
