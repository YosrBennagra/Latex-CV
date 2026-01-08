"""
CLI Module
==========

Command-line interface for CV optimization agent.
"""

import argparse
import logging
from pathlib import Path

from cv_agent.core import CVOptimizationAgent


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CV Optimization Agent - Generate optimized PDF CVs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate --job "Senior React Developer..." --company Google
  %(prog)s optimize --job "..." --output cv_optimized.tex
  %(prog)s score --cv CVs/English/CV.tex --job "..."
  %(prog)s skills --list
        """
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate command (main workflow - produces PDF)
    gen_parser = subparsers.add_parser('generate', help='Generate optimized PDF CV')
    gen_parser.add_argument('--job', '-j', required=True, help='Job description text or file path')
    gen_parser.add_argument('--company', '-c', required=True, help='Company name')
    gen_parser.add_argument('--cv', help='Input CV path (defaults to base CV)')
    
    # Optimize command (legacy - produces .tex)
    opt_parser = subparsers.add_parser('optimize', help='Optimize CV to LaTeX')
    opt_parser.add_argument('--job', '-j', required=True, help='Job description text or file')
    opt_parser.add_argument('--cv', '-c', help='Input CV path (defaults to base CV)')
    opt_parser.add_argument('--output', '-o', required=True, help='Output CV path')
    opt_parser.add_argument('--company', help='Company name')
    
    # Score command
    score_parser = subparsers.add_parser('score', help='Score CV for ATS compatibility')
    score_parser.add_argument('--cv', '-c', required=True, help='CV path to score')
    score_parser.add_argument('--job', '-j', required=True, help='Job description')
    
    # Validate command
    val_parser = subparsers.add_parser('validate', help='Validate CV')
    val_parser.add_argument('--cv', '-c', required=True, help='CV path to validate')
    
    # Skills command
    skills_parser = subparsers.add_parser('skills', help='Manage verified skills')
    skills_parser.add_argument('--list', '-l', action='store_true', help='List all verified skills')
    skills_parser.add_argument('--check', help='Check if a skill is verified')
    
    args = parser.parse_args()
    
    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format='%(message)s')
    
    if args.command == 'generate':
        run_generate(args)
    elif args.command == 'optimize':
        run_optimize(args)
    elif args.command == 'score':
        run_score(args)
    elif args.command == 'validate':
        run_validate(args)
    elif args.command == 'skills':
        run_skills(args)
    else:
        parser.print_help()


def run_generate(args):
    """Generate optimized PDF CV."""
    from cv_agent import generate_cv
    
    # Get job description from text or file
    job_desc = args.job
    if Path(args.job).exists():
        job_desc = Path(args.job).read_text(encoding='utf-8')
    
    print(f"\n{'='*60}")
    print("CV OPTIMIZATION AGENT")
    print(f"{'='*60}")
    print(f"Company: {args.company}")
    print(f"Job description: {len(job_desc)} characters")
    print(f"{'='*60}\n")
    
    result = generate_cv(
        job_description=job_desc,
        company=args.company
    )
    
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")
    
    if result.pdf_path:
        print(f"PDF generated: {result.pdf_path}")
    if result.output_path:
        print(f"LaTeX saved: {result.output_path}")
    
    print(f"\nATS Score: {result.ats_score:.0f}/100")
    print(f"Relevance: {result.relevance_score:.0f}%")
    print(f"Pages: {result.page_count:.1f}")
    print(f"Validation: {'PASSED' if result.validation_passed else 'FAILED'}")
    
    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for w in result.warnings[:5]:
            print(f"  - {w}")
    
    print(f"{'='*60}\n")


def run_optimize(args):
    """Run CV optimization."""
    from cv_agent.core import CVOptimizationAgent
    
    agent = CVOptimizationAgent()
    
    # Get job description
    job_desc = args.job
    if Path(args.job).exists():
        job_desc = Path(args.job).read_text(encoding='utf-8')
    
    # Get CV path
    cv_path = Path(args.cv) if args.cv else None
    
    result = agent.optimize(
        job_description=job_desc,
        cv_path=cv_path,
        output_path=Path(args.output),
        company_name=args.company
    )
    
    print(f"\n{'='*50}")
    print(f"✓ CV optimized successfully!")
    print(f"  ATS Score: {result.ats_score:.0f}/100")
    print(f"  Relevance: {result.relevance_score:.0f}%")
    print(f"  Pages: {result.page_count}")
    print(f"  Output: {args.output}")
    
    if result.warnings:
        print(f"\n⚠ Warnings:")
        for w in result.warnings:
            print(f"  - {w}")


def run_score(args):
    """Run ATS scoring."""
    from cv_agent.parsing import CVParser, JobParser
    from cv_agent.scoring import ATSScorer
    
    cv_parser = CVParser()
    job_parser = JobParser()
    scorer = ATSScorer()
    
    cv_data = cv_parser.parse(Path(args.cv))
    
    job_desc = args.job
    if Path(args.job).exists():
        job_desc = Path(args.job).read_text(encoding='utf-8')
    job_data = job_parser.parse(job_desc)
    
    score = scorer.calculate_score(cv_data, job_data)
    relevance = scorer.score_relevance(cv_data, job_data)
    
    print(f"\n{'='*50}")
    print(f"ATS Score: {score:.0f}/100")
    print(f"\nRelevance breakdown:")
    print(f"  Experiences: {len(relevance['experience'])} scored")
    print(f"  Skills: {len(relevance['skills'])} scored")


def run_validate(args):
    """Run CV validation."""
    from cv_agent.parsing import CVParser, JobParser
    from cv_agent.validation import CVValidator
    from cv_agent.enforcement import OnePageEnforcer
    
    cv_parser = CVParser()
    validator = CVValidator()
    enforcer = OnePageEnforcer()
    
    cv_data = cv_parser.parse(Path(args.cv))
    
    # Create minimal job data for validation
    from cv_agent.domain import JobData
    job_data = JobData(raw_text="", title="Software Engineer")
    
    cv_dict = {
        'name': cv_data.name,
        'role': cv_data.role,
        'summary': cv_data.summary,
        'skills': cv_data.skills,
        'experience': [
            {'title': e.title, 'company': e.company, 'bullets': list(e.bullets)}
            for e in cv_data.experience
        ],
        'education': cv_data.education,
    }
    
    page_estimate = enforcer.estimate_pages(cv_dict)
    result = validator.validate(cv_dict, job_data, page_estimate)
    
    print(f"\n{'='*50}")
    print(f"Validation: {'✓ PASSED' if result.passed else '✗ FAILED'}")
    print(f"  ATS Compliant: {'✓' if result.ats_compliant else '✗'}")
    print(f"  HR Tone: {'✓' if result.hr_tone_approved else '✗'}")
    print(f"  One Page: {'✓' if result.one_page_compliant else '✗'}")
    
    if result.all_warnings:
        print(f"\nWarnings ({result.warning_count}):")
        for w in result.all_warnings:
            print(f"  - {w}")


def run_skills(args):
    """Run skills management."""
    from cv_agent.domain import VERIFIED_SKILLS, is_skill_verified, is_skill_forbidden
    
    if args.list:
        print(f"\nVerified Skills ({len(VERIFIED_SKILLS)}):")
        print("-" * 40)
        for skill in sorted(VERIFIED_SKILLS):
            print(f"  ✓ {skill}")
    
    elif args.check:
        skill = args.check
        verified = is_skill_verified(skill)
        forbidden = is_skill_forbidden(skill)
        
        if forbidden:
            print(f"❌ '{skill}' is FORBIDDEN")
        elif verified:
            print(f"✓ '{skill}' is verified")
        else:
            print(f"⚠ '{skill}' is not in verified inventory")


if __name__ == '__main__':
    main()
