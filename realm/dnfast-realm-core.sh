aria2c -x 4 https://static.realm.io/downloads/core/realm-core-$1.tar.bz2 && \
mv ./realm-core-$1.tar.bz2 $TMPDIR/core_bin/core-$1.tar.bz2
