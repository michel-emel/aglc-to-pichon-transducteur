#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ewondo Transcriptor: Essono (2012) to Pichon (1950)
==================================================

API script for transcribing Ewondo text with detailed rule tracking.
"""

import json
import sys
from typing import List, Dict, Tuple


class EwondoTranscriptor:
    """
    Transcriptor for Ewondo language from Essono system to Pichon system.
    Tracks all applied rules for detailed output.
    """
    
    def __init__(self):
        """Initialize correspondence tables and rules."""
        
        # Consonant mappings
        self.consonant_map = {
            'ŋ': 'ṅ',  # Only consonant that changes (caron → dot above)
        }
        
        # Vowel mappings (character by character)
        self.vowel_map = {
            'ə': 'ë',  # schwa → e with diaeresis
            'ɛ': 'è',  # epsilon → e with grave accent
            'ɔ': 'ò',  # open o → o with grave accent
        }
        
        # Tonal diacritics to remove
        self.tonal_diacritics = [
            '\u0300',  # ◌̀ low tone
            '\u0301',  # ◌́ high tone  
            '\u0304',  # ◌̄ mid tone
            '\u030C',  # ◌̌ rising tone
            '\u0302',  # ◌̂ falling tone
        ]
    
    def analyze_word(self, word: str) -> Dict:
        """
        Analyze and transcribe a single word with rule tracking.
        
        Args:
            word (str): Word in Essono system
            
        Returns:
            Dict: Contains original word, transcribed word, and applied rules
        """
        if not word.strip():
            return {
                'essono': word,
                'pichon': word,
                'rules': []
            }
        
        applied_rules = []
        current_word = word.strip()
        
        # Step 1: Convert consonants
        step1_word = current_word
        for essono_char, pichon_char in self.consonant_map.items():
            if essono_char in step1_word:
                step1_word = step1_word.replace(essono_char, pichon_char)
                applied_rules.append(f"Consonant: {essono_char} → {pichon_char}")
        
        # Step 2: Convert vowels (character by character)
        step2_word = ""
        for char in step1_word:
            if char in self.vowel_map:
                converted_char = self.vowel_map[char]
                step2_word += converted_char
                if f"Vowel: {char} → {converted_char}" not in applied_rules:
                    applied_rules.append(f"Vowel: {char} → {converted_char}")
            else:
                step2_word += char
        
        # Step 3: Remove tonal diacritics
        step3_word = step2_word
        tones_removed = []
        for diacritic in self.tonal_diacritics:
            if diacritic in step3_word:
                step3_word = step3_word.replace(diacritic, '')
                tone_names = {
                    '\u0300': 'low tone (◌̀)',
                    '\u0301': 'high tone (◌́)',
                    '\u0304': 'mid tone (◌̄)',
                    '\u030C': 'rising tone (◌̌)',
                    '\u0302': 'falling tone (◌̂)'
                }
                tones_removed.append(tone_names.get(diacritic, 'tone'))
        
        if tones_removed:
            applied_rules.append(f"Removed tones: {', '.join(set(tones_removed))}")
        
        # If no changes were made
        if not applied_rules:
            applied_rules.append("No changes needed")
        
        return {
            'essono': word.strip(),
            'pichon': step3_word,
            'rules': applied_rules
        }
    
    def transcribe_multiple(self, input_text: str) -> List[Dict]:
        """
        Transcribe multiple words separated by commas.
        
        Args:
            input_text (str): Words separated by commas
            
        Returns:
            List[Dict]: List of transcription results for each word
        """
        # Split by comma and clean each word
        words = [word.strip() for word in input_text.split(',') if word.strip()]
        
        results = []
        for word in words:
            result = self.analyze_word(word)
            results.append(result)
        
        return results


def main():
    """
    Main function for command line usage and API calls.
    """
    transcriptor = EwondoTranscriptor()
    
    if len(sys.argv) > 1:
        # Command line argument provided
        input_text = sys.argv[1]
        results = transcriptor.transcribe_multiple(input_text)
        
        # Output as JSON for the HTML interface
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        # Interactive mode
        print("=== EWONDO TRANSCRIPTOR: ESSONO → PICHON ===")
        print("Enter words separated by commas, or 'quit' to exit\n")
        
        while True:
            user_input = input("Enter Essono word(s): ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            elif user_input:
                results = transcriptor.transcribe_multiple(user_input)
                
                print("\n" + "="*60)
                print(f"{'ESSONO':<20} {'PICHON':<20} {'RULES APPLIED'}")
                print("="*60)
                
                for result in results:
                    rules_str = "; ".join(result['rules'])
                    print(f"{result['essono']:<20} {result['pichon']:<20} {rules_str}")
                
                print("="*60 + "\n")
            else:
                print("Please enter some text to transcribe.\n")


if __name__ == "__main__":
    main()