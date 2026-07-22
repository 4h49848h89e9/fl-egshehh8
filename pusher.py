#!/usr/bin/env python3
"""
pusher.py - OryvexVPN Flutter Auto-Pusher
Commit all changes, force-push to main, and create a new version tag.
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================================
#  CONFIGURATION
# ============================================================
PROJECT_ROOT = Path(__file__).parent.resolve()
REPO_OWNER = "4h49848h89e9"
REPO_NAME = "fl-egshehh8"
PUBSPEC_PATH = PROJECT_ROOT / "pubspec.yaml"
WORKFLOWS_DIR = PROJECT_ROOT / ".github" / "workflows"

GIT_TIMEOUT = 300  # 5 minutes for push operations

# ============================================================
#  COLORS & PRINTING
# ============================================================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

if sys.platform == 'win32':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

def print_header(text):
    print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}{text:^70}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}OK  {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}ERR {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}WARN {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}INFO {text}{Colors.RESET}")

# ============================================================
#  GIT HELPERS
# ============================================================
def run_git_command(cmd, timeout=GIT_TIMEOUT):
    """Run a git command and return the result object."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            cwd=str(PROJECT_ROOT), timeout=timeout
        )
        return result
    except subprocess.TimeoutExpired:
        print_error(f"Git command timed out after {timeout}s: {cmd}")
        return None
    except Exception as e:
        print_error(f"Git command exception: {e}")
        return None

# ============================================================
#  CHECKS
# ============================================================
def check_git_config():
    """Ensure git user.name and user.email are set."""
    name = run_git_command("git config --global user.name", timeout=10)
    email = run_git_command("git config --global user.email", timeout=10)
    if not name or not name.stdout.strip() or not email or not email.stdout.strip():
        print_warning("Git user configuration not found!")
        print_info("Setting default git config...")
        run_git_command('git config --global user.name "Auto Pusher"', timeout=10)
        run_git_command('git config --global user.email "auto@pusher.local"', timeout=10)
    return True

def check_pubspec_name():
    """
    Validate the package name in pubspec.yaml to avoid CI failures.
    Must be lowercase, start with a letter, and use only underscores.
    """
    print_info("Checking pubspec.yaml package name...")
    if not PUBSPEC_PATH.exists():
        print_warning("pubspec.yaml not found, skipping name check.")
        return True

    raw = PUBSPEC_PATH.read_text(encoding="utf-8")
    name_match = re.search(r'^name:\s*([^\s#]+)', raw, re.MULTILINE)
    if not name_match:
        print_error("Could not find a `name:` field in pubspec.yaml.")
        return False

    name_value = name_match.group(1)
    valid_pattern = re.compile(r'^[a-z][a-z0-9_]*$')
    if not valid_pattern.match(name_value):
        print_error(f"Invalid package name in pubspec.yaml: '{name_value}'")
        print_error("Must be lowercase, start with a letter, and use underscores only (no dashes).")
        return False

    print_success(f"pubspec.yaml name OK: '{name_value}'")
    return True

def check_workflow_files():
    """
    Warn if multiple Windows build workflows exist (they cause duplicate CI runs).
    """
    print_info("Checking .github/workflows/ for duplicate workflow files...")
    if not WORKFLOWS_DIR.exists():
        print_warning(".github/workflows/ not found, skipping check.")
        return True

    yml_files = sorted(list(WORKFLOWS_DIR.glob("*.yml")) + list(WORKFLOWS_DIR.glob("*.yaml")))
    if len(yml_files) <= 1:
        print_success(f"{len(yml_files)} workflow file(s) found -- no duplicates.")
        return True

    build_like = []
    for f in yml_files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        if "windows-latest" in text or "windows-2022" in text or "build windows" in text.lower():
            build_like.append(f.name)

    if len(build_like) > 1:
        print_warning(f"Found {len(build_like)} Windows build workflows: {', '.join(build_like)}")
        print_warning("Each one will trigger separately on every push, doubling your build minutes.")
        print_warning("Consider deleting all but one. Continuing anyway.")
    else:
        print_success("No duplicate Windows build workflows detected.")

    return True

# ============================================================
#  GIT OPERATIONS
# ============================================================
def git_add_all():
    print_info("git add -A")
    result = run_git_command("git add -A")
    if result and result.returncode == 0:
        print_success("git add -A successful")
        return True
    print_error("git add -A failed")
    if result and result.stderr:
        print_error(result.stderr.strip())
    return False

def git_commit(message):
    print_info(f'git commit -m "{message}"')
    result = run_git_command(f'git commit -m "{message}"')
    if result and result.returncode == 0:
        print_success("Commit successful.")
        return True
    if result and "nothing to commit" in (result.stderr or ""):
        print_warning("No changes to commit.")
        return True
    print_error("Commit failed.")
    if result and result.stderr:
        print_error(result.stderr.strip())
    return False

def git_force_push():
    """Try force push with extended timeout, fallback to --force-with-lease."""
    # Primary attempt
    print_info("git push --force origin main (timeout: 300s)")
    result = run_git_command("git push --force origin main", timeout=300)
    if result and result.returncode == 0:
        print_success("Force push successful.")
        return True
    if result and result.stderr:
        print_error("Force push error: " + result.stderr.strip())

    # Fallback to --force-with-lease
    print_info("Trying git push --force-with-lease origin main")
    result = run_git_command("git push --force-with-lease origin main", timeout=300)
    if result and result.returncode == 0:
        print_success("Force-with-lease push successful.")
        return True
    if result and result.stderr:
        print_error("Force-with-lease error: " + result.stderr.strip())

    return False

def get_next_version_tag():
    """Determine the next semantic version tag from existing tags."""
    result = run_git_command("git tag -l", timeout=30)
    if result is None:
        return "v1.0.1"
    tags = result.stdout.splitlines()
    pattern = re.compile(r'^v(\d+)\.(\d+)\.(\d+)$')
    max_version = [1, 0, 0]
    for tag in tags:
        match = pattern.match(tag)
        if match:
            major, minor, patch = map(int, match.groups())
            if (major, minor, patch) > tuple(max_version):
                max_version = [major, minor, patch]
    max_version[2] += 1
    return f"v{max_version[0]}.{max_version[1]}.{max_version[2]}"

def delete_existing_tag(tag_name):
    print_info(f"Deleting existing tag: {tag_name}")
    run_git_command(f"git tag -d {tag_name}", timeout=30)
    run_git_command(f"git push origin :refs/tags/{tag_name}", timeout=60)

def create_and_push_tag(tag_name):
    print_info(f"Creating and pushing tag: {tag_name}")
    delete_existing_tag(tag_name)
    result = run_git_command(f"git tag {tag_name}", timeout=30)
    if result is None or result.returncode != 0:
        print_error("Tag creation failed.")
        return False
    result = run_git_command(f"git push origin {tag_name}", timeout=60)
    if result and result.returncode == 0:
        print_success(f"Tag {tag_name} pushed successfully.")
        return True
    print_error("Tag push failed.")
    return False

def check_remote():
    result = run_git_command("git remote -v", timeout=10)
    if result and result.returncode == 0:
        print_info("Remote(s) configured:")
        print(result.stdout)
        return True
    print_error("No git remote found. Please set origin.")
    return False

# ============================================================
#  MAIN
# ============================================================
def main():
    print_header("FL-EGSHEHH8 AUTO PUSHER (FORCE PUSH ALL FILES)")
    print_info(f"Project root: {PROJECT_ROOT}")

    # Pre-flight checks
    check_git_config()

    print_header("1. Pre-push safety checks")
    if not check_pubspec_name():
        print_error("Fix pubspec.yaml before pushing. Aborting.")
        sys.exit(1)
    check_workflow_files()

    # Check remote
    if not check_remote():
        print_error("Remote not set. Aborting.")
        sys.exit(1)

    # Stage changes
    print_header("2. Adding all files to git")
    if not git_add_all():
        print_error("git add failed. Exiting.")
        sys.exit(1)

    # Commit
    print_header("3. Committing changes")
    commit_msg = f"Auto-fix: {datetime.now().strftime('%Y-%m-%d %H:%M')} (pusher.py)"
    if not git_commit(commit_msg):
        print_warning("Attempting empty commit...")
        result = run_git_command('git commit --allow-empty -m "Auto-fix: No changes"')
        if result and result.returncode != 0:
            print_error("Commit failed. Exiting.")
            sys.exit(1)

    # Force push
    print_header("4. Force pushing to main")
    if not git_force_push():
        print_error("Force push failed. Please check your internet connection, credentials, and remote URL.")
        print_info("You can manually push with:")
        print_info("  git push --force origin main")
        print_info("  git push --tags")
        sys.exit(1)

    # Tag and push
    print_header("5. Creating new tag")
    new_tag = get_next_version_tag()
    print_info(f"New tag: {new_tag}")
    if not create_and_push_tag(new_tag):
        print_error("Tag push failed. You can manually push tags with: git push --tags")
        sys.exit(1)

    # Success
    print_header("ALL DONE")
    print_success(f"Tag {new_tag} created and pushed.")
    print_info(f"Actions: https://github.com/{REPO_OWNER}/{REPO_NAME}/actions")
    print_info(f"Release: https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/tag/{new_tag}")

if __name__ == "__main__":
    main()