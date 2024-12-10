#!/usr/bin/env python
import sys
from latest_ai_development.crew import LatestAiDevelopmentCrew
from datetime import datetime

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI Agents in 2024',
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)
