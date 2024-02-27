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
    name = "jsonl-data"

    def __call__(
        self,
        data: bytes,
        *,
        content_type: str | None = None,
        flow: http.HTTPFlow | None = None,
        http_message: http.Message | None = None,
        **unknown_metadata,
    ) -> contentviews.TViewResult:

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

        content = ""
        for json_line in json_lines:
            data = json.loads(json_line)
            content += "data: " + json.dumps(data, indent=2) + "\n"

        return "JSONL", contentviews.format_text(content)


    def render_priority(
        self,
        data: bytes,
        *,
        content_type: str | None = None,
        flow: http.HTTPFlow | None = None,
        http_message: http.Message | None = None,
        **unknown_metadata,
    ) -> float:
        return 0


view = ViewCopilotCodex()


def load(loader: Loader):
    contentviews.add(view)


def done():
    contentviews.remove(view)
