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

class ViewChatCopletions(contentviews.View):
    name = "chat-completions"

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
            # data: {"choices":[],"created":0,"id":"","prompt_filter_results":[{"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"prompt_index":0}]}
            # data: {"choices":[{"index":0,"content_filter_offsets":{"check_offset":1187,"start_offset":1187,"end_offset":1222},"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"delta":{"content":null,"role":"assistant"}}],"created":1709020207,"id":"chatcmpl-8wmVzZpVkD5b889LLLwl837vkhTcV"}
            # data: {"choices":[{"index":0,"content_filter_offsets":{"check_offset":1187,"start_offset":1187,"end_offset":1222},"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"delta":{"content":"```","role":null}}],"created":1709020207,"id":"chatcmpl-8wmVzZpVkD5b889LLLwl837vkhTcV"}
            # data: {"choices":[{"index":0,"content_filter_offsets":{"check_offset":1187,"start_offset":1187,"end_offset":1222},"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"delta":{"content":"javascript","role":null}}],"created":1709020207,"id":"chatcmpl-8wmVzZpVkD5b889LLLwl837vkhTcV"}
            # data: {"choices":[{"index":0,"content_filter_offsets":{"check_offset":1187,"start_offset":1187,"end_offset":1222},"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"delta":{"content":"\n","role":null}}],"created":1709020207,"id":"chatcmpl-8wmVzZpVkD5b889LLLwl837vkhTcV"}
            # data: {"choices":[{"index":0,"content_filter_offsets":{"check_offset":1187,"start_offset":1187,"end_offset":1222},"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"delta":{"content":"this","role":null}}],"created":1709020207,"id":"chatcmpl-8wmVzZpVkD5b889LLLwl837vkhTcV"}
            # data: {"choices":[{"index":0,"content_filter_offsets":{"check_offset":1187,"start_offset":1187,"end_offset":1222},"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"delta":{"content":".name","role":null}}],"created":1709020207,"id":"chatcmpl-8wmVzZpVkD5b889LLLwl837vkhTcV"}
            # data: {"choices":[{"index":0,"content_filter_offsets":{"check_offset":1187,"start_offset":1187,"end_offset":1222},"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"delta":{"content":" =","role":null}}],"created":1709020207,"id":"chatcmpl-8wmVzZpVkD5b889LLLwl837vkhTcV"}
            # data: {"choices":[{"index":0,"content_filter_offsets":{"check_offset":1187,"start_offset":1187,"end_offset":1222},"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"delta":{"content":" name","role":null}}],"created":1709020207,"id":"chatcmpl-8wmVzZpVkD5b889LLLwl837vkhTcV"}
            # data: {"choices":[{"index":0,"content_filter_offsets":{"check_offset":1187,"start_offset":1187,"end_offset":1222},"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"delta":{"content":";\n","role":null}}],"created":1709020207,"id":"chatcmpl-8wmVzZpVkD5b889LLLwl837vkhTcV"}
            # data: {"choices":[{"index":0,"content_filter_offsets":{"check_offset":1187,"start_offset":1187,"end_offset":1222},"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"delta":{"content":"```","role":null}}],"created":1709020207,"id":"chatcmpl-8wmVzZpVkD5b889LLLwl837vkhTcV"}
            # data: {"choices":[{"finish_reason":"stop","index":0,"content_filter_offsets":{"check_offset":1187,"start_offset":1187,"end_offset":1222},"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"delta":{"content":null,"role":null}}],"created":1709020207,"id":"chatcmpl-8wmVzZpVkD5b889LLLwl837vkhTcV"}
            # data: [DONE]
            # """

            jsonl_data = data.decode("utf-8")

            # Split the data into lines and filter out any non-JSON lines.
            lines = jsonl_data.strip().split("\n")
            json_lines = [line[6:] for line in lines if line.startswith("data: ") and line != "data: [DONE]"]

            # Parse the JSON lines and sort texts by index within each choice.
            content = ''
            for json_line in json_lines:
                json_data = json.loads(json_line)
                # print("HERE JSON DATA")
                # pprint.pprint(json_data)
                # print("...HERE JSON DATA")
                choices = json_data["choices"]
                if (len(choices) > 0):
                    choice = choices[0]
                    delta = choice["delta"]
                    if delta["content"] is not None:
                        content += delta["content"]

            return "Prompt response", contentviews.format_text(content)

        else:

            try:
                json_data = json.loads(data)
            except Exception as e:
                return f"Error: {str(e)}"

            # Initialize an empty string for the formatted message
            formatted_message = ""

            # Loop through the messages in the JSON data
            for message in json_data['messages']:
                # Append the role and content to the formatted message
                formatted_message += f"# {message['role'].upper()}\n \n{message['content']}\n \n"

            return "Prompt request", contentviews.format_text(formatted_message)

    def render_priority(
        self,
        data: bytes,
        *,
        content_type: str | None = None,
        flow: http.HTTPFlow | None = None,
        http_message: http.Message | None = None,
        **unknown_metadata,
    ) -> float:

        if flow.request.pretty_url == "https://api.githubcopilot.com/chat/completions":
            return 1
        else:
            return 0


view = ViewChatCopletions()


def load(loader: Loader):
    contentviews.add(view)


def done():
    contentviews.remove(view)
