# Logical Cores
cat /proc/cpuinfo | grep -c "^processor"

# Physical Cores
cat /proc/cpuinfo | awk '/^core id/&&!a[$0]++{++i} END {print i}'

# Model Name
cat /proc/cpuinfo | awk -F '\\s*: | @' '/model name|Hardware|Processor|^cpu model|chip type|^cpu type/ {cpu=$2; if ($1 == "Hardware") exit } END { print cpu }'

# Base Frequency
cat /sys/devices/system/cpu/cpu0/cpufreq/base_frequency

# Current Frequency
cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq
