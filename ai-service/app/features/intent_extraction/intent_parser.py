"""
Feature: Intent Extraction
File Purpose: Extract travel parameters from user input
Owner: Yug
Dependencies: LLM API
Last Updated: Initial Setup
"""
import json
import os

class IntentParser:
    def __init__(self, llmClient):
        self.llmClient = llmClient
        # 1. Get current directory (intent_extraction folder)
        currentDir = os.path.dirname(os.path.abspath(__file__))
        
        self.promptPath = os.path.join(currentDir, "..", "..", "prompts", "trip_prompt.txt")

    def parse_user_intent(self, userQuery: str):
        with open(self.promptPath, "r") as file:
            template = file.read()
        
        formattedPrompt = template.replace("{UserQuery}", userQuery)
        
        # In a real scenario, call your LLM API here
        # rawResponse = self.llmClient.generate(formattedPrompt)
        
        # Mocking the LLM Response for logic demonstration
        mockParsedData = {
            "destinationCity": "Goa",
            "durationDays": 3,
            "budgetLevel": "moderate",
            "travelInterests": ["beach", "water-sports"],
            "travelerGroup": "friends"
        }
        return mockParsedData