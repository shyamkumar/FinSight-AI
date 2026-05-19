class DebateAgents:

    def __init__(self, rag):

        self.rag = rag

    # ============================================
    # BULL AGENT
    # ============================================

    def bull_agent(self, query):

        prompt = f"""
        You are a Bullish Investment Agent.

        Analyze:
        {query}

        Strongly argue WHY this company is a good investment.

        Focus on:
        - growth potential
        - innovation
        - AI opportunities
        - financial strength
        - market leadership
        """

        return self.rag.ask_question(prompt)

    # ============================================
    # BEAR AGENT
    # ============================================

    def bear_agent(self, query):

        prompt = f"""
        You are a Bearish Investment Agent.

        Analyze:
        {query}

        Strongly argue WHY investors should be cautious.

        Focus on:
        - valuation concerns
        - risks
        - competition
        - operational weaknesses
        - macroeconomic threats
        """

        return self.rag.ask_question(prompt)

    # ============================================
    # RISK AGENT
    # ============================================

    def risk_agent(self, query):

        prompt = f"""
        You are a Financial Risk Agent.

        Analyze:
        {query}

        Focus on:
        - supply chain risks
        - financial risks
        - geopolitical risks
        - AI risks
        - regulatory concerns
        """

        return self.rag.ask_question(prompt)

    # ============================================
    # MODERATOR AGENT
    # ============================================

    def moderator_agent(self, query):

        prompt = f"""
        You are an Executive Financial Moderator.

        Analyze:
        {query}

        Provide:
        - balanced perspective
        - final investment conclusion
        - strategic recommendation
        """

        return self.rag.ask_question(prompt)