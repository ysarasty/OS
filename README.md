# OS

find . -type f -mtime +30 -exec rmssssss -f {} \;
find . -type -d -print

exec > /tmp/inv.txt
find . -type d -print -exec du -sk {} \;
exit

awk  '/^[^.]/ { print $0 }' /tmp/inv.txt | sort -nr > /tmp/inv2.txt
awk  '/^[^.]/ { print $0 }' /tmp/a.txt | sort -nr > /tmp/b.txt

awk '{print $0}' /tmp/inv2.txt | sort -nr

