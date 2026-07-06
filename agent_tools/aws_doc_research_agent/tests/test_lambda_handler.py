import json
import unittest
from unittest.mock import patch

from aws_doc_research_agent.lambda_handler import handler


class LambdaHandlerTests(unittest.TestCase):
    @patch("aws_doc_research_agent.lambda_handler.make_citation_pack")
    def test_direct_invoke_returns_tool_payload(self, make_pack):
        make_pack.return_value = {"topic": "S3"}

        payload = handler({"tool": "make_citation_pack", "arguments": {"topic": "S3"}})

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["result"]["topic"], "S3")

    @patch("aws_doc_research_agent.lambda_handler.search_aws_docs")
    def test_http_api_event_parses_body(self, search_docs):
        search_docs.return_value = {"query": "EKS"}
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({"tool": "search_aws_docs", "arguments": {"query": "EKS"}}),
        }

        response = handler(event)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertTrue(body["ok"])
        self.assertEqual(body["result"]["query"], "EKS")

    def test_http_api_event_rejects_invalid_json(self):
        response = handler({
            "requestContext": {"http": {"method": "POST"}},
            "body": "{not-json",
        })

        self.assertEqual(response["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()
