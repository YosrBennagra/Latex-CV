"""
PDF Generator
=============

Compiles LaTeX to PDF using pdflatex.
"""

import subprocess
import shutil
import logging
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class PDFGenerator:
    """
    Generates PDF from LaTeX source.
    
    Uses pdflatex for compilation with proper error handling.
    """
    
    def __init__(self, output_dir: Path = None):
        """
        Initialize PDF generator.
        
        Args:
            output_dir: Directory for PDF output (default: ./output)
        """
        self.output_dir = output_dir or Path("output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check for pdflatex
        self.pdflatex_path = self._find_pdflatex()
    
    def _find_pdflatex(self) -> Optional[str]:
        """Find pdflatex executable."""
        pdflatex = shutil.which("pdflatex")
        if pdflatex:
            logger.info(f"Found pdflatex: {pdflatex}")
            return pdflatex
        
        # Common Windows paths
        common_paths = [
            r"C:\texlive\2023\bin\win64\pdflatex.exe",
            r"C:\texlive\2024\bin\win64\pdflatex.exe",
            r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe",
        ]
        
        for path in common_paths:
            if Path(path).exists():
                logger.info(f"Found pdflatex: {path}")
                return path
        
        logger.warning("pdflatex not found. PDF generation may fail.")
        return None
    
    def generate(
        self,
        latex_content: str,
        output_name: str,
        preamble_path: Path = None
    ) -> Path:
        """
        Generate PDF from LaTeX content.
        
        Args:
            latex_content: LaTeX document string
            output_name: Output filename (without .pdf)
            preamble_path: Path to preamble.tex file
            
        Returns:
            Path to generated PDF
            
        Raises:
            RuntimeError: If PDF generation fails
        """
        if not self.pdflatex_path:
            raise RuntimeError("pdflatex not found. Please install TeX Live or MiKTeX.")
        
        # Create temp directory for compilation
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Copy preamble if specified
            if preamble_path and preamble_path.exists():
                # Handle relative path in LaTeX
                shutil.copy(preamble_path, temp_path / "preamble.tex")
                
                # Fix the preamble path in LaTeX
                latex_content = latex_content.replace(
                    r"\input{../../preamble}",
                    r"\input{preamble}"
                )
            
            # Write LaTeX to temp file
            tex_path = temp_path / f"{output_name}.tex"
            tex_path.write_text(latex_content, encoding='utf-8')
            
            # Run pdflatex (twice for proper references)
            for run in range(2):
                result = subprocess.run(
                    [
                        self.pdflatex_path,
                        "-interaction=nonstopmode",
                        "-halt-on-error",
                        tex_path.name,
                    ],
                    cwd=temp_path,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                
                if result.returncode != 0 and run == 1:
                    # Log error output
                    log_path = temp_path / f"{output_name}.log"
                    if log_path.exists():
                        log_content = log_path.read_text(encoding='utf-8', errors='ignore')
                        # Extract error lines
                        errors = [l for l in log_content.split('\n') if '!' in l or 'Error' in l]
                        error_msg = '\n'.join(errors[:10])
                        logger.error(f"LaTeX errors:\n{error_msg}")
                    
                    raise RuntimeError(f"pdflatex failed: {result.stderr[:500]}")
            
            # Copy PDF to output directory
            pdf_temp = temp_path / f"{output_name}.pdf"
            if not pdf_temp.exists():
                raise RuntimeError("PDF was not generated")
            
            pdf_output = self.output_dir / f"{output_name}.pdf"
            shutil.copy(pdf_temp, pdf_output)
            
            logger.info(f"Generated PDF: {pdf_output}")
            return pdf_output
    
    def generate_from_file(self, tex_path: Path, output_name: str = None) -> Path:
        """
        Generate PDF from existing .tex file.
        
        Args:
            tex_path: Path to .tex file
            output_name: Output filename (default: same as input)
            
        Returns:
            Path to generated PDF
        """
        if not tex_path.exists():
            raise FileNotFoundError(f"LaTeX file not found: {tex_path}")
        
        latex_content = tex_path.read_text(encoding='utf-8')
        name = output_name or tex_path.stem
        
        # Find preamble relative to tex file
        preamble_path = tex_path.parent.parent.parent / "preamble.tex"
        if not preamble_path.exists():
            preamble_path = tex_path.parent.parent / "preamble.tex"
        if not preamble_path.exists():
            preamble_path = None
        
        return self.generate(latex_content, name, preamble_path)
    
    def is_available(self) -> bool:
        """Check if PDF generation is available."""
        return self.pdflatex_path is not None
