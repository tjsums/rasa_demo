import os
import sys

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

sys.argv.append('run')
sys.argv.append('actions')
from rasa.__main__ import main

main()
