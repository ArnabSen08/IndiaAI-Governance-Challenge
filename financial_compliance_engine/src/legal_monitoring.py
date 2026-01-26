import spacy
import re
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

class LegalDataIngestor:
    """
    Simulates real-time data ingestion from legal and regulatory sources.
    """
    def __init__(self):
        pass
        
    def fetch_live_feed(self) -> List[Dict]:
        """
        Simulate fetching live alerts.
        In a real system, this would connect to RSS feeds, Web Scrapers, or APIs.
        """
        return [
             {
                'id': 'L-101',
                'timestamp': datetime.now().isoformat(),
                'source': 'SEBI Enforcement',
                'title': 'Order in the matter of ABC Technologies Ltd',
                'content': 'SEBI has imposed a penalty of Rs. 10 Lakhs on ABC Technologies for non-compliance with LODR regulations regarding disclosure of material events. The investigation revealed insider trading patterns.',
                'link': 'https://sebi.gov.in/orders/abc-tech'
            },
            {
                'id': 'L-102',
                'timestamp': datetime.now().isoformat(),
                'source': 'Whistleblower Portal',
                'title': 'Allegation of Fund Diversion',
                'content': 'A whistleblower report alleges that XYZ Corp has diverted funds to a shell company in Mauritius. The CFO is allegedly involved in falsifying invoices.',
                'link': 'internal://whistleblower/case-882'
            },
            {
                'id': 'L-103',
                'timestamp': datetime.now().isoformat(),
                'source': 'Court Judgment',
                'title': 'Civil Dispute: Vendor vs DEMO_CORP',
                'content': 'The High Court has issued a notice to DEMO_CORP regarding unpaid dues of Rs. 50 Crores to a vendor. The company has 4 weeks to respond.',
                'link': 'https://highcourt.gov.in/cases/2025/112'
            },
             {
                'id': 'L-104',
                'timestamp': datetime.now().isoformat(),
                'source': 'RBI Notification',
                'title': 'General banking compliance update',
                'content': 'RBI issues new guidelines for KYC norms. All banks to ensure compliance by next quarter.',
                'link': 'https://rbi.org.in/notifications'
            }
        ]

class LegalAnalyzer:
    """
    Analyzes legal text for entities and risk.
    """
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except:
             try:
                 self.nlp = spacy.load("en_core_web_sm")
             except:
                 self.nlp = spacy.blank("en")

    def analyze_event(self, event: Dict) -> Dict:
        """
        Enrich event with NER and Risk Score.
        """
        text = event['content']
        
        # 1. Entity Recognition
        entities = self._extract_entities(text)
        
        # 2. Risk Scoring
        risk_profile = self._calculate_risk_score(text, event['source'])
        
        enriched_event = {
            **event,
            'entities': entities,
            'risk_score': risk_profile['score'],
            'risk_level': risk_profile['level'],
            'risk_factors': risk_profile['factors']
        }
        
        return enriched_event

    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        doc = self.nlp(text)
        
        extracted = {
            'Organizations': [],
            'Persons': [],
            'Money': [],
            'Laws': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                extracted['Organizations'].append(ent.text)
            elif ent.label_ == 'PERSON':
                extracted['Persons'].append(ent.text)
            elif ent.label_ == 'MONEY':
                extracted['Money'].append(ent.text)
            elif ent.label_ == 'LAW': # Spacy has LAW entity support in some models
                extracted['Laws'].append(ent.text)
        
        # Fallback/Custom Regex for Laws if model misses them
        law_patterns = r'(?:Section\s+\d+|Act|Regulation\s+\d+)'
        laws = re.findall(law_patterns, text, re.IGNORECASE)
        extracted['Laws'].extend(laws)
        
        # Dedup
        for k in extracted:
            extracted[k] = list(set(extracted[k]))
            
        return extracted

    def _calculate_risk_score(self, text: str, source: str) -> Dict:
        """
        Calculate risk score based on keywords and source.
        """
        text_lower = text.lower()
        score = 0
        factors = []
        
        # Keyword Weights
        keywords = {
            'critical': {
                'fraud': 90, 'money laundering': 90, 'ban': 90, 'insider trading': 85,
                'arrest': 85, 'rbi penalty': 80, 'sebi order': 75, 'diversion': 80
            },
            'high': {
                'penalty': 60, 'fine': 60, 'non-compliance': 55, 'show cause': 50,
                'violation': 50, 'falsifying': 60
            },
            'medium': {
                'notice': 30, 'delay': 25, 'warning': 30, 'inquiry': 30, 'dispute': 25
            },
            'low': {
                'guidelines': 10, 'update': 5, 'notification': 5
            }
        }
        
        # Check Critical
        for kw, weight in keywords['critical'].items():
            if kw in text_lower:
                score = max(score, weight)
                factors.append(f"Critical Keyword: {kw}")
        
        # Check High
        for kw, weight in keywords['high'].items():
            if kw in text_lower:
                score = max(score, weight)
                factors.append(f"High Risk Keyword: {kw}")
                
        # Check Medium/Low if score is still low
        if score < 50:
             for kw, weight in keywords['medium'].items():
                if kw in text_lower:
                    score = max(score, weight)
                    factors.append(f"Medium Risk Keyword: {kw}")
        
        if score < 20:
             for kw, weight in keywords['low'].items():
                if kw in text_lower:
                    score = max(score, weight)
                    factors.append(f"Low Risk Keyword: {kw}")
        
        # Source Multiplier
        if source == 'Whistleblower Portal':
            score = max(score, 70) # Whistleblower allegations are always high risk until proven otherwise
            factors.append("Source: Whistleblower")
        elif source == 'SEBI Enforcement' and score < 50:
            score = max(score, 50)
            factors.append("Source: Regulatory Enforcement")
            
        # Determine Level
        if score >= 80: level = 'CRITICAL'
        elif score >= 50: level = 'HIGH'
        elif score >= 20: level = 'MEDIUM'
        else: level = 'LOW'
        
        return {
            'score': score,
            'level': level,
            'factors': factors
        }
