import re
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import pdfplumber
from decimal import Decimal

class FinancialNLPParser:
    """
    NLP pipeline for financial statement parsing
    """
    
    def __init__(self):
        # Load models
        # Note: In a real environment, we'd ensure these models are downloaded.
        # For this prototype, we'll try/except to avoid crashing if models aren't present.
        try:
            self.nlp = spacy.load('en_core_web_lg')
        except OSError:
            print("Warning: en_core_web_lg not found. Functionality may be limited.")
            self.nlp = spacy.blank("en") # Fallback

        try:
            self.ner_model = pipeline("ner", model="bert-base-multilingual-cased")
        except:
             print("Warning: NER model not loaded.")
             self.ner_model = None

        
        # Financial entity patterns
        self.patterns = {
            'currency_amount': r'(?:Rs|₹|USD|INR|USD|EUR)\s*[.,]?\s*(\d+(?:[,\s.]\d{3})*(?:\.\d+)?)',
            'account_types': ['Asset', 'Liability', 'Equity', 'Revenue', 'Expense', 'Income'],
            'debit_credit': r'(Debit|Credit|Dr\.|Cr\.)',
        }
    
    def parse_financial_document(self, pdf_path: str) -> Dict:
        """
        Extract structured data from financial statement PDF
        """
        extracted_data = {
            'balance_sheet': {},
            'income_statement': {},
            'cash_flow': {},
            'disclosures': [],
            'metadata': {}
        }
        
        # Extract text and tables
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract text
                text = page.extract_text()
                if not text: continue
                
                # Extract tables
                tables = page.extract_tables()
                
                # Identify statement type
                stmt_type = self._identify_statement_type(text)
                
                # Parse based on statement type
                if 'Balance Sheet' in stmt_type:
                    extracted_data['balance_sheet'].update(
                        self._parse_balance_sheet(tables, text)
                    )
                elif 'Income' in stmt_type or 'P&L' in stmt_type:
                    extracted_data['income_statement'].update(
                        self._parse_income_statement(tables, text)
                    )
                elif 'Cash Flow' in stmt_type:
                    extracted_data['cash_flow'].update(
                        self._parse_cash_flow(tables, text)
                    )
                else:
                    # Disclosure notes
                    extracted_data['disclosures'].extend(
                        self._parse_disclosures(text)
                    )
        
        # Extract metadata
        extracted_data['metadata'] = self._extract_metadata(pdf_path)
        
        return extracted_data
    
    def _identify_statement_type(self, text: str) -> str:
        """
        Identify type of financial statement
        """
        keywords = {
            'Balance Sheet': ['Balance Sheet', 'Balance', 'Financial Position'],
            'Income Statement': ['Income Statement', 'P&L', 'Profit and Loss', 'Statement of Profit or Loss'],
            'Cash Flow': ['Cash Flow', 'Cash Flows from Operations'],
            'Disclosure': ['Note', 'Schedule', 'Disclosure', 'Accounting Policy']
        }
        
        for stmt_type, keywords_list in keywords.items():
            if any(kw in text for kw in keywords_list):
                return stmt_type
        
        return 'Unknown'
    
    def _parse_balance_sheet(self, tables: List, text: str) -> Dict:
        """
        Parse balance sheet data
        """
        bs_data = {
            'assets': {},
            'liabilities': {},
            'equity': {}
        }
        
        for table in tables:
            if not table: continue
            df = pd.DataFrame(table)
            
            # Extract numerical columns
            for idx, row in df.iterrows():
                row_text = ' '.join(str(cell) for cell in row if cell)
                
                # Identify section
                if 'Current Asset' in row_text:
                    section = 'assets'
                elif 'Non-Current Asset' in row_text:
                    section = 'assets'
                elif 'Liabilit' in row_text:
                    section = 'liabilities'
                elif 'Equity' in row_text:
                    section = 'equity'
                else:
                    # Default to assets if identifying logic is weak for prototype
                    section = 'assets' 
                
                # Extract account name and amount
                account_name = row_text.split('\n')[0]
                amounts = self._extract_amounts(row_text)
                
                if amounts.get('current') is not None:
                     bs_data[section][account_name] = amounts
        
        return bs_data
    
    def _parse_income_statement(self, tables: List, text: str) -> Dict:
        """
        Parse income statement
        """
        is_data = {
            'revenue': {},
            'expenses': {},
            'profitability': {}
        }
        
        for table in tables:
            if not table: continue
            df = pd.DataFrame(table)
            
            for idx, row in df.iterrows():
                row_text = ' '.join(str(cell) for cell in row if cell)
                
                # Identify line items
                if any(rev in row_text.lower() for rev in ['revenue', 'sales', 'income from']):
                    section = 'revenue'
                elif any(exp in row_text.lower() for exp in ['expense', 'cost', 'depreciation']):
                    section = 'expenses'
                elif any(prof in row_text.lower() for prof in ['profit', 'earnings', 'ebitda']):
                    section = 'profitability'
                else:
                    section = 'revenue' # Default
                
                account_name = row_text.split('\n')[0]
                amounts = self._extract_amounts(row_text)
                
                if amounts.get('current') is not None:
                    is_data[section][account_name] = amounts
        
        return is_data
    
    def _parse_cash_flow(self, tables: List, text: str) -> Dict:
        """
        Parse cash flow statement
        """
        cf_data = {
            'operating': {},
            'investing': {},
            'financing': {}
        }
        
        for table in tables:
            if not table: continue
            df = pd.DataFrame(table)
            
            for idx, row in df.iterrows():
                row_text = ' '.join(str(cell) for cell in row if cell)
                
                if 'Operating' in row_text:
                    section = 'operating'
                elif 'Investing' in row_text:
                    section = 'investing'
                elif 'Financing' in row_text:
                    section = 'financing'
                else:
                    section = 'operating' # Default
                
                account_name = row_text.split('\n')[0]
                amounts = self._extract_amounts(row_text)
                
                if amounts.get('current') is not None:
                    cf_data[section][account_name] = amounts
        
        return cf_data
    
    def _extract_amounts(self, text: str) -> Dict:
        """
        Extract numerical amounts from text
        """
        amounts = {}
        
        # Find all currency amounts
        pattern = r'(?:Rs|₹|INR|USD|EUR)?\s*[.,]?\s*(\d+(?:[,\s]\d{3})*(?:\.\d{2})?)'
        matches = re.findall(pattern, text)
        
        if matches:
            # Typically: current period, prior period
            amounts['current'] = self._clean_amount(matches[0]) if len(matches) > 0 else None
            amounts['prior'] = self._clean_amount(matches[1]) if len(matches) > 1 else None
        
        return amounts
    
    def _clean_amount(self, amount_str: str) -> Decimal:
        """
        Clean and convert amount string to Decimal
        """
        # Remove commas and spaces
        cleaned = amount_str.replace(',', '').replace(' ', '')
        
        try:
            return Decimal(cleaned)
        except:
            return Decimal('0')
    
    def _parse_disclosures(self, text: str) -> List[Dict]:
        """
        Parse disclosure notes and schedules
        """
        disclosures = []
        
        # Split by disclosure markers
        disclosure_pattern = r'(?:Note|Schedule)\s+(\d+)[:\s]+'
        sections = re.split(disclosure_pattern, text)
        
        for i in range(1, len(sections), 2):
            disc_num = sections[i]
            disc_text = sections[i + 1] if i + 1 < len(sections) else ''
            
            # Extract key information
            disclosure = {
                'number': disc_num,
                'text': disc_text[:500],  # First 500 chars
                'entities': self._extract_entities(disc_text),
                'numbers': self._extract_numbers(disc_text)
            }
            
            disclosures.append(disclosure)
        
        return disclosures
    
    def _extract_entities(self, text: str) -> List[Dict]:
        """
        Extract financial entities using NER
        """
        entities = []
        if self.nlp:
             doc = self.nlp(text)
             for ent in doc.ents:
                if ent.label_ in ['MONEY', 'DATE', 'PERCENT', 'ORG']:
                    entities.append({
                        'text': ent.text,
                        'type': ent.label_,
                        'start': ent.start_char,
                        'end': ent.end_char
                    })
        
        return entities
    
    def _extract_numbers(self, text: str) -> List[float]:
        """
        Extract all numerical values
        """
        pattern = r'-?\d+(?:[.,]\d{3})*(?:\.\d+)?'
        numbers = re.findall(pattern, text)
        
        return [float(n.replace(',', '')) for n in numbers]
    
    def _extract_metadata(self, pdf_path: str) -> Dict:
        """
        Extract document metadata
        """
        metadata = {}
        
        with pdfplumber.open(pdf_path) as pdf:
            # PDF metadata
            if pdf.metadata:
                metadata['title'] = pdf.metadata.get('Title')
                metadata['author'] = pdf.metadata.get('Author')
                metadata['creation_date'] = pdf.metadata.get('CreationDate')
            
            # Extract document info from content
            if len(pdf.pages) > 0:
                text = pdf.pages[0].extract_text()
                
                # Find company name
                metadata['company_name'] = self._extract_company_name(text)
                
                # Find financial year
                metadata['financial_year'] = self._extract_financial_year(text)
                
                # Find statement date
                metadata['statement_date'] = self._extract_date(text)
        
        return metadata
    
    def _extract_company_name(self, text: str) -> str:
        """Extract company name from text"""
        # Usually in first few lines
        if not text: return "Unknown"
        lines = text.split('\n')[:10]
        for line in lines:
            if len(line) > 10 and len(line) < 100:
                return line.strip()
        return "Unknown"
    
    def _extract_financial_year(self, text: str) -> str:
        """Extract financial year"""
        if not text: return None
        pattern = r'(?:FY|Year|Period)?\s*(?:20\d{2})[-\s](?:20\d{2})'
        match = re.search(pattern, text)
        if match:
            return match.group()
        return None
    
    def _extract_date(self, text: str) -> str:
        """Extract date from text"""
        if not text: return None
        pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{4}'
        match = re.search(pattern, text)
        if match:
            return match.group()
        return None
