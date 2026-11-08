from pathlib import Path
import concurrent.futures as cf
import collections
import argparse
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Audit centralized GuicedEE dependency properties against Maven Central.')
parser.add_argument('--root', type=Path, default=Path.cwd())
parser.add_argument('--out', type=Path, required=True)
parser.add_argument('--inventory-only', action='store_true')
args = parser.parse_args()
ROOT = args.root.resolve()
OUT = args.out.resolve()
OUT.mkdir(parents=True, exist_ok=True)
VERSIONER = ROOT / 'GuicedEE/bom/Versioner/pom.xml'
NS = {'m': 'http://maven.apache.org/POM/4.0.0'}
raw = VERSIONER.read_bytes()
if not (OUT / 'versioner-before.xml').exists():
    (OUT / 'versioner-before.xml').write_bytes(raw)
versioner = ET.fromstring(raw)
for e in versioner.iter(): e.tag = '{http://maven.apache.org/POM/4.0.0}' + e.tag.split('}')[-1]
props = {e.tag.split('}')[-1]: e.text.strip() for e in versioner.find('m:properties', NS) if e.text}
usages = collections.defaultdict(list)
official_plugin_props = set()
scan_errors = []
unresolved_usages = []
pom_count = 0
additional_usages = []
property_references = collections.defaultdict(list)

def value(node, key):
    return node.findtext('m:' + key, '', NS).strip()

def resolve(s, env):
    for _ in range(8):
        newer = re.sub(r'\$\{([^}]+)\}', lambda m: env.get(m[1], m[0]), s)
        if newer == s: break
        s = newer
    return s

for directory, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in {'target','.git','.gradle','build','node_modules','.idea','dist','.worktrees','.venv','venv'}]
    if 'pom.xml' not in files: continue
    p = Path(directory) / 'pom.xml'
    try: model = ET.parse(p).getroot()
    except ET.ParseError as error:
        scan_errors.append({'pom': str(p.relative_to(ROOT)), 'error': str(error)})
        continue
    # Handle both Maven 4.0 and 4.1 XML namespaces.
    for e in model.iter(): e.tag = '{http://maven.apache.org/POM/4.0.0}' + e.tag.split('}')[-1]
    pom_count += 1
    env = dict(props)
    ancestor = p.parent
    chain = []
    visited = {p.resolve()}
    parent_model = model
    while True:
        parent = parent_model.find('m:parent', NS)
        if parent is None: break
        relative = parent.find('m:relativePath', NS)
        if relative is not None and not relative.text: break
        candidate = (ancestor / (relative.text.strip() if relative is not None else '../pom.xml')).resolve()
        if candidate in visited or not candidate.is_file(): break
        visited.add(candidate)
        try: parent_model = ET.parse(candidate).getroot()
        except ET.ParseError: break
        for element in parent_model.iter(): element.tag = '{http://maven.apache.org/POM/4.0.0}' + element.tag.split('}')[-1]
        chain.append(parent_model)
        ancestor = candidate.parent
    for parent_model in reversed(chain):
        for element in parent_model.findall('m:properties/*', NS):
            if element.text: env[element.tag.split('}')[-1]] = element.text.strip()
    for e in model.findall('m:properties/*', NS):
        if e.text: env[e.tag.split('}')[-1]] = e.text.strip()
    for plugin in model.findall('.//m:plugin', NS):
        group = resolve(value(plugin, 'groupId') or 'org.apache.maven.plugins', env)
        if group == 'org.apache.maven.plugins':
            official_plugin_props.update(re.findall(r'\$\{([^}]+)\}', value(plugin, 'version')))
    for name in props:
        if '${' + name + '}' in ET.tostring(model, encoding='unicode'):
            property_references[name].append(str(p.relative_to(ROOT)))
    for dep in model.iter():
        kind = dep.tag.split('}')[-1]
        if kind not in {'dependency', 'plugin', 'annotationProcessorPath', 'path', 'extension', 'additionalDependency'}:
            continue
        expression = value(dep,'version')
        group = resolve(value(dep,'groupId') or ('org.apache.maven.plugins' if kind == 'plugin' else ''), env)
        artifact = resolve(value(dep,'artifactId'), env)
        resolved = resolve(expression, env)
        names = re.findall(r'\$\{([^}]+)\}', expression)
        if expression and (not names or any(n not in props or env.get(n) != props.get(n) for n in names)):
            additional_usages.append({'pom':str(p.relative_to(ROOT)), 'kind':kind, 'group':group, 'artifact':artifact, 'expression':expression, 'current':resolved, 'classification':'fixture-retained' if '/src/it/' in p.as_posix() or '/src/test/resources/' in p.as_posix() else 'official-plugin-frozen' if kind == 'plugin' and group == 'org.apache.maven.plugins' else 'project-release' if group.startswith(('com.guicedee','com.jwebmp','com.activity-master')) else 'local-override' if names else 'hardcoded'})
        for prop in re.findall(r'\$\{([^}]+)\}', expression):
            if prop not in props or not re.match(r'^\d', props[prop]): continue
            group = resolve(value(dep,'groupId') or ('org.apache.maven.plugins' if kind == 'plugin' else ''),env)
            artifact = resolve(value(dep,'artifactId'),env)
            if not group or not artifact or '${' in group + artifact:
                unresolved_usages.append({'property': prop, 'pom': str(p.relative_to(ROOT)), 'group': group, 'artifact': artifact})
                continue
            if group.startswith(('com.guicedee','com.jwebmp','com.activity-master')): continue
            # A local override is not governed by the central Versioner value.
            if env.get(prop) != props[prop]: continue
            entry = {'group':group,'artifact':artifact,'kind':kind,'expression':expression,'pom':str(p.relative_to(ROOT)).replace('\\','/')}
            if entry not in usages[prop]: usages[prop].append(entry)

# Freeze actual official plugin version properties, never arbitrary maven.* library properties.
frozen = official_plugin_props | {p for p in props if p.startswith('javadoc.')} | {
    'guicedee.version','guicedee.config.version','jdk.release'
}
selected = {p:u for p,u in usages.items() if p not in frozen}
coordinates = sorted({(u['group'],u['artifact']) for rows in selected.values() for u in rows} | {(u['group'],u['artifact']) for u in additional_usages if u['classification'] in {'local-override','hardcoded'} and u['group'] and u['artifact'] and '${' not in u['group']+u['artifact']})

def fetch(coordinate):
    group, artifact = coordinate
    url = 'https://repo.maven.apache.org/maven2/' + group.replace('.','/') + '/' + artifact + '/maven-metadata.xml'
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'GuicedEE-dependency-audit/1.0'})
        data = urllib.request.urlopen(req,timeout=30).read()
        xml = ET.fromstring(data)
        return coordinate, {'url':url,'versions':[v.text for v in xml.findall('./versioning/versions/version')], 'lastUpdated':xml.findtext('./versioning/lastUpdated')}
    except Exception as error:
        return coordinate, {'url':url,'error':str(error)}

def key(version):
    m = re.match(r'\d+(?:\.\d+)*',version)
    return tuple(int(x) for x in m[0].split('.')) if m else ()

def eligible(version, current, allow_alpha=False):
    # Preserve runtime-flavor suffixes (JRE, Android, platform variants).
    if re.search(r'(?:alpha|beta|snapshot|(?:^|[.-])(?:rc|cr|m)\d)', current, re.I) and not allow_alpha:
        return False
    suffix = re.sub(r'^\d+(?:\.\d+)*','',current)
    if suffix and suffix.lower() not in {'.final','-final','.ga','-ga','.release','-release','-alpha'}:
        return bool(re.fullmatch(r'\d+(?:\.\d+)*'+re.escape(suffix),version))
    pattern = r'\d+(?:\.\d+)*(?:[-.](?:Final|GA|RELEASE))?'
    if allow_alpha: pattern = r'\d+(?:\.\d+)*(?:-alpha)?'
    return bool(re.fullmatch(pattern,version,re.I))

if args.inventory_only:
    inventory = {'additionalUsages':additional_usages, 'propertyReferences':dict(property_references), 'pomCount': pom_count, 'usages': dict(usages), 'frozenProperties': sorted(frozen), 'scanErrors': scan_errors, 'unresolvedUsages': unresolved_usages}
    (OUT/'inventory.json').write_text(json.dumps(inventory, indent=2), encoding='utf-8')
    print('Inventory saved:', OUT/'inventory.json')
    raise SystemExit(0)

print(f'Checking {len(selected)} properties / {len(coordinates)} coordinates from {pom_count} POMs',flush=True)
metadata = {}
with cf.ThreadPoolExecutor(max_workers=18) as pool:
    for i,(coordinate,data) in enumerate(pool.map(fetch,coordinates),1):
        metadata[':'.join(coordinate)] = data
        if i % 100 == 0: print(f'Fetched {i}/{len(coordinates)} metadata documents',flush=True)
(OUT/'metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
rows=[]
for prop, usage in sorted(selected.items()):
    current=props[prop]
    artifacts=[]
    seen=set()
    for use in usage:
        identity=(use['group'],use['artifact'],use['expression'])
        if identity in seen: continue
        seen.add(identity)
        md=metadata[use['group']+':'+use['artifact']]
        effective=resolve(use['expression'],props)
        versions=md.get('versions',[])
        alpha='opentelemetry' in prop and effective.endswith('-alpha')
        stable=[v for v in versions if eligible(v,effective,alpha)]
        same=[v for v in stable if key(v)[0]==key(effective)[0]] if key(effective) else []
        artifacts.append({**use,'currentArtifactVersion':effective,'currentExists':effective in versions,
                          'latestSameMajor':max(same,key=key) if same else None,
                          'latestStable':max(stable,key=key) if stable else None,
                          'alphaException':alpha,'url':md['url'],**({'error':md['error']} if 'error' in md else {})})
    rows.append({'property':prop,'current':current,'artifacts':artifacts,'usages':usage})
for use in additional_usages:
    md = metadata.get(use['group']+':'+use['artifact'], {})
    current = use['current']
    versions = [v for v in md.get('versions',[]) if key(current) and eligible(v,current) and key(v)[0] == key(current)[0]]
    use.update({'latestSameMajor':max(versions,key=key) if versions else None, 'metadataError':md.get('error'), 'url':md.get('url')})
unmapped_dispositions = {name: ('official-plugin-unused' if name == 'maven.jar.version' else 'local-project-plugin' if name == 'flatten-maven-plugin.version' else 'no-active-POM-reference' if not property_references.get(name) else 'requires-coordinate-review') for name in props if re.match(r'^\d',props[name]) and name not in selected and name not in frozen}
report={'unmappedDispositions':unmapped_dispositions, 'additionalUsages':additional_usages, 'propertyReferences':dict(property_references), 'scanErrors':scan_errors,'unresolvedUsages':unresolved_usages,'pomCount':pom_count,'propertyCount':len(rows),'coordinateCount':len(coordinates),'frozenProperties':sorted(frozen),'unmappedNumericProperties':{p:v for p,v in props.items() if re.match(r'^\d',v) and p not in selected and p not in frozen},'rows':rows}
(OUT/'audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
for row in rows:
    findings=[a for a in row['artifacts'] if a.get('error') or not a['currentExists'] or (a['latestSameMajor'] and key(a['latestSameMajor'])>key(a['currentArtifactVersion'])) or (a['latestStable'] and key(a['latestStable'])[0]>key(a['currentArtifactVersion'])[0])]
    if findings:
        print(json.dumps({'property':row['property'],'current':row['current'],'findings':[{k:a[k] for k in ('group','artifact','currentExists','latestSameMajor','latestStable') if k in a} | ({'error':a['error']} if 'error' in a else {}) for a in findings]}),flush=True)
print('Audit saved:',OUT/'audit.json',flush=True)

