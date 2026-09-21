import React from "react";

const agents = [
    {
        name: "Supervisor Agent",
        description: "Orchestrates workflow",
    },
    {
        name: "Document Agent",
        description: "Understands documents",
    },
    {
        name: "RAG Agent",
        description: "Retrieves relevant context",
    },
    {
        name: "Research Agent",
        description: "Performs web research",
    },
    {
        name: "Document Generator",
        description: "Creates editable documents",
    },
    {
        name: "PPT Generator",
        description: "Creates PowerPoint files",
    },
    {
        name: "Validation Agent",
        description: "Validates generated output",
    },
];

export default function AgentStatus() {

    return (
        <section className="workflow-card">

            <h2>
                Multi-Agent Workflow
            </h2>

            <div className="workflow-subtitle">
                Specialized agents coordinate to
                understand, research, generate and
                validate your content.
            </div>

            <div className="agent-grid">

                {agents.map(
                    (agent) => (

                        <div
                            className="agent-card"
                            key={agent.name}
                        >

                            <h3>
                                <span className="status" />

                                {agent.name}
                            </h3>

                            <p>
                                {agent.description}
                            </p>

                        </div>

                    )
                )}

            </div>

        </section>
    );
}