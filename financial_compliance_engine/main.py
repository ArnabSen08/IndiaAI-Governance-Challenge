import argparse
import sys
import os
import json
from src.indas_engine import IndASValidationEngine
from src.sebi_engine import SEBIComplianceEngine
from src.reporting import ExplainableComplianceReportGenerator

def main():
    parser = argparse.ArgumentParser(description="AI Financial Compliance Validation Engine")
    parser.add_argument('input_file', help="Path to financial statement PDF", nargs='?')
    parser.add_argument('--output', help="Output directory for reports", default="data/output")
    parser.add_argument('--demo', action='store_true', help="Run in demo mode with mock data")
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    parsed_data = {}
    
    if args.demo:
        print("Running in DEMO mode with mock data...")
        parsed_data = _generate_mock_data()
        company_name = parsed_data['metadata']['company_name']
    elif args.input_file:
        from src.nlp_parser import FinancialNLPParser
        print(f"Processing {args.input_file}...")
        try:
            nlp_parser = FinancialNLPParser()
            parsed_data = nlp_parser.parse_financial_document(args.input_file)
            company_name = parsed_data['metadata'].get('company_name', 'Unknown Company')
        except Exception as e:
            print(f"Error processing file: {e}")
            return
    else:
        parser.print_help()
        return

    print("Running IndAS Validation...")
    indas_engine = IndASValidationEngine()
    indas_findings = indas_engine.validate_statement(parsed_data)
    print(f"IndAS Findings: {len(indas_findings)}")
    
    print("Running SEBI Validation...")
    sebi_engine = SEBIComplianceEngine()
    # Mocking governance data for demo purposes if not present
    governance_data = parsed_data.get('governance_data', {
        'board_size': 10,
        'independent_directors': 2, # Intentional violation for demo
        'audit_committee_size': 4,
        'audit_committee_independent': 2
    })
    sebi_findings = sebi_engine.validate_sebi_compliance(parsed_data, governance_data)
    print(f"SEBI Findings: {len(sebi_findings)}")
    
    all_findings = indas_findings + sebi_findings
    
    print("Generating Report...")
    reporter = ExplainableComplianceReportGenerator()
    report = reporter.generate_comprehensive_report(
        findings=all_findings,
        financial_data=parsed_data,
        company_name=company_name,
        report_period="FY 2024-25"
    )
    
    # Save JSON
    json_path = os.path.join(args.output, f"{company_name}_compliance_report.json")
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=4, default=str)
    print(f"JSON report saved to {json_path}")
    
    # Save PDF
    pdf_path = os.path.join(args.output, f"{company_name}_compliance_report.pdf")
    reporter.export_report_to_pdf(report, pdf_path)
    print(f"PDF report saved to {pdf_path}")

def _generate_mock_data():
    """Generate valid mock data for testing"""
    from decimal import Decimal
    return {
        'metadata': {
            'company_name': 'Demo Corp Ltd',
            'financial_year': '2024-2025'
        },
        'balance_sheet': {
            'assets': {
                'Cash': {'current': Decimal('1000')},
                'Property': {'current': Decimal('5000')},
            },
            'liabilities': {
                'Debt': {'current': Decimal('3000')}
            },
            'equity': {
                'Share Capital': {'current': Decimal('2000')}
            },
            # Imbalance: 6000 vs 5000
        },
        'income_statement': {
            'revenue': {'Sales': {'current': Decimal('10000')}},
            'expenses': {'Cost of Goods': {'current': Decimal('6000')}},
            'profitability': {'Profit': {'current': Decimal('4000')}}
        },
        'disclosures': [
            {'text': 'Note 1: Basis of Preparation. We follow IndAS.'},
            {'text': 'Note 2: Revenue Recognition. Revenue is recognized upon delivery.'}
            # Missing other policies
        ],
        'governance_data': {
            'board_size': 8,
            'independent_directors': 1, # < 33% violation
            'audit_committee_size': 2, # < 3 violation
        }
    }

if __name__ == "__main__":
    main()
