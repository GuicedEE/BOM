# GuicedEE 2.6.0 consumer reference alignment

Completed locally on 15 November 2026. No deployment, publication, push, or tag was performed.

The remaining platform references were corrected in **63 POMs** across JWebMP, ActivityMaster, EntityAssist, GuicedEE examples, and outlying service/test consumers. The existing 121 core release modules already declared 2.6.0.

- Consumer GuicedEE parent, Versioner, and BOM selections now use 2.6.0. Independent application/library artifact versions remain unchanged.
- **45 example BOM imports** now use `${guicedee.version}`: 44 previously used `${project.version}`, and GraphQL/Basic hardcoded 2.5.0.
- The Angular Maven plugin now imports GuicedEE 2.6.0 and is included in the root JWebMP profile, so consumer verification rebuilds it.
- The two EntityAssist website checkouts now declare `maven.asm.version=9.11.1`. Their standalone models previously failed because importing a BOM did not supply this property for compiler-plugin dependencies. Official Apache Maven plugin versions were preserved.
- The generated KaTeX dependency now matches ngx-markdown 22's supported range, `>=0.16.0 <0.19.0`. This fixes the strict npm resolution failure encountered during the website build.
- Failed npm commands now throw for both standard and application-only Angular workspaces. Three process-based regression tests cover failure and success; the previous standard-workspace path could print Maven `BUILD SUCCESS` without a browser bundle.

## Verification

Maven 4.0.0-rc-7 wrapper, Oracle JDK 25, Node 24.22.1. Isolated fixture directories contain copied source POMs/resources and their own `.mvn` roots/configuration; they do not include the GuicedEE framework reactor. Maven checks used offline resolution against the existing local repository, without GuicedEE version overrides. The frontend used normal npm dependency resolution, with no `--force` or `--legacy-peer-deps`.

| Check | Result |
| --- | --- |
| JWebMP and ActivityMaster parent/BOM local installs | Passed from isolated copies |
| Angular Maven plugin compile/package/install | Passed from isolated source; installed POM selects 2.6.0 and installed JAR SHA-256 matches the built JAR |
| Current website application and plugin dependency graphs | All selected GuicedEE artifacts at 2.6.0; nine in the plugin graph |
| All 45 changed example effective models | Platform selections at 2.6.0 |
| Eight additional isolated consumer/plugin effective models | Passed; existing upstream-versioned managed alias noted below |
| Inject, Config, and CDI examples | `verify` passed, full runtime jlink images created, and all three images ran and shut down successfully |
| Generator tests | 10 passed, zero failures/errors/skips, including three new npm process tests |
| Isolated GuicedEE website | Java compilation, Guice bootstrap, TypeScript generation, strict npm install, and Angular production build passed |
| Generated frontend dependency tree | `npm ls --depth=0` passed; Angular 22.2.6, ngx-markdown 22.1.1, KaTeX 0.18.10 |
| Failure propagation through the rebuilt Maven plugin | Fake npm exit 23 caused Maven exit 1 and `BUILD FAILURE` |
| Root JWebMP reactor validation | Passed with the Angular Maven plugin included |
| Project versions / official Maven plugin declarations | Unchanged in all 63 edited POMs |

The example projects contain no unit tests: their validation above is compilation, packaging, jlink, and actual execution. Other websites were checked as effective models, not full frontend/application builds. This is not a fresh-cache publication or production acceptance test.

## Retained references and warnings

- `website-backend-jlink` still selects `website-backend:2.5.0`, matching that application's artifact version. The backend framework property/model selects GuicedEE 2.6.0. Application artifact versions are independent of framework dependency versions.
- The StandaloneBOM contains an existing, unused managed alias `com.guicedee.modules.services:jSerialComm:2.11.4` driven by the upstream `jserialcomm.version` property. It is recorded as an explicit exception in the model assertions; it is not present in the verified website application/plugin graphs. The actual serial library uses `com.fazecast:jSerialComm`. No nonexistent 2.6.0 wrapper was substituted.
- Historical release documentation, independent Maven-plugin versions, and the private WASI experiment's baseline were not rewritten.
- Existing website Angular template/CommonJS/CSS warnings and logging stream-close messages during shutdown remain. They did not prevent the verified production output. This change does not claim to resolve those separate issues.

## Local evidence and repeat commands

Evidence is under `target/guicedee-2.6.0-fixes-2026-11-15/` at the DevSuite root:

- `verification-summary.json`, `consumer-model-check.json`, `example-model-check.json`.
- `before/`, `changed-poms.json`, and `reference-fixes.patch` preserve the task's POM baseline and changes without mixing in earlier workspace edits.
- `install-angular-plugin.log`, `install-angular.log`, `install-markdown.log`.
- `website-app-dependencies.txt`, `website-plugin-dependencies.txt`, `website-build-verified.log`, and `website-npm-tree.log`.
- `inject-verify.log`, `config-verify.log`, `cdi-verify.log`, and matching `*-runtime.log` files.
- `website-expected-npm-failure.log` and `npm-failure-check.json` record the deliberately failing acceptance check.

From `target/guicedee-2.6.0-fixes-2026-11-15/isolated/website`:

```powershell
& C:/Java/DevSuite/mvnw.cmd -B -ntp -o -N dependency:tree '-Dincludes=com.guicedee*:*'
& C:/Java/DevSuite/mvnw.cmd -B -ntp -o -N dependency:resolve-plugins '-DincludeArtifactIds=angular-maven-plugin'
& C:/Java/DevSuite/mvnw.cmd -B -ntp -o -N package com.jwebmp.plugins:angular-maven-plugin:2.0.3-SNAPSHOT:build '-Djwebmp.angular.docker=false' '-Dmaven.javadoc.skip=true' '-Dcentral.publishing.skip=true' '-Dmaven.deploy.skip=true'
```

The verified browser output is `isolated/website/target/webroot/guicedee-website/dist/jwebmp/browser/` within the evidence directory. It contains `index.html` and a hashed production `main-*.js` bundle.

From the DevSuite root, reactor validation requires keeping the profile-owning root project selected with Maven 4:

```powershell
.\mvnw.cmd -B -ntp -o '-Pjwebmp-boms,jwebmp' -pl '.,:angular-maven-plugin' -am validate '-Dcentral.publishing.skip=true' '-Dmaven.deploy.skip=true'
```
