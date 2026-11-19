# GitHub Setup

Recommended repository name: `is665_assignment7_regression_lab`.

After the first push, verify GitHub Actions is green. Protect `main` with pull requests, required CI checks, blocked force pushes, and blocked deletions.

For a stable release:

```powershell
git tag -a v1.0.0 -m "Assignment 7 stable release"
git push origin v1.0.0
```

The release workflow creates a downloadable source ZIP on GitHub Releases.
