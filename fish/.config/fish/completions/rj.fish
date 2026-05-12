# Completions for rj - repojump

# Disable file completions
complete -c rj -f

# Subcommands
complete -c rj -n __fish_use_subcommand -a pr       -d "Open pull requests (GitHub) / merge requests (GitLab)"
complete -c rj -n __fish_use_subcommand -a mr       -d "Open merge requests (GitLab) / pull requests (GitHub)"
complete -c rj -n __fish_use_subcommand -a issues   -d "Open issues"
complete -c rj -n __fish_use_subcommand -a ci       -d "Open CI/CD (Actions / Pipelines)"
complete -c rj -n __fish_use_subcommand -a releases -d "Open releases"
complete -c rj -n __fish_use_subcommand -a tags     -d "Open tags"
complete -c rj -n __fish_use_subcommand -a wiki     -d "Open wiki"
complete -c rj -n __fish_use_subcommand -a branches -d "Open branches"
complete -c rj -n __fish_use_subcommand -a commits  -d "Open commit history"
complete -c rj -n __fish_use_subcommand -a settings -d "Open repository settings"

# Options
complete -c rj -s r -l remote -x -a "(git remote 2>/dev/null)" -d "Specify git remote"
complete -c rj -s p -l provider -x -a "github gitlab" -d "Force provider"
