import json
import unittest
from unittest.mock import MagicMock, patch

from aws_doc_research_agent.remote_client import RemoteAgentError, invoke_remote_agent


class RemoteClientTests(unittest.TestCase):
    @patch("aws_doc_research_agent.remote_client.urllib.request.urlopen")
    def test_invoke_remote_agent_returns_result(self, urlopen):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({
            "ok": True,
            "result": {"query": "ALB"},
        }).encode("utf-8")
        urlopen.return_value = response

        payload = invoke_remote_agent(
            "search_aws_docs",
            {"query": "ALB"},
            endpoint_url="https://example.com/invoke",
        )

        self.assertEqual(payload["query"], "ALB")

    def test_invoke_remote_agent_requires_url(self):
        with self.assertRaises(RemoteAgentError):
            invoke_remote_agent("search_aws_docs", {"query": "SG"}, endpoint_url="")


if __name__ == "__main__":
    unittest.main()
