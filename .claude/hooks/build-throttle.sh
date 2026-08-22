#!/usr/bin/env bash
input=$(cat)
cmd=$(jq -r '.tool_input.command // empty' <<<"$input")
[[ "$cmd" == *"dotnet build"* || "$cmd" == *"dotnet test"* ]] || exit 0

state=/tmp/claude-build-throttle; now=$(date +%s); cooldown=300
if [[ -f $state ]] && (( now - $(cat $state) < cooldown )); then
  left=$(( cooldown - (now - $(cat $state)) ))
  jq -n --arg r "Build throttled: ${left}s cooldown remaining. Keep editing and batch your changes; run one build afterwards." \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
fi
echo "$now" > "$state"
