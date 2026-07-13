"""Resolve project paths so the app works no matter the current working directory."""
import os

# this file is <root>/utils/paths.py -> go up 2 levels to the project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACTS = os.path.join(ROOT, "artifacts")
LEXICON = os.path.join(ROOT, "colloquial-indonesian-lexicon.csv")
