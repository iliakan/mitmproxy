"""
Add a custom message body pretty-printer for use inside mitmproxy.

This example shows how one can add a custom contentview to mitmproxy,
which is used to pretty-print HTTP bodies for example.
The content view API is explained in the mitmproxy.contentviews module.
"""
from mitmproxy import contentviews
from mitmproxy import flow
from mitmproxy import http
from mitmproxy.addonmanager import Loader
import json
import pprint

class ViewCopilotCodex(contentviews.View):
    name = "copilot-codex"

    def __call__(
        self,
        data: bytes,
        *,
        content_type: str | None = None,
        flow: http.HTTPFlow | None = None,
        http_message: http.Message | None = None,
        **unknown_metadata,
    ) -> contentviews.TViewResult:

        # pprint.pprint(locals())

        if isinstance(http_message, http.Response):
            # Sample JSONL data as a multi-line string for demonstration.
            # In practice, this could be read from a file or another source.
            # jsonl_data = """
            # data: {"id":"cmpl-8wf2i0p2Nb0WdsTaLjoMcePxWpCuO","created":1708991484,"choices":[{"text":"","index":0,"finish_reason":null,"logprobs":null}]}
            # data: {"id":"cmpl-8wf2i0p2Nb0WdsTaLjoMcePxWpCuO","created":1708991484,"choices":[{"text":"","index":2,"finish_reason":null,"logprobs":null}]}
            # ...
            # data: [DONE]
            # """

            jsonl_data = data.decode("utf-8")

            # Split the data into lines and filter out any non-JSON lines.
            lines = jsonl_data.strip().split("\n")
            json_lines = [line[6:] for line in lines if line.startswith("data: ") and line != "data: [DONE]"]

            # Parse the JSON lines and sort texts by index within each choice.
            texts_by_index = {}
            for json_line in json_lines:
                data = json.loads(json_line)
                for choice in data["choices"]:
                    index = choice["index"]
                    text = choice["text"]
                    if index in texts_by_index:
                        texts_by_index[index] += text
                    else:
                        texts_by_index[index] = text

            # Since the texts are grouped and concatenated by index, we sort by index and join them.
            sorted_texts = [texts_by_index[index] for index in sorted(texts_by_index)]
            joined_text = "".join(sorted_texts)

            return "Prompt response", contentviews.format_text(joined_text)

        else:

            def parse_json_data(data: bytes) -> str:
                try:
                    json_data = json.loads(data)
                    prompt = json_data.get("prompt")
                    return prompt
                except Exception as e:
                    return f"Error: {str(e)}"

            prompt = parse_json_data(data)

            return "Prompt request", contentviews.format_text(prompt)

    def render_priority(
        self,
        data: bytes,
        *,
        content_type: str | None = None,
        flow: http.HTTPFlow | None = None,
        http_message: http.Message | None = None,
        **unknown_metadata,
    ) -> float:

        if flow.request.pretty_url == "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions":
            return 1
        else:
            return 0


view = ViewCopilotCodex()


def load(loader: Loader):
    contentviews.add(view)


def done():
    contentviews.remove(view)
