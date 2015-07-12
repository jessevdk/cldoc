# Release procedure

## Increment versions, commit and tag
1. Increment the version in setup.py
1. Increment the version in cldoc-static/package.json (new minor version, micro version to 0)
1. Commit and tag:

  ```bash
  git add setup.py cldoc-static/package.json
  git commit -m "Release version <version>"
  git tag -a -m "Release version <version>" v<version>
  ```

## Release source version to pypi
```bash
python setup.py sdist upload
```

## Release static site generator to npm
```bash
npm publish
```

## Push to remote
```bash
git push --tags master:master
```