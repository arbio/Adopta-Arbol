mkdir -p _orig/
for f in *.jpg; do
    cp -v $f _orig/
    mogrify -geometry 600x $f 
done
