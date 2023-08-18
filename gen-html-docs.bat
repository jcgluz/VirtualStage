del html-docs\*.*
python -m pydoc -w .\
move *.html html-docs
copy virtualstage-html-index.txt html-docs\index.html
gsar -o "-s<a href=:034.:034>index" "-r<a href=:034index.html:034>index" html-docs\*.html
gsar -o "-s<a href=:034file::d:0373A:0375Cvirtualstage:0375C" "-r<a href=:034../" html-docs\*.html


