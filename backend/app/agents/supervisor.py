"""
Supervisor Agent

Central orchestrator for the Multi-Agent Document AI system.

Responsibilities:
    - Understand the user's request
    - Create an execution plan
    - Decide which agents are required
    - Support the Chat API through execute()
    - Keep compatibility with workflow.py and test files
    - Return a structured plan that downstream agents can execute

Supported capabilities:
    - Document analysis
    - PPT analysis
    - Web research
    - RAG
    - DOCX generation
    - PPTX generation
    - Validation
    - Conversational editing
"""

from __future__ import annotations

from typing import Any


class SupervisorAgent:
    """
    Central supervisor/orchestrator.

    High-level architecture:

        User Request
             |
             v
        Supervisor
             |
             +----> Document Agent
             |
             +----> PPT Agent
             |
             +----> Research Agent
             |
             +----> RAG Agent
             |
             +----> Document Generator
             |
             +----> PPT Generator
             |
             +----> Editing Agent
             |
             +----> Validation Agent
    """

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        """
        Initialize the SupervisorAgent.

        Agent objects are intentionally imported lazily so that:
        - importing the supervisor does not unnecessarily initialize
          external services;
        - Gemini/Tavily quota errors do not happen during import;
        - unit tests can test planning independently.
        """

        self.agent_name = "SupervisorAgent"

        self.available_agents = [
            "document",
            "ppt",
            "research",
            "rag",
            "document_generator",
            "ppt_generator",
            "editing",
            "validation",
        ]

    # ------------------------------------------------------------------
    # Request Classification
    # ------------------------------------------------------------------

    def _normalize_query(self, query: str) -> str:
        """
        Normalize the user query.
        """

        if query is None:
            return ""

        return str(query).strip()

    # ------------------------------------------------------------------

    def _contains_any(
        self,
        text: str,
        keywords: list[str],
    ) -> bool:
        """
        Return True when at least one keyword exists in the text.
        """

        text = text.lower()

        return any(
            keyword.lower() in text
            for keyword in keywords
        )

    # ------------------------------------------------------------------
    # Plan
    # ------------------------------------------------------------------

    def plan(
        self,
        query: str = "",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Create an execution plan for a user request.

        IMPORTANT:
            query is optional and accepts keyword arguments.

        This keeps compatibility with code such as:

            supervisor.plan(query="create a presentation")

        and:

            supervisor.plan(
                query="research AI trends"
            )
        """

        # --------------------------------------------------------------
        # Accept alternative query names for compatibility
        # --------------------------------------------------------------

        if not query:
            query = kwargs.get("request", "")

        if not query:
            query = kwargs.get("user_query", "")

        query = self._normalize_query(query)

        # --------------------------------------------------------------
        # Empty query
        # --------------------------------------------------------------

        if not query:
            return {
                "query": "",
                "status": "invalid",
                "message": "Query cannot be empty.",

                "needs_document_analysis": False,
                "needs_ppt_analysis": False,
                "needs_research": False,
                "needs_rag": False,
                "needs_document_generation": False,
                "needs_ppt_generation": False,
                "needs_editing": False,
                "needs_validation": False,

                "agents": [],
                "steps": [],
            }

        text = query.lower()

        # --------------------------------------------------------------
        # Detect request type
        # --------------------------------------------------------------

        needs_document_analysis = self._contains_any(
            text,
            [
                "document",
                "docx",
                "pdf",
                "word file",
                "analyze document",
                "analyse document",
                "uploaded file",
            ],
        )

        needs_ppt_analysis = self._contains_any(
            text,
            [
                "ppt",
                "pptx",
                "powerpoint",
                "presentation",
                "slide",
                "slides",
                "template",
            ],
        )

        needs_research = self._contains_any(
            text,
            [
                "research",
                "latest",
                "current",
                "recent",
                "news",
                "trend",
                "trends",
                "search web",
                "web research",
                "online",
                "internet",
            ],
        )

        needs_rag = self._contains_any(
            text,
            [
                "rag",
                "knowledge base",
                "knowledgebase",
                "uploaded documents",
                "search documents",
                "document search",
                "retrieve",
                "retrieval",
            ],
        )

        needs_document_generation = self._contains_any(
            text,
            [
                "create document",
                "generate document",
                "generate docx",
                "create docx",
                "word document",
                "proposal",
                "report",
                "summary document",
            ],
        )

        needs_ppt_generation = self._contains_any(
            text,
            [
                "create presentation",
                "generate presentation",
                "generate ppt",
                "generate pptx",
                "create ppt",
                "create pptx",
                "powerpoint",
                "slides",
                "presentation",
            ],
        )

        needs_editing = self._contains_any(
            text,
            [
                "edit",
                "modify",
                "update",
                "change",
                "rewrite",
                "make it shorter",
                "make it concise",
                "add section",
                "remove section",
                "revise",
            ],
        )

        needs_validation = True

        # --------------------------------------------------------------
        # Combined document + PPT request
        #
        # Example:
        #
        # "Research latest GenAI trends and create a proposal
        #  and 12-slide presentation."
        #
        # --------------------------------------------------------------

        if (
            needs_document_generation
            and needs_ppt_generation
        ):
            needs_document_analysis = True
            needs_ppt_analysis = True

        # --------------------------------------------------------------
        # Research + generation
        # --------------------------------------------------------------

        if needs_research and (
            needs_document_generation
            or needs_ppt_generation
        ):
            needs_rag = True

        # --------------------------------------------------------------
        # If user explicitly asks for presentation, analyze template
        # --------------------------------------------------------------

        if needs_ppt_generation:
            needs_ppt_analysis = True

        # --------------------------------------------------------------
        # If user asks to generate a document, document analysis may
        # be required when source documents are involved.
        # --------------------------------------------------------------

        if needs_document_generation and self._contains_any(
            text,
            [
                "uploaded",
                "source document",
                "based on document",
                "from pdf",
                "from docx",
            ],
        ):
            needs_document_analysis = True

        # --------------------------------------------------------------
        # Build ordered agent list
        # --------------------------------------------------------------

        agents: list[str] = []
        steps: list[str] = []

        if needs_document_analysis:
            agents.append("document")
            steps.append(
                "Analyze uploaded documents and extract "
                "structure, content, style, and metadata."
            )

        if needs_ppt_analysis:
            agents.append("ppt")
            steps.append(
                "Analyze PowerPoint structure, layouts, "
                "formatting, theme, and template style."
            )

        if needs_research:
            agents.append("research")
            steps.append(
                "Perform real-time web research and collect "
                "traceable sources."
            )

        if needs_rag:
            agents.append("rag")
            steps.append(
                "Retrieve relevant information from the "
                "enterprise knowledge base."
            )

        if needs_document_generation:
            agents.append("document_generator")
            steps.append(
                "Generate an editable DOCX document."
            )

        if needs_ppt_generation:
            agents.append("ppt_generator")
            steps.append(
                "Generate an editable PPTX presentation "
                "using the analyzed template when available."
            )

        if needs_editing:
            agents.append("editing")
            steps.append(
                "Apply conversational editing instructions "
                "to the requested artifact."
            )

        if needs_validation:
            agents.append("validation")
            steps.append(
                "Validate generated artifacts for existence, "
                "format, editability, and basic integrity."
            )

        # --------------------------------------------------------------
        # Default behavior
        # --------------------------------------------------------------

        if not agents:
            steps.append(
                "Understand the user's request and prepare "
                "a response using the appropriate workflow."
            )

        # --------------------------------------------------------------
        # Determine status
        # --------------------------------------------------------------

        status = "planned"

        # --------------------------------------------------------------
        # Return structured plan
        # --------------------------------------------------------------

        return {
            "query": query,

            "status": status,

            "agents": agents,

            "steps": steps,

            "needs_document_analysis": needs_document_analysis,

            "needs_ppt_analysis": needs_ppt_analysis,

            "needs_research": needs_research,

            "needs_rag": needs_rag,

            "needs_document_generation": (
                needs_document_generation
            ),

            "needs_ppt_generation": (
                needs_ppt_generation
            ),

            "needs_editing": needs_editing,

            "needs_validation": needs_validation,

            "agent_count": len(agents),

            "execution_order": agents.copy(),
        }

    # ------------------------------------------------------------------
    # Execute
    # ------------------------------------------------------------------

    def execute(
        self,
        query: str = "",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Main execution entry point.

        This method is used by the Chat API.

        It first creates a plan and then returns a structured
        execution context.

        Keeping planning separate from execution allows the
        workflow layer to invoke the individual agents.
        """

        query = self._normalize_query(query)

        if not query:
            query = self._normalize_query(
                kwargs.get("request", "")
            )

        if not query:
            query = self._normalize_query(
                kwargs.get("user_query", "")
            )

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )


            # ------------------------------------------------------------------
    # Request Classification
    # ------------------------------------------------------------------

    def classify_request(self, query: str) -> str:
        """
        Classify the user's request into a primary workflow route.

        Returns one of:
            - document
            - ppt
            - research
            - rag
            - editing
            - generation
            - general

        This method is kept separate from plan() because the test suite
        and workflow layer use it to determine the primary route.
        """

        query = self._normalize_query(query)

        if not query:
            return "general"

        text = query.lower()

        # --------------------------------------------------------------
        # Editing requests should be detected first because an editing
        # request may also contain words such as document/PPT.
        # --------------------------------------------------------------

        if self._contains_any(
            text,
            [
                "edit",
                "modify",
                "update",
                "change",
                "rewrite",
                "revise",
                "make it shorter",
                "make it concise",
                "add section",
                "remove section",
            ],
        ):
            return "editing"

        # --------------------------------------------------------------
        # PPT / presentation requests
        # --------------------------------------------------------------

        if self._contains_any(
            text,
            [
                "ppt",
                "pptx",
                "powerpoint",
                "presentation",
                "slide",
                "slides",
            ],
        ):
            return "ppt"

        # --------------------------------------------------------------
        # Document requests
        # --------------------------------------------------------------

        if self._contains_any(
            text,
            [
                "document",
                "docx",
                "pdf",
                "word file",
                "word document",
                "uploaded document",
            ],
        ):
            return "document"

        # --------------------------------------------------------------
        # Research requests
        # --------------------------------------------------------------

        if self._contains_any(
            text,
            [
                "research",
                "latest",
                "current",
                "recent",
                "news",
                "trend",
                "trends",
                "web search",
                "web research",
                "internet",
                "online",
            ],
        ):
            return "research"

        # --------------------------------------------------------------
        # RAG / knowledge-base requests
        # --------------------------------------------------------------

        if self._contains_any(
            text,
            [
                "rag",
                "knowledge base",
                "knowledgebase",
                "retrieve",
                "retrieval",
                "search uploaded files",
                "search documents",
            ],
        ):
            return "rag"

        # --------------------------------------------------------------
        # Generation requests
        # --------------------------------------------------------------

        if self._contains_any(
            text,
            [
                "generate",
                "create",
                "build",
                "make",
                "produce",
            ],
        ):
            return "generation"

        # --------------------------------------------------------------
        # Default route
        # --------------------------------------------------------------

        return "general"

        # --------------------------------------------------------------
        # Create supervisor plan
        # --------------------------------------------------------------

        plan = self.plan(
            query=query,
            **kwargs,
        )

        # --------------------------------------------------------------
        # Add execution metadata
        # --------------------------------------------------------------

        plan["status"] = "ready"

        plan["supervisor"] = self.agent_name

        plan["execution_ready"] = True

        # --------------------------------------------------------------
        # Human-readable message
        # --------------------------------------------------------------

        if plan["agents"]:
            agent_text = ", ".join(
                plan["agents"]
            )

            plan["message"] = (
                "Request analyzed successfully. "
                f"Selected agents: {agent_text}."
            )

        else:
            plan["message"] = (
                "Request analyzed successfully."
            )

        return plan

    # ------------------------------------------------------------------
    # Convenience Method
    # ------------------------------------------------------------------

    def analyze_request(
        self,
        query: str,
    ) -> dict[str, Any]:
        """
        Alias for plan().

        Useful for code that refers to the supervisor as
        a request-analysis component.
        """

        return self.plan(
            query=query
        )

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> dict[str, Any]:
        """
        Return supervisor status.
        """

        return {
            "agent": self.agent_name,
            "status": "ready",
            "available_agents": self.available_agents,
            "agent_count": len(
                self.available_agents
            ),
        }


# ======================================================================
# MANUAL TEST
# ======================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SUPERVISOR AGENT TEST")
    print("=" * 70)

    supervisor = SupervisorAgent()

    print("\n[1] Initialization")
    print(
        "Supervisor initialized successfully."
    )

    # --------------------------------------------------------------
    # Test 1
    # --------------------------------------------------------------

    query_1 = (
        "Research the latest generative AI trends "
        "and create a presentation."
    )

    print("\n[2] Query")
    print(query_1)

    plan_1 = supervisor.plan(
        query=query_1
    )

    print("\n[3] PLAN")
    print("-" * 70)

    print(
        "Status:",
        plan_1["status"],
    )

    print(
        "Agents:",
        plan_1["agents"],
    )

    print(
        "Research:",
        plan_1["needs_research"],
    )

    print(
        "PPT Generation:",
        plan_1["needs_ppt_generation"],
    )

    print(
        "Validation:",
        plan_1["needs_validation"],
    )

    # --------------------------------------------------------------
    # Test 2 - execute()
    # --------------------------------------------------------------

    print("\n[4] EXECUTE")
    print("-" * 70)

    execution = supervisor.execute(
        query=query_1
    )

    print(
        "Execution Ready:",
        execution["execution_ready"],
    )

    print(
        "Message:",
        execution["message"],
    )

    # --------------------------------------------------------------
    # Test 3 - keyword argument compatibility
    # --------------------------------------------------------------

    print("\n[5] QUERY KEYWORD TEST")
    print("-" * 70)

    query_2 = (
        "Create a DOCX report from the uploaded PDF."
    )

    result_2 = supervisor.execute(
        query=query_2
    )

    print(
        "Query:",
        result_2["query"],
    )

    print(
        "Agents:",
        result_2["agents"],
    )

    # --------------------------------------------------------------
    # Final
    # --------------------------------------------------------------

    print("\n" + "=" * 70)
    print("SUPERVISOR TEST COMPLETE")
    print("=" * 70)