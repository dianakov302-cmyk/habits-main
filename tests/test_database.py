import unittest

from backend.repositories.database import normalize_mongodb_uri


class MongoUriTests(unittest.TestCase):
    def test_normalize_mongodb_uri_merges_existing_query_params(self):
        uri = (
            "mongodb+srv://example.mongodb.net/goalsplatform"
            "?retryWrites=true&w=majority"
        )

        normalized = normalize_mongodb_uri(uri)

        self.assertEqual(
            normalized,
            (
                "mongodb+srv://example.mongodb.net/goalsplatform"
                "?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
            ),
        )

    def test_normalize_mongodb_uri_keeps_existing_tls_option(self):
        uri = (
            "mongodb+srv://example.mongodb.net/goalsplatform"
            "?retryWrites=true&w=majority&tlsAllowInvalidCertificates=false"
        )

        normalized = normalize_mongodb_uri(uri)

        self.assertEqual(
            normalized,
            (
                "mongodb+srv://example.mongodb.net/goalsplatform"
                "?retryWrites=true&w=majority&tlsAllowInvalidCertificates=false"
            ),
        )


if __name__ == "__main__":
    unittest.main()
