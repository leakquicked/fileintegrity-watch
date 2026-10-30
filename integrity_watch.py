#!/usr/bin/env python3
"""FileIntegrity Watch: create and verify SHA-256 manifests for local files."""
import argparse, hashlib, json
from pathlib import Path

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def build_manifest(root, paths):
    root=Path(root).resolve()
    records=[]
    for item in paths:
        path=(root / item).resolve()
        if root not in path.parents and path != root: raise ValueError(f"Path escapes root: {item}")
        if path.is_file(): records.append({"path":path.relative_to(root).as_posix(),"sha256":digest(path),"size":path.stat().st_size})
    return {"algorithm":"sha256","root":str(root),"files":sorted(records,key=lambda x:x["path"])}

def verify_manifest(manifest_path):
    manifest=json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    root=Path(manifest["root"]).resolve()
    results=[]
    for entry in manifest["files"]:
        path=(root / entry["path"]).resolve()
        if root not in path.parents and path != root: raise ValueError("Manifest contains path outside root")
        if not path.exists(): status="missing"; actual=None
        elif not path.is_file(): status="not_a_file"; actual=None
        else:
            actual=digest(path)
            status="ok" if actual==entry["sha256"] else "changed"
        results.append({"path":entry["path"],"status":status,"expected":entry["sha256"],"actual":actual})
    return {"checked":len(results),"ok":sum(x["status"]=="ok" for x in results),
            "problems":[x for x in results if x["status"]!="ok"],"results":results}

def main():
    p=argparse.ArgumentParser(description="Create or verify local SHA-256 file manifests.")
    sub=p.add_subparsers(dest="command",required=True)
    b=sub.add_parser("baseline"); b.add_argument("root"); b.add_argument("manifest"); b.add_argument("paths",nargs="+")
    v=sub.add_parser("verify"); v.add_argument("manifest")
    a=p.parse_args()
    if a.command=="baseline":
        output=Path(a.manifest)
        if output.exists(): p.error("Manifest already exists; choose another path to avoid overwriting a baseline.")
        data=build_manifest(a.root,a.paths); output.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
        print(f"Baseline created: {len(data['files'])} file(s)")
    else:
        result=verify_manifest(a.manifest); print(json.dumps(result,indent=2))
        if result["problems"]: raise SystemExit(1)
if __name__=="__main__": main()
