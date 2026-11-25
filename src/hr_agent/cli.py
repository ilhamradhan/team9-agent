import argparse

from hr_agent.workflow import build_graph


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask the sample HR policy documents.")
    parser.add_argument("question", help="Question about the supplied HR documents")
    args = parser.parse_args()
    result = build_graph().invoke({"question": args.question})
    print(result["answer"])
