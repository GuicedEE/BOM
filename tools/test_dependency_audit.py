import pathlib,subprocess,tempfile,json,unittest
SCRIPT=pathlib.Path(__file__).with_name('dependency-audit.py')
class CoverageTest(unittest.TestCase):
 def test_inherited_override_hardcode_and_official_plugin(self):
  with tempfile.TemporaryDirectory() as d:
   root=pathlib.Path(d); v=root/'GuicedEE/bom/Versioner';v.mkdir(parents=True)
   (v/'pom.xml').write_text('<project><properties><lib.version>1.0</lib.version></properties></project>')
   (root/'pom.xml').write_text('<project><properties><lib.version>1.1</lib.version></properties></project>')
   child=root/'child';child.mkdir()
   (child/'pom.xml').write_text('''<project xmlns="http://maven.apache.org/POM/4.1.0"><parent><relativePath>../pom.xml</relativePath></parent><dependencies><dependency><groupId>example</groupId><artifactId>lib</artifactId><version>${lib.version}</version></dependency><dependency><groupId>example</groupId><artifactId>literal</artifactId><version>2.0</version></dependency></dependencies><build><plugins><plugin><artifactId>maven-compiler-plugin</artifactId><version>3.0</version></plugin></plugins></build></project>''')
   out=root/'target/audit';subprocess.run(['python',str(SCRIPT),'--root',str(root),'--out',str(out),'--inventory-only'],check=True,capture_output=True)
   rows=json.loads((out/'inventory.json').read_text())['additionalUsages'];r={x['artifact']:x for x in rows}
   self.assertEqual(r['lib']['current'],'1.1');self.assertEqual(r['lib']['classification'],'local-override')
   self.assertEqual(r['literal']['classification'],'hardcoded');self.assertEqual(r['maven-compiler-plugin']['classification'],'official-plugin-frozen')
if __name__=='__main__':unittest.main()
