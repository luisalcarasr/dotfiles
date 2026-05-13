set fish_greeting

if test (uname) = "Darwin"
    clear
end

# Initialize zoxide if available
if command -v zoxide &> /dev/null
    zoxide init fish | source
end

# Google Cloud SDK.
if [ -f '/Users/l.alcaras/.google-cllooud-sdk/google-cloud-sdk/path.fish.inc' ]
    . '/Users/l.alcaras/.google-cllooud-sdk/google-cloud-sdk/path.fish.inc'
end

# Python
if test -d '/Library/Frameworks/Python.framework/Versions/3.12/bin'
    fish_add_path -g '/Library/Frameworks/Python.framework/Versions/3.12/bin'
end

# opencode and antigravity paths are handled by conf.d/paths_scanner.fish

# If tide is installed but not configured, run tide configure
if status is-interactive
    if type -q tide; and not set -q tide_left_prompt_items
        echo "Tide is not configured. Running tide configure..."
        tide configure
    end
end
