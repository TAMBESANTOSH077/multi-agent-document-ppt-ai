"""
Manual test for the Supervisor Agent.
"""

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.agents.supervisor import SupervisorAgent


def test_route(query: str):
    print("\n" + "=" * 70)
    print("QUERY")
    print("=" * 70)
    print(query)

    supervisor = SupervisorAgent()

    route = supervisor.classify_request(query)

    print("\nSELECTED ROUTE:")
    print(route)


def main():
    print("=" * 70)
    print("SUPERVISOR AGENT TEST")
    print("=" * 70)

    test_route(
        "What is PHP according to the uploaded document?"
    )

    test_route(
        "What are the latest generative AI trends in 2026?"
    )

    test_route(
        "Using my uploaded documents and the latest AI trends, "
        "give me an updated analysis."
    )


if __name__ == "__main__":
    main()