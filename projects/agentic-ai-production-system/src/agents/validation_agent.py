"""
Validation Agent - Ensures output quality and safety.
"""

import asyncio
import re
from typing import Dict, Any, List, Tuple
from .base_agent import BaseAgent

class ValidationAgent(BaseAgent):
    """Specialized agent for quality assurance and safety validation."""
    
    def __init__(self, config, logger):
        super().__init__("ValidationAgent", config, logger)
        self.safety_patterns = self._initialize_safety_patterns()
        self.quality_metrics = {
            "validations_performed": 0,
            "safety_issues_detected": 0,
            "quality_issues_detected": 0,
            "validations_passed": 0
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process validation request for content quality and safety."""
        
        if not self.validate_input(input_data):
            return {"error": "Invalid input data", "success": False}
        
        try:
            content = input_data.get("content", "")
            validation_type = input_data.get("validation_type", "comprehensive")
            strict_mode = input_data.get("strict_mode", False)
            
            self.logger.info(f"ValidationAgent: Validating content ({validation_type} mode)")
            
            self.quality_metrics["validations_performed"] += 1
            
            # Perform validation based on type
            if validation_type == "safety":
                result = await self._safety_validation(content, strict_mode)
            elif validation_type == "quality":
                result = await self._quality_validation(content, strict_mode)
            elif validation_type == "technical":
                result = await self._technical_validation(content, strict_mode)
            else:
                result = await self._comprehensive_validation(content, strict_mode)
            
            # Update metrics
            if result.get("success") and result.get("validation_passed"):
                self.quality_metrics["validations_passed"] += 1
            
            if result.get("safety_issues"):
                self.quality_metrics["safety_issues_detected"] += len(result["safety_issues"])
            
            if result.get("quality_issues"):
                self.quality_metrics["quality_issues_detected"] += len(result["quality_issues"])
            
            return result
            
        except Exception as e:
            self.logger.error(f"ValidationAgent: Error during validation: {str(e)}")
            return {
                "error": str(e),
                "success": False,
                "agent": self.name
            }
    
    async def _comprehensive_validation(self, content: str, strict_mode: bool) -> Dict[str, Any]:
        """Perform comprehensive validation including safety and quality checks."""
        
        # Run all validation types
        safety_result = await self._safety_validation(content, strict_mode)
        quality_result = await self._quality_validation(content, strict_mode)
        
        # Combine results
        all_issues = []
        if safety_result.get("safety_issues"):
            all_issues.extend(safety_result["safety_issues"])
        if quality_result.get("quality_issues"):
            all_issues.extend(quality_result["quality_issues"])
        
        validation_passed = len(all_issues) == 0
        
        return {
            "success": True,
            "validation_type": "comprehensive",
            "validation_passed": validation_passed,
            "content_length": len(content),
            "safety_score": safety_result.get("safety_score", 0),
            "quality_score": quality_result.get("quality_score", 0),
            "overall_score": (safety_result.get("safety_score", 0) + quality_result.get("quality_score", 0)) / 2,
            "issues": all_issues,
            "safety_issues": safety_result.get("safety_issues", []),
            "quality_issues": quality_result.get("quality_issues", []),
            "recommendations": self._generate_recommendations(all_issues),
            "strict_mode": strict_mode,
            "agent": self.name
        }
    
    async def _safety_validation(self, content: str, strict_mode: bool) -> Dict[str, Any]:
        """Perform safety validation to detect harmful or inappropriate content."""
        
        safety_issues = []
        
        # Pattern-based safety checks
        for category, patterns in self.safety_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    safety_issues.append({
                        "category": category,
                        "severity": "high" if strict_mode else "medium",
                        "description": f"Potential {category} content detected",
                        "pattern_matched": pattern[:50] + "..." if len(pattern) > 50 else pattern
                    })
        
        # LLM-based safety assessment
        llm_safety_result = await self._llm_safety_check(content)
        if llm_safety_result.get("issues"):
            safety_issues.extend(llm_safety_result["issues"])
        
        # Calculate safety score
        safety_score = max(0, 100 - (len(safety_issues) * 20))
        
        return {
            "success": True,
            "validation_type": "safety",
            "validation_passed": len(safety_issues) == 0,
            "safety_score": safety_score,
            "safety_issues": safety_issues,
            "content_length": len(content),
            "strict_mode": strict_mode,
            "agent": self.name
        }
    
    async def _quality_validation(self, content: str, strict_mode: bool) -> Dict[str, Any]:
        """Perform quality validation to assess content quality and coherence."""
        
        quality_issues = []
        
        # Basic quality checks
        quality_issues.extend(self._check_basic_quality(content, strict_mode))
        
        # LLM-based quality assessment
        llm_quality_result = await self._llm_quality_check(content)
        if llm_quality_result.get("issues"):
            quality_issues.extend(llm_quality_result["issues"])
        
        # Calculate quality score
        quality_score = max(0, 100 - (len(quality_issues) * 15))
        
        return {
            "success": True,
            "validation_type": "quality",
            "validation_passed": len(quality_issues) == 0,
            "quality_score": quality_score,
            "quality_issues": quality_issues,
            "content_length": len(content),
            "readability_score": self._calculate_readability_score(content),
            "strict_mode": strict_mode,
            "agent": self.name
        }
    
    async def _technical_validation(self, content: str, strict_mode: bool) -> Dict[str, Any]:
        """Perform technical validation for code, documentation, or technical content."""
        
        technical_issues = []
        
        # Check for code blocks and validate syntax
        code_blocks = re.findall(r'```[\w]*\n(.*?)\n```', content, re.DOTALL)
        for i, code_block in enumerate(code_blocks):
            code_issues = self._validate_code_block(code_block, i)
            technical_issues.extend(code_issues)
        
        # Check technical terminology consistency
        terminology_issues = self._check_terminology_consistency(content)
        technical_issues.extend(terminology_issues)
        
        # LLM-based technical assessment
        llm_technical_result = await self._llm_technical_check(content)
        if llm_technical_result.get("issues"):
            technical_issues.extend(llm_technical_result["issues"])
        
        # Calculate technical score
        technical_score = max(0, 100 - (len(technical_issues) * 10))
        
        return {
            "success": True,
            "validation_type": "technical",
            "validation_passed": len(technical_issues) == 0,
            "technical_score": technical_score,
            "technical_issues": technical_issues,
            "code_blocks_found": len(code_blocks),
            "content_length": len(content),
            "strict_mode": strict_mode,
            "agent": self.name
        }
    
    async def _llm_safety_check(self, content: str) -> Dict[str, Any]:
        """Use LLM to perform safety assessment."""
        
        messages = [
            {
                "role": "system",
                "content": """You are a content safety specialist. Analyze the given content for potential safety issues.
                
                Check for:
                - Harmful or dangerous instructions
                - Inappropriate or offensive content
                - Misinformation or misleading claims
                - Privacy violations
                - Bias or discrimination
                
                Respond with a JSON structure:
                {
                    "safe": true/false,
                    "issues": [{"type": "issue_type", "severity": "low/medium/high", "description": "details"}],
                    "confidence": "low/medium/high"
                }"""
            },
            {
                "role": "user",
                "content": f"Analyze this content for safety issues:\n\n{content[:2000]}"  # Limit content length
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=400)
            
            # Parse response (simplified - in production, use proper JSON parsing)
            issues = []
            if "unsafe" in response.lower() or "harmful" in response.lower():
                issues.append({
                    "type": "potential_safety_concern",
                    "severity": "medium",
                    "description": "LLM detected potential safety concerns",
                    "details": response[:200]
                })
            
            return {
                "issues": issues,
                "llm_response": response
            }
            
        except Exception as e:
            self.logger.error(f"ValidationAgent: LLM safety check failed: {str(e)}")
            return {"issues": []}
    
    async def _llm_quality_check(self, content: str) -> Dict[str, Any]:
        """Use LLM to perform quality assessment."""
        
        messages = [
            {
                "role": "system",
                "content": """You are a content quality specialist. Analyze the given content for quality issues.
                
                Assess:
                - Clarity and coherence
                - Grammar and style
                - Logical structure
                - Completeness
                - Accuracy (where verifiable)
                
                Identify specific areas for improvement."""
            },
            {
                "role": "user",
                "content": f"Analyze this content for quality issues:\n\n{content[:2000]}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=300)
            
            # Parse response for quality issues
            issues = []
            quality_keywords = ["unclear", "confusing", "incomplete", "error", "improve"]
            
            if any(keyword in response.lower() for keyword in quality_keywords):
                issues.append({
                    "type": "quality_concern",
                    "severity": "low",
                    "description": "LLM identified potential quality improvements",
                    "details": response[:200]
                })
            
            return {
                "issues": issues,
                "llm_response": response
            }
            
        except Exception as e:
            self.logger.error(f"ValidationAgent: LLM quality check failed: {str(e)}")
            return {"issues": []}
    
    async def _llm_technical_check(self, content: str) -> Dict[str, Any]:
        """Use LLM to perform technical assessment."""
        
        messages = [
            {
                "role": "system",
                "content": """You are a technical content specialist. Analyze the given content for technical accuracy and completeness.
                
                Check for:
                - Technical accuracy
                - Code syntax and best practices
                - Documentation completeness
                - Proper terminology usage
                - Missing technical details
                
                Focus on actionable technical improvements."""
            },
            {
                "role": "user",
                "content": f"Analyze this technical content:\n\n{content[:2000]}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=300)
            
            # Parse response for technical issues
            issues = []
            technical_keywords = ["incorrect", "missing", "syntax", "deprecated", "outdated"]
            
            if any(keyword in response.lower() for keyword in technical_keywords):
                issues.append({
                    "type": "technical_concern",
                    "severity": "medium",
                    "description": "LLM identified potential technical issues",
                    "details": response[:200]
                })
            
            return {
                "issues": issues,
                "llm_response": response
            }
            
        except Exception as e:
            self.logger.error(f"ValidationAgent: LLM technical check failed: {str(e)}")
            return {"issues": []}
    
    def _check_basic_quality(self, content: str, strict_mode: bool) -> List[Dict[str, Any]]:
        """Perform basic quality checks."""
        
        issues = []
        
        # Check content length
        if len(content) < 10:
            issues.append({
                "type": "length",
                "severity": "high",
                "description": "Content too short to be meaningful"
            })
        
        # Check for excessive repetition
        words = content.lower().split()
        if len(words) > 0:
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            max_freq = max(word_freq.values())
            if max_freq > len(words) * 0.1:  # More than 10% repetition
                issues.append({
                    "type": "repetition",
                    "severity": "medium",
                    "description": "Excessive word repetition detected"
                })
        
        # Check for proper sentence structure
        sentences = re.split(r'[.!?]+', content)
        short_sentences = [s for s in sentences if len(s.strip()) < 5]
        if len(short_sentences) > len(sentences) * 0.3:
            issues.append({
                "type": "structure",
                "severity": "low",
                "description": "Many very short sentences detected"
            })
        
        return issues
    
    def _validate_code_block(self, code: str, block_index: int) -> List[Dict[str, Any]]:
        """Validate code blocks for basic syntax issues."""
        
        issues = []
        
        # Check for balanced brackets
        brackets = {'(': ')', '[': ']', '{': '}'}
        stack = []
        
        for char in code:
            if char in brackets:
                stack.append(char)
            elif char in brackets.values():
                if not stack or brackets.get(stack.pop()) != char:
                    issues.append({
                        "type": "syntax",
                        "severity": "high",
                        "description": f"Unbalanced brackets in code block {block_index + 1}"
                    })
                    break
        
        if stack:
            issues.append({
                "type": "syntax",
                "severity": "high",
                "description": f"Unclosed brackets in code block {block_index + 1}"
            })
        
        return issues
    
    def _check_terminology_consistency(self, content: str) -> List[Dict[str, Any]]:
        """Check for consistent terminology usage."""
        
        issues = []
        
        # Common technical term variations
        term_variations = {
            "javascript": ["javascript", "js", "JavaScript", "JS"],
            "python": ["python", "Python", "PYTHON"],
            "api": ["api", "API", "Api"]
        }
        
        for base_term, variations in term_variations.items():
            found_variations = [var for var in variations if var in content]
            if len(found_variations) > 1:
                issues.append({
                    "type": "terminology",
                    "severity": "low",
                    "description": f"Inconsistent terminology for '{base_term}': {found_variations}"
                })
        
        return issues
    
    def _calculate_readability_score(self, content: str) -> float:
        """Calculate a simple readability score."""
        
        sentences = re.split(r'[.!?]+', content)
        words = content.split()
        
        if len(sentences) == 0 or len(words) == 0:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Simple readability score (lower is better)
        # Ideal sentence length is around 15-20 words
        if avg_sentence_length <= 20:
            return min(100, (20 - abs(avg_sentence_length - 15)) * 5)
        else:
            return max(0, 100 - (avg_sentence_length - 20) * 2)
    
    def _generate_recommendations(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on identified issues."""
        
        recommendations = []
        
        issue_types = [issue["type"] for issue in issues]
        
        if "safety" in issue_types:
            recommendations.append("Review content for potential safety concerns and revise as needed")
        
        if "quality" in issue_types:
            recommendations.append("Improve content clarity, structure, and completeness")
        
        if "syntax" in issue_types:
            recommendations.append("Check code blocks for syntax errors and proper formatting")
        
        if "terminology" in issue_types:
            recommendations.append("Ensure consistent terminology usage throughout the content")
        
        if not recommendations:
            recommendations.append("Content meets validation standards")
        
        return recommendations
    
    def _initialize_safety_patterns(self) -> Dict[str, List[str]]:
        """Initialize safety patterns for content filtering."""
        
        return {
            "personal_info": [
                r'\b\d{3}-\d{2}-\d{4}\b',  # SSN pattern
                r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit card pattern
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email pattern
            ],
            "harmful_instructions": [
                r'\b(how to (make|create|build).*(bomb|explosive|weapon))\b',
                r'\b(illegal|unlawful|criminal)\s+(activity|action|method)\b'
            ],
            "inappropriate_content": [
                r'\b(explicit|graphic|violent)\s+(content|material|description)\b'
            ]
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate validation-specific input data."""
        
        if not super().validate_input(input_data):
            return False
        
        # Check for content to validate
        content = input_data.get("content", "")
        if not content:
            self.logger.error(f"{self.name}: No content provided for validation")
            return False
        
        # Validate validation type
        valid_types = ["safety", "quality", "technical", "comprehensive"]
        validation_type = input_data.get("validation_type", "comprehensive")
        if validation_type not in valid_types:
            self.logger.error(f"{self.name}: Invalid validation type: {validation_type}")
            return False
        
        return True
    
    def get_validation_metrics(self) -> Dict[str, Any]:
        """Get validation performance metrics."""
        
        total_validations = self.quality_metrics["validations_performed"]
        pass_rate = (self.quality_metrics["validations_passed"] / total_validations * 100) if total_validations > 0 else 0
        
        return {
            **self.quality_metrics,
            "pass_rate": round(pass_rate, 2),
            "avg_safety_issues": round(self.quality_metrics["safety_issues_detected"] / max(1, total_validations), 2),
            "avg_quality_issues": round(self.quality_metrics["quality_issues_detected"] / max(1, total_validations), 2)
        }