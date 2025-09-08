#!/bin/bash
# Nine Inches of Git Hooks Installation Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_SCRIPT="$SCRIPT_DIR/git_screamer_hook.py"
GIT_HOOKS_DIR=".git/hooks"
POST_PUSH_HOOK="$GIT_HOOKS_DIR/post-push"

echo "🎸 Installing Nine Inches of Git Hooks..."
echo "This will make your commit messages scream in industrial style when you push!"

# Check if we're in a git repository
if [ ! -d "$GIT_HOOKS_DIR" ]; then
    echo "❌ Error: Not a git repository. Please run this from a git project."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install -r "$SCRIPT_DIR/requirements.txt"

# Create the post-push hook
echo "🔗 Creating post-push hook..."
cat > "$POST_PUSH_HOOK" << 'EOF'
#!/bin/bash
# Nine Inches of Git Hooks

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_SCRIPT="$SCRIPT_DIR/../nine-inches-of-git-hooks/nine_inches_of_git_hooks.py"

if [ -f "$HOOK_SCRIPT" ]; then
    python3 "$HOOK_SCRIPT" "$@"
else
    echo "⚠️  Nine Inches of Git Hooks script not found at: $HOOK_SCRIPT"
fi
EOF

# Make the hook executable
chmod +x "$POST_PUSH_HOOK"

echo "✅ Nine Inches of Git Hooks installed successfully!"
echo "🎤 Your commit messages will now scream in industrial style when you push!"
echo ""
echo "To test it, make a commit and push:"
echo "  git commit -m 'Fixed the bug that was haunting my dreams'"
echo "  git push"
echo ""
echo "To uninstall, remove the hook:"
echo "  rm .git/hooks/post-push"