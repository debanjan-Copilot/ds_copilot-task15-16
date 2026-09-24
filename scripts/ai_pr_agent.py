import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def required_environment(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"Missing required environment variable: {name}", file=sys.stderr)
        raise SystemExit(1)
    return value


def build_prompt(diff: str, test_outcome: str) -> str:
    return f"""Review this pull request for correctness, regressions, security concerns, and test gaps.

Test outcome: {test_outcome}

Return concise Markdown with:
1. Findings ranked by severity.
2. Specific file or code references where possible.
3. Recommended fixes.
4. A short test assessment.

Pull request diff:
{diff}
"""


def request_review(api_url: str, api_key: str, model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a careful software engineering pull-request review agent."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
    }
    request = Request(api_url, data=json.dumps(payload).encode("utf-8"), headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as error:
        print(f"AI review request failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    try:
        return result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        print("AI review response did not contain message content", file=sys.stderr)
        raise SystemExit(1) from error


def post_comment(repository: str, pr_number: str, token: str, body: str) -> None:
    payload = json.dumps({"body": f"## AI PR Agent Review\n\n{body}"}).encode("utf-8")
    request = Request(f"https://api.github.com/repos/{repository}/issues/{pr_number}/comments", data=payload, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "Content-Type": "application/json", "X-GitHub-Api-Version": "2022-11-28"}, method="POST")
    try:
        with urlopen(request, timeout=30):
            return
    except (HTTPError, URLError, TimeoutError) as error:
        print(f"GitHub comment request failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error


def main() -> None:
    api_url = required_environment("AI_API_URL")
    api_key = required_environment("AI_API_KEY")
    repository = required_environment("GITHUB_REPOSITORY")
    github_token = required_environment("GH_TOKEN")
    pr_number = required_environment("PR_NUMBER")
    model = os.getenv("AI_MODEL", "gpt-4o-mini")
    diff = os.getenv("PR_DIFF", "")
    test_outcome = os.getenv("TEST_OUTCOME", "unknown")
    if not diff.strip():
        print("Pull request diff is empty; no review was posted.", file=sys.stderr)
        raise SystemExit(1)
    review = request_review(api_url, api_key, model, build_prompt(diff, test_outcome))
    post_comment(repository, pr_number, github_token, review)


if __name__ == "__main__":
    main()
