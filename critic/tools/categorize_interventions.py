#!/usr/bin/env python3
"""Categorize @ADMIN interventions by trigger type."""

import json
import re
from pathlib import Path
from collections import defaultdict

# Trigger patterns
TRIGGER_PATTERNS = {
    'BOUNDARY_VIOLATION': [
        r'keep it in your own lane',
        r'stay in your lane',
        r'own workspace',
        r'not touch that',
        r'don\'t touch',
        r'workspace sovereignty'
    ],
    'TOOL_MISUSE': [
        r'tools\.md',
        r'native.*shell',
        r'Read.*instead',
        r'Write.*instead',
        r'bash.*grep',
        r'could Read',
        r'grep.*discouraged',
        r'Glob.*find'
    ],
    'ARCHITECTURE_DRIFT': [
        r'better idea',
        r'We use tmux',
        r'correction:',
        r'wrong approach',
        r'not how we',
        r'scratch that'
    ],
    'EFFICIENCY_LOSS': [
        r'one at a time',
        r'don\'t batch',
        r'over-?engineer',
        r'too complex',
        r'simpler',
        r'directly'
    ],
    'PROGRESS_STALL': [
        r'interrupting',
        r'hiccup',
        r'hold off',
        r'wait',
        r'finish.*now',
        r'let.*finish'
    ],
    'QUALITY_ISSUE': [
        r'chmod',
        r'git commit',
        r'test',
        r'verify',
        r'check',
        r'ensure'
    ],
    'SUPPORTIVE': [
        r'great',
        r'perfect',
        r'nice',
        r'brilliant',
        r'cool',
        r'thanks',
        r'welcome'
    ],
    'DIRECTIVE': [
        r'please',
        r'need',
        r'want',
        r'should',
        r'must',
        r'let\'s'
    ]
}

def categorize_intervention(text):
    """Categorize an intervention by its trigger type."""
    text_lower = text.lower()
    categories = []
    
    for category, patterns in TRIGGER_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                categories.append(category)
                break
    
    # If no specific category found, default to DIRECTIVE
    if not categories:
        categories.append('DIRECTIVE')
    
    return categories

def analyze_tone(text):
    """Analyze the tone of the intervention."""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['sorry', 'my bad', 'apologies']):
        return 'apologetic'
    elif any(word in text_lower for word in ['great', 'perfect', 'nice', 'brilliant']):
        return 'supportive'
    elif any(word in text_lower for word in ['nope', 'don\'t', 'stop', 'wait']):
        return 'corrective'
    elif '!' in text and not '!!' in text:
        return 'enthusiastic'
    elif '?' in text:
        return 'questioning'
    else:
        return 'neutral'

def main():
    input_file = Path('critic/analysis/outputs/2025-01-27_admin_interventions.json')
    output_file = Path('critic/analysis/outputs/2025-01-27_categorized_interventions.json')
    
    with open(input_file, 'r') as f:
        interventions = json.load(f)
    
    categorized = []
    category_counts = defaultdict(int)
    tone_counts = defaultdict(int)
    
    for intervention in interventions:
        text = intervention['intervention_text']
        timestamp = intervention['timestamp']
        session_id = intervention['session_id']
        
        # Skip if it's formatted weirdly
        if text.startswith("[{'"):
            # Try to extract actual text
            match = re.search(r"'text': ['\"]([^'\"]+)['\"]", text)
            if match:
                text = match.group(1)
            else:
                continue
        
        categories = categorize_intervention(text)
        tone = analyze_tone(text)
        
        for cat in categories:
            category_counts[cat] += 1
        tone_counts[tone] += 1
        
        categorized.append({
            'timestamp': timestamp,
            'session_id': session_id,
            'text': text,
            'categories': categories,
            'tone': tone,
            'length': len(text),
            'has_code': '`' in text,
            'is_question': '?' in text
        })
    
    # Sort by timestamp
    categorized.sort(key=lambda x: x['timestamp'])
    
    # Analysis summary
    summary = {
        'total_interventions': len(categorized),
        'category_distribution': dict(category_counts),
        'tone_distribution': dict(tone_counts),
        'avg_length': sum(i['length'] for i in categorized) / len(categorized) if categorized else 0,
        'questions': sum(1 for i in categorized if i['is_question']),
        'with_code': sum(1 for i in categorized if i['has_code'])
    }
    
    # Save results
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump({
            'summary': summary,
            'interventions': categorized
        }, f, indent=2)
    
    # Print summary
    print(f"Categorized {summary['total_interventions']} interventions")
    print("\nCategory Distribution:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / summary['total_interventions']) * 100
        print(f"  {cat:20s}: {count:3d} ({percentage:5.1f}%)")
    
    print("\nTone Distribution:")
    for tone, count in sorted(tone_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / summary['total_interventions']) * 100
        print(f"  {tone:12s}: {count:3d} ({percentage:5.1f}%)")
    
    print(f"\nAverage length: {summary['avg_length']:.0f} characters")
    print(f"Questions: {summary['questions']} ({(summary['questions']/summary['total_interventions'])*100:.1f}%)")
    print(f"With code: {summary['with_code']} ({(summary['with_code']/summary['total_interventions'])*100:.1f}%)")

if __name__ == '__main__':
    main()