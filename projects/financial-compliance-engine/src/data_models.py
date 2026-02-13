from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Boolean, JSON, Text, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FinancialStatement(Base):
    """
    Master financial statement record
    """
    __tablename__ = 'financial_statements'
    
    # Identifiers
    statement_id = Column(String, primary_key=True)
    company_id = Column(String, nullable=False, index=True)
    company_name = Column(String)
    cin_number = Column(String, unique=True)  # Company registration
    gstin = Column(String)
    
    # Statement Period
    fiscal_year = Column(Integer, index=True)
    quarter = Column(Integer)  # 1-4 for quarterly
    statement_date = Column(DateTime, index=True)
    financial_year_end = Column(DateTime)
    comparative_period_end = Column(DateTime, nullable=True)
    
    # Statement Type
    statement_type = Column(String)  # Annual, Quarterly, Standalone, Consolidated
    is_consolidated = Column(Boolean)
    is_restated = Column(Boolean, default=False)
    
    # Industry Sector
    industry_sector = Column(String)  # Banking, NBFC, Manufacturing, IT, etc.
    listing_status = Column(String)  # BSE, NSE, Unlisted
    
    # Financial Status
    is_first_time_adopter = Column(Boolean)  # IndAS adoption
    accounting_standard_used = Column(String)  # IndAS, IFRS, Old GAAP
    
    # Submission Details
    auditor_name = Column(String)
    audit_opinion = Column(String)  # Unmodified, Modified, Disclaimer
    audit_report_date = Column(DateTime)
    director_certification_date = Column(DateTime)
    filing_date = Column(DateTime)
    
    # Metadata
    extraction_date = Column(DateTime, default=datetime.now)
    last_validation = Column(DateTime, nullable=True)
    data_quality_score = Column(Float)  # 0-100
    
    # Source Document
    source_file_hash = Column(String)
    source_file_path = Column(String)

class GeneralLedgerAccount(Base):
    """
    Chart of accounts with GL codes
    """
    __tablename__ = 'general_ledger_accounts'
    
    account_id = Column(String, primary_key=True)
    statement_id = Column(String, ForeignKey('financial_statements.statement_id'), nullable=False, index=True)
    
    # Account Details
    account_name = Column(String)
    account_code = Column(String)  # IndAS GL code
    account_type = Column(String)  # Asset, Liability, Equity, Revenue, Expense
    account_subtype = Column(String)  # Current, Non-current, etc.
    
    # Amounts
    current_period_amount = Column(Numeric(18, 2))
    prior_period_amount = Column(Numeric(18, 2), nullable=True)
    prior_year_opening_amount = Column(Numeric(18, 2), nullable=True)
    
    # SEBI Classification
    sebi_classification = Column(String)
    materiality_flag = Column(Boolean)
    
    # Relationships
    parent_account_code = Column(String)
    schedule_reference = Column(String)  # "Schedule 1", "Schedule 2", etc.
    
    # Notes & Disclosures
    footnote_reference = Column(String)
    disclosure_notes = Column(JSON)  # References to disclosure notes
    
    # Validation Status
    is_reconciled = Column(Boolean, default=False)
    reconciliation_note = Column(Text, nullable=True)

class IncomeStatement(Base):
    """
    Profit & Loss statement data
    """
    __tablename__ = 'income_statements'
    
    statement_id = Column(String, ForeignKey('financial_statements.statement_id'), primary_key=True)
    
    # Revenue
    gross_revenue = Column(Numeric(18, 2))
    revenue_from_operations = Column(Numeric(18, 2))
    other_income = Column(Numeric(18, 2))
    excise_duty = Column(Numeric(18, 2), nullable=True)
    revenue_from_services = Column(Numeric(18, 2), nullable=True)
    
    # Expenses
    cost_of_materials = Column(Numeric(18, 2))
    employee_benefits = Column(Numeric(18, 2))
    depreciation_amortization = Column(Numeric(18, 2))
    finance_costs = Column(Numeric(18, 2))
    other_expenses = Column(Numeric(18, 2))
    total_expenses = Column(Numeric(18, 2))
    
    # EBITDA and Profitability
    ebitda = Column(Numeric(18, 2))
    operating_profit = Column(Numeric(18, 2))
    profit_before_tax = Column(Numeric(18, 2))
    tax_expense = Column(Numeric(18, 2))
    profit_after_tax = Column(Numeric(18, 2))
    
    # EPS
    eps_basic = Column(Float)
    eps_diluted = Column(Float)
    
    # Comparable Periods
    prior_period_profit_after_tax = Column(Numeric(18, 2), nullable=True)
    yoy_growth_percent = Column(Float, nullable=True)

class BalanceSheet(Base):
    """
    Balance sheet statement
    """
    __tablename__ = 'balance_sheets'
    
    statement_id = Column(String, ForeignKey('financial_statements.statement_id'), primary_key=True)
    
    # Assets
    current_assets = Column(Numeric(18, 2))
    non_current_assets = Column(Numeric(18, 2))
    total_assets = Column(Numeric(18, 2))
    
    # Asset Breakdowns
    cash_equivalents = Column(Numeric(18, 2))
    inventories = Column(Numeric(18, 2))
    receivables = Column(Numeric(18, 2))
    property_plant_equipment = Column(Numeric(18, 2))
    intangible_assets = Column(Numeric(18, 2))
    financial_assets = Column(Numeric(18, 2))
    right_of_use_asset = Column(Numeric(18, 2), default=0)
    
    # Liabilities
    current_liabilities = Column(Numeric(18, 2))
    non_current_liabilities = Column(Numeric(18, 2))
    total_liabilities = Column(Numeric(18, 2))
    
    # Liability Breakdowns
    borrowings_short_term = Column(Numeric(18, 2))
    borrowings_long_term = Column(Numeric(18, 2))
    lease_liability = Column(Numeric(18, 2), default=0)
    payables = Column(Numeric(18, 2))
    provisions = Column(Numeric(18, 2))
    deferred_tax_liabilities = Column(Numeric(18, 2))
    
    # Equity
    share_capital = Column(Numeric(18, 2))
    reserves_surpluses = Column(Numeric(18, 2))
    total_equity = Column(Numeric(18, 2))
    
    # Balance Check
    is_balanced = Column(Boolean)
    balance_difference = Column(Numeric(18, 2), default=0)

class CashFlowStatement(Base):
    """
    Cash flow statement
    """
    __tablename__ = 'cash_flow_statements'
    
    statement_id = Column(String, ForeignKey('financial_statements.statement_id'), primary_key=True)
    
    # Operating Activities
    operating_cash_flow = Column(Numeric(18, 2))
    net_profit = Column(Numeric(18, 2))
    depreciation = Column(Numeric(18, 2))
    change_in_working_capital = Column(Numeric(18, 2))
    
    # Investing Activities
    investing_cash_flow = Column(Numeric(18, 2))
    capex = Column(Numeric(18, 2))
    asset_disposals = Column(Numeric(18, 2))
    investments = Column(Numeric(18, 2))
    
    # Financing Activities
    financing_cash_flow = Column(Numeric(18, 2))
    debt_raised = Column(Numeric(18, 2))
    debt_repaid = Column(Numeric(18, 2))
    dividend_paid = Column(Numeric(18, 2))
    share_issuance = Column(Numeric(18, 2))
    
    # Net Cash Movement
    net_change_cash = Column(Numeric(18, 2))
    cash_opening = Column(Numeric(18, 2))
    cash_closing = Column(Numeric(18, 2))

class FinancialDisclosure(Base):
    """
    Schedule/Note disclosures
    """
    __tablename__ = 'financial_disclosures'
    
    disclosure_id = Column(String, primary_key=True)
    statement_id = Column(String, ForeignKey('financial_statements.statement_id'), nullable=False, index=True)
    
    # Disclosure Details
    disclosure_number = Column(String)  # Schedule 1, Note 2, etc.
    disclosure_title = Column(String)
    disclosure_type = Column(String)  # Schedule, Accounting Policy, Contingency, etc.
    
    # Content
    disclosure_text = Column(Text)
    extracted_data = Column(JSON)  # Structured data extracted from disclosure
    
    # Compliance Relevance
    relevant_standards = Column(JSON)  # IndAS, SEBI, RBI rules referenced
    is_material = Column(Boolean)
    materiality_assessment = Column(Text)

class ComplianceRule(Base):
    """
    Master compliance rules database
    """
    __tablename__ = 'compliance_rules'
    
    rule_id = Column(String, primary_key=True)
    
    # Rule Details
    rule_name = Column(String)
    rule_description = Column(Text)
    rule_type = Column(String, index=True)  # IndAS, SEBI, RBI, ESG
    framework = Column(String)  # e.g., "IndAS 109", "LODR", "RBI NBFC Norms"
    framework_section = Column(String)
    
    # Rule Logic
    rule_condition = Column(Text)  # Rule definition/logic
    severity_level = Column(String)  # Critical, High, Medium, Low
    applicability = Column(JSON)  # Sector, Size, Status conditions
    
    # Validation Approach
    validation_method = Column(String)  # Rule-based, ML-based, Manual
    test_data_fields = Column(JSON)  # Required GL codes/amounts
    
    # Compliance Guidance
    compliance_guidance = Column(Text)
    remediation_steps = Column(JSON)
    
    # Metrics
    false_positive_rate = Column(Float)
    detection_accuracy = Column(Float)
    
    # References
    regulatory_reference = Column(String)  # Link to regulation
    version = Column(Integer)
    last_updated = Column(DateTime)

class ComplianceCheckResult(Base):
    """
    Compliance check execution and results
    """
    __tablename__ = 'compliance_check_results'
    
    result_id = Column(String, primary_key=True)
    statement_id = Column(String, ForeignKey('financial_statements.statement_id'), nullable=False, index=True)
    rule_id = Column(String, ForeignKey('compliance_rules.rule_id'), nullable=False)
    
    # Check Execution
    check_timestamp = Column(DateTime)
    check_duration_seconds = Column(Float)
    
    # Result
    is_compliant = Column(Boolean)
    finding_type = Column(String)  # Pass, Warning, Exception, Risk
    finding_description = Column(Text)
    
    # Evidence & Details
    relevant_accounts = Column(JSON)  # GL codes involved
    relevant_amounts = Column(JSON)  # Amounts from statements
    supporting_evidence = Column(Text)
    
    # Explainability
    explanation = Column(Text)  # Natural language explanation
    xai_method = Column(String)  # LIME, SHAP, Rule trace
    feature_importance = Column(JSON)  # Feature importance scores
    
    # Risk Assessment
    fraud_risk_score = Column(Float)  # 0-100
    risk_flag = Column(Boolean)
    risk_indicators = Column(JSON)
    
    # Resolution
    management_response = Column(Text, nullable=True)
    corrective_action = Column(Text, nullable=True)
    status = Column(String)  # Open, In-progress, Resolved, Waived

class ComplianceReport(Base):
    """
    Generated compliance reports
    """
    __tablename__ = 'compliance_reports'
    
    report_id = Column(String, primary_key=True)
    statement_id = Column(String, ForeignKey('financial_statements.statement_id'), nullable=False, index=True)
    
    # Report Details
    report_type = Column(String)  # Executive, Detailed, Auditor Workpaper
    report_date = Column(DateTime)
    report_period = Column(String)
    
    # Compliance Status
    overall_compliance_status = Column(String)  # Compliant, Non-compliant, Conditional
    compliance_percentage = Column(Float)  # % of rules passed
    
    # Findings Summary
    total_findings = Column(Integer)
    critical_findings = Column(Integer)
    high_findings = Column(Integer)
    medium_findings = Column(Integer)
    low_findings = Column(Integer)
    
    # Framework Coverage
    indas_compliance_percent = Column(Float)
    sebi_compliance_percent = Column(Float)
    rbi_compliance_percent = Column(Float)
    esg_compliance_percent = Column(Float)
    
    # Report Content
    executive_summary = Column(Text)
    detailed_findings = Column(Text)
    recommendations = Column(JSON)
    
    # Generated Report Files
    pdf_report_path = Column(String)
    excel_workpaper_path = Column(String)
    json_export_path = Column(String)
    
    # Validation & Approval
    prepared_by = Column(String)
    reviewed_by = Column(String, nullable=True)
    approved_by = Column(String, nullable=True)
    review_date = Column(DateTime, nullable=True)

class ESGData(Base):
    """
    Environmental, Social, Governance data
    """
    __tablename__ = 'esg_data'
    
    esg_id = Column(String, primary_key=True)
    statement_id = Column(String, ForeignKey('financial_statements.statement_id'), nullable=False, index=True)
    
    # Environmental Indicators
    carbon_emissions_scope1 = Column(Numeric(18, 2), nullable=True)
    carbon_emissions_scope2 = Column(Numeric(18, 2), nullable=True)
    energy_consumption_mwh = Column(Numeric(18, 2), nullable=True)
    water_consumption = Column(Numeric(18, 2), nullable=True)
    waste_generated_tonnes = Column(Numeric(18, 2), nullable=True)
    renewable_energy_percent = Column(Float, nullable=True)
    
    # Social Indicators
    employee_count = Column(Integer, nullable=True)
    gender_diversity_percent_female = Column(Float, nullable=True)
    employee_turnover_percent = Column(Float, nullable=True)
    workplace_injuries = Column(Integer, nullable=True)
    training_hours_per_employee = Column(Float, nullable=True)
    community_investment = Column(Numeric(18, 2), nullable=True)
    
    # Governance Indicators
    board_size = Column(Integer, nullable=True)
    independent_directors_percent = Column(Float, nullable=True)
    women_board_members = Column(Integer, nullable=True)
    audit_committee_meetings = Column(Integer, nullable=True)
    csr_spending_percent_pbt = Column(Float, nullable=True)
    executive_remuneration_ratio = Column(Float, nullable=True)
    
    # ESG Ratings
    environmental_score = Column(Float, nullable=True)  # 0-100
    social_score = Column(Float, nullable=True)
    governance_score = Column(Float, nullable=True)
    overall_esg_score = Column(Float, nullable=True)
    
    # Data Quality
    data_source = Column(String)  # Annual report, CSR report, Third-party audit
    is_assured = Column(Boolean, default=False)
    assurance_provider = Column(String, nullable=True)
    last_updated = Column(DateTime)
