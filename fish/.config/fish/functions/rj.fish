function rj -d "Jump from a git repo to its browser URL"
    # --- Validate git repo ---
    if not command -q git
        echo "rj: git is not installed" >&2
        return 1
    end

    if not git rev-parse --is-inside-work-tree >/dev/null 2>&1
        echo "rj: not inside a git repository" >&2
        return 1
    end

    # --- Parse options ---
    set -l remote origin
    set -l provider_override ""

    while set -q argv[1]
        switch $argv[1]
            case -r --remote
                if not set -q argv[2]
                    echo "rj: missing value for $argv[1]" >&2
                    return 1
                end

                set remote $argv[2]
                set -e argv[1..2]

            case -p --provider
                if not set -q argv[2]
                    echo "rj: missing value for $argv[1]" >&2
                    return 1
                end

                set provider_override (string lower -- $argv[2])
                switch $provider_override
                    case github gitlab
                    case '*'
                        echo "rj: unsupported provider '$provider_override' (expected: github, gitlab)" >&2
                        return 1
                end

                set -e argv[1..2]

            case '*'
                break
        end
    end

    set -l remote_url (git remote get-url $remote 2>/dev/null)
    if test -z "$remote_url"
        echo "rj: remote '$remote' not found" >&2
        return 1
    end

    # --- Parse remote URL into base_url (https://host/owner/repo) ---
    set -l base_url (_rj_parse_remote "$remote_url")
    if test -z "$base_url"
        echo "rj: could not parse remote URL '$remote_url'" >&2
        return 1
    end

    # --- Detect provider ---
    set -l provider
    if test -n "$provider_override"
        set provider $provider_override
    else
        set provider (_rj_detect_provider "$base_url")
    end

    # --- Resolve subcommand to path ---
    set -l subcommand ""
    if set -q argv[1]
        set subcommand $argv[1]
    end

    set -l url (_rj_build_url "$base_url" "$provider" "$subcommand")

    # --- Open in browser ---
    echo "Opening $url"
    _rj_open "$url"
end

# ---------------------------------------------------------------------------
# Parse a git remote URL (SSH or HTTPS) into https://host/owner/repo
# ---------------------------------------------------------------------------
function _rj_parse_remote -a remote_url
    set -l url "$remote_url"

    # SSH: git@host:owner/repo.git  ->  https://host/owner/repo
    if string match -qr '^[a-zA-Z0-9._-]+@' -- "$url"
        set url (string replace -r '^[a-zA-Z0-9._-]+@' '' -- "$url")
        set url (string replace ':' '/' -- "$url")
        set url "https://$url"
    end

    # ssh://git@host/owner/repo.git  ->  https://host/owner/repo
    if string match -qr '^ssh://' -- "$url"
        set url (string replace -r '^ssh://[^@]+@' 'https://' -- "$url")
    end

    # git://host/owner/repo.git  ->  https://host/owner/repo
    if string match -qr '^git://' -- "$url"
        set url (string replace -r '^git://' 'https://' -- "$url")
    end

    # Strip trailing .git
    set url (string replace -r '\.git$' '' -- "$url")

    # Strip trailing slash
    set url (string replace -r '/$' '' -- "$url")

    echo "$url"
end

# ---------------------------------------------------------------------------
# Detect provider from the base URL
# Returns: github | gitlab | unknown
# ---------------------------------------------------------------------------
function _rj_detect_provider -a base_url
    if string match -qr 'github\.com' -- "$base_url"
        echo github
    else if string match -qr 'gitlab\.' -- "$base_url"
        echo gitlab
    else
        echo unknown
    end
end

# ---------------------------------------------------------------------------
# Build the final URL based on provider and subcommand
# ---------------------------------------------------------------------------
function _rj_build_url -a base_url provider subcommand
    # No subcommand -> open repo home
    if test -z "$subcommand"
        echo "$base_url"
        return
    end

    switch "$subcommand"
        # --- Pull / Merge requests ---
        case pr prs pull-requests mr mrs merge-requests
            switch "$provider"
                case github
                    echo "$base_url/pulls"
                case gitlab
                    echo "$base_url/-/merge_requests"
                case '*'
                    echo "$base_url/pulls"
            end

        # --- Issues ---
        case issues
            switch "$provider"
                case github
                    echo "$base_url/issues"
                case gitlab
                    echo "$base_url/-/issues"
                case '*'
                    echo "$base_url/issues"
            end

        # --- CI / Pipelines / Actions ---
        case ci pipelines actions
            switch "$provider"
                case github
                    echo "$base_url/actions"
                case gitlab
                    echo "$base_url/-/pipelines"
                case '*'
                    echo "$base_url/actions"
            end

        # --- Releases / Tags ---
        case releases
            switch "$provider"
                case github
                    echo "$base_url/releases"
                case gitlab
                    echo "$base_url/-/releases"
                case '*'
                    echo "$base_url/releases"
            end

        case tags
            switch "$provider"
                case github
                    echo "$base_url/tags"
                case gitlab
                    echo "$base_url/-/tags"
                case '*'
                    echo "$base_url/tags"
            end

        # --- Wiki ---
        case wiki
            switch "$provider"
                case github
                    echo "$base_url/wiki"
                case gitlab
                    echo "$base_url/-/wikis"
                case '*'
                    echo "$base_url/wiki"
            end

        # --- Settings ---
        case settings
            switch "$provider"
                case github
                    echo "$base_url/settings"
                case gitlab
                    echo "$base_url/-/settings/general"
                case '*'
                    echo "$base_url/settings"
            end

        # --- Branches ---
        case branches
            switch "$provider"
                case github
                    echo "$base_url/branches"
                case gitlab
                    echo "$base_url/-/branches"
                case '*'
                    echo "$base_url/branches"
            end

        # --- Commits ---
        case commits log
            switch "$provider"
                case github
                    echo "$base_url/commits"
                case gitlab
                    echo "$base_url/-/commits"
                case '*'
                    echo "$base_url/commits"
            end

        # --- Anything else: append as-is (escape hatch) ---
        case '*'
            echo "$base_url/$subcommand"
    end
end

# ---------------------------------------------------------------------------
# Cross-platform open command
# ---------------------------------------------------------------------------
function _rj_open -a url
    if command -q open
        open "$url"
    else if command -q xdg-open
        xdg-open "$url"
    else if command -q wslview
        wslview "$url"
    else
        echo "rj: no suitable browser opener found (tried: open, xdg-open, wslview)" >&2
        echo "     URL: $url"
        return 1
    end
end
