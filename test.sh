echo "Andrew:"
git log --author=Andrew --pretty=tformat: --numstat | grep -v '^-' | awk '{ add+=$1; remove+=$2 } END { print add, remove }'
echo
echo "Andrew Darling"
git log --author=Andrew\ Darling --pretty=tformat: --numstat | grep -v '^-' | awk '{ add+=$1; remove+=$2 } END { print add, remove }'
echo
echo "Mehmet:"
git log --author=Mehmet --pretty=tformat: --numstat | grep -v '^-' | awk '{ add+=$1; remove+=$2 } END { print add, remove }'
echo
echo "MehmetMHY"
git log --author=MehmetMHY --pretty=tformat: --numstat | grep -v '^-' | awk '{ add+=$1; remove+=$2 } END { print add, remove }'
echo
echo "ehayes2000"
git log --author=ehayes2000 --pretty=tformat: --numstat | grep -v '^-' | awk '{ add+=$1; remove+=$2 } END { print add, remove }'
echo
echo "z3ht"
git log --author=z3ht --pretty=tformat: --numstat | grep -v '^-' | awk '{ add+=$1; remove+=$2 } END { print add, remove }'
echo



