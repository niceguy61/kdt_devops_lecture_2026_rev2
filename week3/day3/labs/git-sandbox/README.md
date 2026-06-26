# W3D3 Git Sandbox

This sandbox creates an isolated Git repository under `/tmp/w3d3-git-sandbox`.

It is safe for class because it does not modify the lecture repository history.

## Create Sandbox
```bash
bash week3/day3/labs/git-sandbox/setup.sh
cd /tmp/w3d3-git-sandbox
```

## Inspect History
```bash
git log --oneline --graph --decorate --all
git branch --show-current
git status
```

## Conflict Drill
```bash
git switch feature/change-message
git rebase main
```

Expected: conflict in `app.txt`.

Abort if needed:

```bash
git rebase --abort
```

## Revert Drill
```bash
git switch main
git log --oneline -3
git revert HEAD --no-edit
git log --oneline -4
```

## Tag Drill
```bash
git tag v0.1.0
git tag --list
git show --stat v0.1.0
```
