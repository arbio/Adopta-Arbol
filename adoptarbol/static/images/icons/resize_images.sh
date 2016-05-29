mkdir -p _orig/
for f in *.svg; do
    convert -antialias -geometry 48x48 $f `echo $f | cut -d . -f 1`.png
    mv -v $f _orig/
done
