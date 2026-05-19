class WhatIfSimulator:

    def __init__(self, rag):

        self.rag = rag

    def simulate(self, company, scenario):

        prompt = f"""
        You are an AI Financial Strategy Simulator.

        Company:
        {company}

        Scenario:
        {scenario}

        Analyze:

        - financial impact
        - revenue effect
        - operational challenges
        - investor sentiment
        - risk escalation
        - long-term strategic consequences

        Provide a detailed executive-level simulation.
        """

        return self.rag.ask_question(prompt)