# latexmk configuration for CV project
$pdf_mode = 1;          # Generate PDF via pdflatex
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error %O %S';
$clean_ext = 'aux bbl blg fdb_latexmk fls log out synctex.gz synctex toc lof lot nav snm vrb run.xml';
