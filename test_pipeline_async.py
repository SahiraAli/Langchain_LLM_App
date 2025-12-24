# test_pipeline_async.py
import re
import pytest
import asyncio

from langchain_core.prompts import PromptTemplate

# same canned output (simulate model)
CANNED_RAW = """<think>
internal reasoning...
</think>
1. Async Pipe Dreams
2. Async Great Data Heist
3. Async Sql vs NoSql
"""

class FakeAsyncPipeline:
    """Fake pipeline that supports async ainvoke()"""
    def __init__(self, raw=CANNED_RAW):
        self.raw = raw

    async def ainvoke(self, inputs):
        # simulate some async delay just for realism
        await asyncio.sleep(0)
        return self.raw

def fake_prompt_or(self, other):
    class Partial:
        def __or__(self_inner, other2):
            return FakeAsyncPipeline()
    return Partial()

@pytest.mark.asyncio
async def test_async_pipeline_ainvoke(monkeypatch: pytest.MonkeyPatch):
    # monkeypatch PromptTemplate.__or__ to return a Partial that yields FakeAsyncPipeline on second '|'
    monkeypatch.setattr(PromptTemplate, "__or__", fake_prompt_or, raising=False)

    # Build the pipeline inside the test (like your code does)
    prompt_template = PromptTemplate(
        input_variables=["topic", "adjective"],
        template="Suggest three {adjective} blog post titles about {topic}."
    )
    # In real code you'd do: chain = prompt | llm | StrOutputParser()
    # But our monkeypatch makes that return FakeAsyncPipeline
    chain = prompt_template | object() | object()

    # Call async method
    raw = await chain.ainvoke({
    "topic": "Data Engineering",
    "adjective": "funny"
})

    # clean out <think> if any (mimic what your code does)
    cleaned = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL | re.IGNORECASE).strip()

    assert "<think>" not in cleaned.lower()
    lines = [ln.strip() for ln in cleaned.splitlines() if ln.strip()]
    numbered = [ln for ln in lines if re.match(r'^\d+\.', ln)]
    assert len(numbered) == 3
