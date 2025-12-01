# Compilation Guide

## Yosr's CVs

### English ATS CV
```powershell
cd E:\LatexCv\CVs\English
pdflatex -output-directory=../../build CV_Yosr_BenNagra_English_ATS.tex
Move-Item ../../build/CV_Yosr_BenNagra_English_ATS.pdf .
```

### French ATS CV
```powershell
cd E:\LatexCv\CVs\French
pdflatex -output-directory=../../build CV_Yosr_BenNagra_French_ATS.tex
Move-Item ../../build/CV_Yosr_BenNagra_French_ATS.pdf .
```

### English General CV
```powershell
cd E:\LatexCv\CVs\English
pdflatex -output-directory=../../build CV_Yosr_BenNagra_English_General.tex
Move-Item ../../build/CV_Yosr_BenNagra_English_General.pdf .
```

### French General CV
```powershell
cd E:\LatexCv\CVs\French
pdflatex -output-directory=../../build CV_Yosr_BenNagra_French_General.tex
Move-Item ../../build/CV_Yosr_BenNagra_French_General.pdf .
```

## Naoures' CVs

### French CV
```powershell
cd E:\LatexCv\CVs\Naoures\French
pdflatex -output-directory=../../../build CV_Naoures_BenNagra_French.tex
Move-Item ../../../build/CV_Naoures_BenNagra_French.pdf .
```

### English CV
```powershell
cd E:\LatexCv\CVs\Naoures\English
pdflatex -output-directory=../../../build CV_Naoures_BenNagra_English.tex
Move-Item ../../../build/CV_Naoures_BenNagra_English.pdf .
```

## Cover Letters

### AFD.Tech Cover Letter
```powershell
cd E:\LatexCv\CoverLetters
pdflatex -output-directory=../build CoverLetter_Yosr_BenNagra_AFDTech.tex
Move-Item ../build/CoverLetter_Yosr_BenNagra_AFDTech.pdf .
```

### SOLUTEC Cover Letter
```powershell
cd E:\LatexCv\CoverLetters
pdflatex -output-directory=../build CoverLetter_Yosr_BenNagra_Solutec.tex
Move-Item ../build/CoverLetter_Yosr_BenNagra_Solutec.pdf .
```

## Note
All auxiliary files (.aux, .log, etc.) will be generated in the `build/` directory to keep your source folders clean.

## Current Job-Specific Configurations

### Yosr - English ATS CV
- **Target Role**: Angular Developer (Full-Stack Web Applications)
- **Key Skills**: Angular, TypeScript, HTML5, CSS3, Responsive Design, Node.js, Python, Firestore, Agile/Scrum
- **Optimized For**: Angular-focused roles, Remote teams, Agile environments

### Yosr - French ATS CV
- **Target Role**: Développeur Angular (Applications Web Full-Stack)
- **Key Skills**: Angular, TypeScript, HTML5, CSS3, Responsive Design, Node.js, Python, Firestore, Agile/Scrum
- **Optimized For**: Rôles Angular, Équipes distantes, Environnements Agile
