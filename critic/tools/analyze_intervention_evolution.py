#!/usr/bin/env python3
"""Analyze how intervention patterns evolve over time."""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

def parse_timestamp(ts):
    """Parse timestamp to datetime object."""
    # Handle different timestamp formats
    if ts.endswith('Z'):
        ts = ts[:-1] + '+00:00'
    return datetime.fromisoformat(ts.replace('Z', '+00:00'))

def get_time_bucket(timestamp):
    """Get time bucket (day and hour) for grouping."""
    dt = parse_timestamp(timestamp)
    return dt.strftime('%Y-%m-%d'), dt.hour

def main():
    input_file = Path('critic/analysis/outputs/2025-01-27_categorized_interventions.json')
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    interventions = data['interventions']
    
    # Group by day
    by_day = defaultdict(list)
    for inv in interventions:
        day, _ = get_time_bucket(inv['timestamp'])
        by_day[day].append(inv)
    
    # Analyze patterns over time
    print("Intervention Evolution Analysis")
    print("=" * 60)
    
    for day in sorted(by_day.keys()):
        day_interventions = by_day[day]
        
        # Category distribution for the day
        categories = []
        for inv in day_interventions:
            categories.extend(inv['categories'])
        cat_counts = Counter(categories)
        
        # Tone distribution
        tone_counts = Counter(inv['tone'] for inv in day_interventions)
        
        # Key metrics
        avg_length = sum(inv['length'] for inv in day_interventions) / len(day_interventions)
        questions = sum(1 for inv in day_interventions if inv['is_question'])
        
        print(f"\n{day} ({len(day_interventions)} interventions)")
        print("-" * 40)
        
        # Top categories
        print("Top Categories:")
        for cat, count in cat_counts.most_common(3):
            percentage = (count / len(day_interventions)) * 100
            print(f"  {cat}: {count} ({percentage:.0f}%)")
        
        # Dominant tone
        dominant_tone = tone_counts.most_common(1)[0]
        print(f"Dominant Tone: {dominant_tone[0]} ({dominant_tone[1]} times)")
        
        # Metrics
        print(f"Avg Length: {avg_length:.0f} chars")
        print(f"Questions: {questions}/{len(day_interventions)} ({(questions/len(day_interventions)*100):.0f}%)")
    
    # Specific pattern analysis
    print("\n\nPattern Evolution:")
    print("-" * 40)
    
    # Tool misuse over time
    tool_misuse_by_day = {}
    for day in sorted(by_day.keys()):
        tool_misuse = sum(1 for inv in by_day[day] if 'TOOL_MISUSE' in inv['categories'])
        tool_misuse_by_day[day] = (tool_misuse, len(by_day[day]))
    
    print("\nTool Misuse Interventions:")
    for day, (misuse, total) in tool_misuse_by_day.items():
        percentage = (misuse / total * 100) if total > 0 else 0
        print(f"  {day}: {misuse}/{total} ({percentage:.0f}%)")
    
    # Supportive vs Corrective balance
    print("\nTone Balance:")
    for day in sorted(by_day.keys()):
        supportive = sum(1 for inv in by_day[day] if inv['tone'] == 'supportive')
        corrective = sum(1 for inv in by_day[day] if inv['tone'] == 'corrective')
        total = len(by_day[day])
        print(f"  {day}: Supportive {supportive}/{total} ({supportive/total*100:.0f}%), Corrective {corrective}/{total} ({corrective/total*100:.0f}%)")
    
    # Learning indicators - do certain issues decrease?
    print("\nLearning Indicators:")
    
    # Early vs Late comparison
    all_days = sorted(by_day.keys())
    if len(all_days) >= 2:
        early_day = all_days[0]
        late_day = all_days[-1]
        
        early_cats = []
        for inv in by_day[early_day]:
            early_cats.extend(inv['categories'])
        
        late_cats = []
        for inv in by_day[late_day]:
            late_cats.extend(inv['categories'])
        
        early_counter = Counter(early_cats)
        late_counter = Counter(late_cats)
        
        print(f"\nComparing {early_day} (early) vs {late_day} (late):")
        
        # Categories that decreased
        for cat in set(early_counter.keys()) | set(late_counter.keys()):
            early_pct = (early_counter.get(cat, 0) / len(by_day[early_day])) * 100
            late_pct = (late_counter.get(cat, 0) / len(by_day[late_day])) * 100
            
            if early_pct > late_pct + 5:  # Decreased by more than 5%
                print(f"  ↓ {cat}: {early_pct:.0f}% → {late_pct:.0f}% (improved)")
            elif late_pct > early_pct + 5:  # Increased by more than 5%
                print(f"  ↑ {cat}: {early_pct:.0f}% → {late_pct:.0f}% (worsened)")

if __name__ == '__main__':
    main()