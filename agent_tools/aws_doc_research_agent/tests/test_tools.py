from unittest import TestCase
from unittest.mock import patch

from aws_doc_research_agent.tools import make_citation_pack, read_aws_doc, search_aws_docs


class ToolContractTests(TestCase):
    @patch("aws_doc_research_agent.tools.AwsDocsClient")
    def test_search_aws_docs_returns_client_payload(self, client_cls):
        client_cls.return_value.search.return_value = {"query": "s3", "results": []}

        payload = search_aws_docs("s3", limit=3)

        self.assertEqual(payload["query"], "s3")
        client_cls.return_value.search.assert_called_once()

    @patch("aws_doc_research_agent.tools.AwsDocsClient")
    def test_read_aws_doc_returns_client_payload(self, client_cls):
        client_cls.return_value.read.return_value = {"url": "https://docs.aws.amazon.com/x.html"}

        payload = read_aws_doc("https://docs.aws.amazon.com/x.html")

        self.assertEqual(payload["url"], "https://docs.aws.amazon.com/x.html")
        client_cls.return_value.read.assert_called_once()

    @patch("aws_doc_research_agent.tools.search_aws_docs")
    def test_make_citation_pack_shapes_sources(self, search):
        search.return_value = {
            "query_id": "q-1",
            "results": [
                {
                    "rank": 1,
                    "title": "Configuring IAM for Amazon EKS",
                    "url": "https://docs.aws.amazon.com/eks/latest/userguide/example.html",
                    "context": "Security and permissions guidance",
                    "recommended_sections": ["IAM roles"],
                }
            ],
        }

        pack = make_citation_pack("EKS IAM")

        self.assertEqual(pack["topic"], "EKS IAM")
        self.assertEqual(pack["sources"][0]["confidence"], 1.0)
        self.assertIn("security note", pack["sources"][0]["usable_for"])

