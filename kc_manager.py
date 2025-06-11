import json
import os
from typing import Dict, List, Tuple
from config import Config

class KCManager:
    """Manages Knowledge Components and their mastery levels"""
    
    def __init__(self):
        self.kc_data = {}
        self.load_kc_data()
    
    def load_kc_data(self):
        """Load KC mastery data from file"""
        try:
            if os.path.exists(Config.KC_MASTERY_FILE):
                with open(Config.KC_MASTERY_FILE, 'r') as f:
                    self.kc_data = json.load(f)
            else:
                # Initialize with default KCs for math
                self.kc_data = self.get_default_kcs()
                self.save_kc_data()
        except Exception as e:
            print(f"Error loading KC data: {e}")
            self.kc_data = self.get_default_kcs()
    
    def save_kc_data(self):
        """Save KC mastery data to file"""
        try:
            with open(Config.KC_MASTERY_FILE, 'w') as f:
                json.dump(self.kc_data, f, indent=2)
        except Exception as e:
            print(f"Error saving KC data: {e}")
    
    def get_default_kcs(self) -> Dict:
        """Return default knowledge components with mastery levels"""
        return {
            "basic_addition": {
                "name": "Basic Addition (single digit)",
                "mastery": 100,
                "keywords": ["add", "plus", "+", "sum"],
                "description": "Adding single digit numbers"
            },
            "carry_addition": {
                "name": "Addition with Carrying (two digit)",
                "mastery": 50,
                "keywords": ["carry", "two digit", "double digit"],
                "description": "Adding two digit numbers requiring carrying"
            },
            "basic_subtraction": {
                "name": "Basic Subtraction",
                "mastery": 100,
                "keywords": ["subtract", "minus", "-", "difference"],
                "description": "Basic subtraction operations"
            },
            "borrowing_subtraction": {
                "name": "Subtraction with Borrowing",
                "mastery": 0,
                "keywords": ["borrow", "regroup"],
                "description": "Subtraction requiring borrowing/regrouping"
            },
            "multiplication_tables": {
                "name": "Multiplication Tables",
                "mastery": 50,
                "keywords": ["multiply", "times", "×", "*"],
                "description": "Basic multiplication facts"
            },
            "long_multiplication": {
                "name": "Long Multiplication",
                "mastery": 0,
                "keywords": ["long multiplication", "multi-digit multiplication"],
                "description": "Multi-digit multiplication"
            },
            "basic_division": {
                "name": "Basic Division",
                "mastery": 0,
                "keywords": ["divide", "÷", "/", "division"],
                "description": "Basic division operations"
            },
            "place_value": {
                "name": "Place Value Understanding",
                "mastery": 100,
                "keywords": ["ones", "tens", "hundreds", "place value"],
                "description": "Understanding place value in numbers"
            }
        }
    
    def identify_relevant_kcs(self, question: str) -> List[Tuple[str, int]]:
        """Identify which KCs are relevant to a given question"""
        question_lower = question.lower()
        relevant_kcs = []
        
        for kc_id, kc_info in self.kc_data.items():
            for keyword in kc_info["keywords"]:
                if keyword in question_lower:
                    relevant_kcs.append((kc_id, kc_info["mastery"]))
                    break
        
        # Additional logic for number analysis
        if any(char.isdigit() for char in question):
            numbers = [int(s) for s in question.split() if s.isdigit()]
            if len(numbers) >= 2:
                # Check if it's addition with carrying
                if "+" in question and any(num > 9 for num in numbers):
                    if ("carry_addition", self.kc_data["carry_addition"]["mastery"]) not in relevant_kcs:
                        relevant_kcs.append(("carry_addition", self.kc_data["carry_addition"]["mastery"]))
        
        return relevant_kcs
    
    def get_kc_mastery(self, kc_id: str) -> int:
        """Get mastery level for a specific KC"""
        return self.kc_data.get(kc_id, {}).get("mastery", 0)
    
    def update_kc_mastery(self, kc_id: str, new_mastery: int):
        """Update mastery level for a KC"""
        if kc_id in self.kc_data:
            self.kc_data[kc_id]["mastery"] = max(0, min(100, new_mastery))
            self.save_kc_data()
    
    def get_all_kcs(self) -> Dict:
        """Get all knowledge components"""
        return self.kc_data
    
    def add_new_kc(self, kc_id: str, name: str, keywords: List[str], 
                   description: str, mastery: int = 0):
        """Add a new knowledge component"""
        self.kc_data[kc_id] = {
            "name": name,
            "mastery": mastery,
            "keywords": keywords,
            "description": description
        }
        self.save_kc_data()