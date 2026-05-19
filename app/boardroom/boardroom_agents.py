class BoardroomAgents:

    def __init__(self, rag):

        self.rag = rag

    # ============================================
    # Research Agent
    # ============================================

    def research_agent(self, query):

        prompt = f"""
        You are a Financial Research Agent.

        Analyze:
        {query}

        Focus on:
        - revenue trends
        - financial performance
        - market growth
        - operational analysis
        """

        return self.rag.ask_question(prompt)

    # ============================================
    # Risk Agent
    # ============================================

    def risk_agent(self, query):

        prompt = f"""
        You are a Financial Risk Agent.

        Analyze:
        {query}

        Focus on:
        - business risks
        - operational risks
        - supply chain risks
        - geopolitical risks
        - financial vulnerabilities
        """

        return self.rag.ask_question(prompt)

    # ============================================
    # Investment Agent
    # ============================================

    def investment_agent(self, query):

        prompt = f"""
        You are an Investment Analysis Agent.

        Analyze:
        {query}

        Provide:
        - bullish signals
        - bearish signals
        - investor perspective
        - valuation analysis
        """

        return self.rag.ask_question(prompt)

    # ============================================
    # Strategy Agent
    # ============================================

    def strategy_agent(self, query):

        prompt = f"""
        You are a Corporate Strategy Agent.

        Analyze:
        {query}

        Focus on:
        - future growth
        - AI opportunities
        - expansion strategy
        - innovation
        - market positioning
        """

        return self.rag.ask_question(prompt)

    # ============================================
    # CEO Agent
    # ============================================

    def ceo_agent(self, query):

        prompt = f"""
        You are a CEO Executive Advisor.

        Based on:
        {query}

        Provide:
        - executive recommendations
        - strategic direction
        - leadership decisions
        - final boardroom summary
        """

        return self.rag.ask_question(prompt)