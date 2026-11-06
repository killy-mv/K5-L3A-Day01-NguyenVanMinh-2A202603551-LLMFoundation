"""AI-assisted optional lab implementation; API behavior follows the supplied template.
Live API experiments are not measured without a configured key.
"""
import time
from typing import Any, Callable

OPENAI_MODEL = "gpt-6.1-terra"
OPENAI_MINI_MODEL = "gpt-6-luna"
COST_PER_1K_OUTPUT_TOKENS = {OPENAI_MODEL: 0.005, OPENAI_MINI_MODEL: 0.0005}

def call_openai(prompt: str, model: str = OPENAI_MODEL,
                temperature: float = 0.7, top_p: float = 0.9,
                max_tokens: int = 256) -> tuple[str, float]:
    from openai import OpenAI
    client = OpenAI()
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}],
        reasoning_effort="none", temperature=temperature, top_p=top_p,
        max_completion_tokens=max_tokens,
    )
    return response.choices[0].message.content or "", float(time.perf_counter() - start)

def call_openai_mini(prompt: str, temperature: float = 0.7,
                     top_p: float = 0.9, max_tokens: int = 256) -> tuple[str, float]:
    return call_openai(prompt, model=OPENAI_MINI_MODEL, temperature=temperature,
                       top_p=top_p, max_tokens=max_tokens)

def compare_models(prompt: str) -> dict:
    big_text, big_latency = call_openai(prompt)
    mini_text, mini_latency = call_openai_mini(prompt)
    return {
        "gpt4o_response": big_text, "mini_response": mini_text,
        "gpt4o_latency": big_latency, "mini_latency": mini_latency,
        # Output-only approximation required by the exercise, not a full API bill.
        "gpt4o_cost_estimate": len(big_text.split()) / 0.75 / 1000 * COST_PER_1K_OUTPUT_TOKENS[OPENAI_MODEL],
    }

def streaming_chatbot() -> None:
    from openai import OpenAI
    client = OpenAI()
    history = []
    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if prompt.lower() in {"quit", "exit"}:
            break
        if not prompt:
            continue
        messages = history + [{"role": "user", "content": prompt}]
        stream = client.chat.completions.create(
            model=OPENAI_MINI_MODEL, messages=messages, stream=True,
            reasoning_effort="none", max_completion_tokens=256,
        )
        pieces = []
        print("Assistant: ", end="", flush=True)
        try:
            for chunk in stream:
                if not chunk.choices:
                    continue
                text = chunk.choices[0].delta.content or ""
                pieces.append(text)
                print(text, end="", flush=True)
        finally:
            close = getattr(stream, "close", None)
            if close:
                close()
        print()
        history = (messages + [{"role": "assistant", "content": "".join(pieces)}])[-6:]

def retry_with_backoff(fn: Callable, max_retries: int = 3,
                       base_delay: float = 0.1) -> Any:
    """Exercise contract retries any Exception; production should filter transient errors."""
    if max_retries < 0 or base_delay < 0:
        raise ValueError("Retry count and delay must be nonnegative")
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception:
            if attempt == max_retries:
                raise
            time.sleep(base_delay * 2 ** attempt)

def batch_compare(prompts: list[str]) -> list[dict]:
    return [{"prompt": prompt, **compare_models(prompt)} for prompt in prompts]

def format_comparison_table(results: list[dict]) -> str:
    def shorten(value):
        text = str(value).replace("\n", " ").replace("|", "/")
        return text if len(text) <= 40 else text[:37] + "..."
    rows = [
        "| Prompt | GPT-4o Response | Mini Response | GPT-4o Latency | Mini Latency |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for row in results:
        rows.append(
            f"| {shorten(row['prompt'])} | {shorten(row['gpt4o_response'])} | "
            f"{shorten(row['mini_response'])} | {row['gpt4o_latency']:.4f}s | {row['mini_latency']:.4f}s |"
        )
    return "\n".join(rows)

if __name__ == "__main__":
    rows = batch_compare(["Explain temperature and top_p in one sentence."])
    print(format_comparison_table(rows))
    streaming_chatbot()
