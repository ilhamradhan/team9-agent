from hr_agent.workflow import build_graph


def test_answers_from_retrieved_document_with_source():
    result = build_graph().invoke(
        {"question": "How many paid days off do I get for my wedding?"}
    )

    assert "one paid working day" in result["answer"]
    assert result["sources"] == ["leave_policy.md#Wedding leave"]


def test_falls_back_when_documents_do_not_cover_question():
    result = build_graph().invoke(
        {"question": "What is the policy for payroll corrections?"}
    )

    assert result["answer"] == (
        "I couldn't find this information in the provided HR documents. "
        "Please ask HR."
    )
    assert result["sources"] == []
