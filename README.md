![Python checks](https://github.com/leakquicked/fileintegrity-watch/actions/workflows/python-checks.yml/badge.svg)

# FileIntegrity Watch

A local file-integrity monitor that records SHA-256 hashes and later detects modified or missing files.

## Usage
Python 3.10+, standard library only.

```bash
python integrity_watch.py baseline ./important-files baseline.json config.json app.py
python integrity_watch.py verify baseline.json
python -m unittest discover -s tests -v
```

The baseline command refuses to overwrite an existing manifest. Store the manifest somewhere protected and separate from the files being monitored; an attacker who can replace both can defeat this simple check.

## Scope and limitations
This tool hashes files you explicitly list; it does not run continuously, monitor directories automatically, or prove who changed a file. SHA-256 detects content changes but does not authenticate the manifest. Use it only on files you own or are authorized to inspect.
