import unittest

from backend.auth import create_access_token, verify_token


class TestCreateAccessToken(unittest.TestCase):
    def test_returns_string(self):
        token = create_access_token("user@test.com")
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 20)

    def test_different_emails_produce_different_tokens(self):
        t1 = create_access_token("a@test.com")
        t2 = create_access_token("b@test.com")
        self.assertNotEqual(t1, t2)

    def test_same_email_produces_string_token(self):
        token = create_access_token("same@test.com")
        self.assertIsInstance(token, str)

    def test_token_contains_three_parts(self):
        # JWT tokens are three base64url segments separated by dots
        token = create_access_token("user@test.com")
        parts = token.split(".")
        self.assertEqual(len(parts), 3)


class TestVerifyToken(unittest.TestCase):
    def test_valid_token_returns_email(self):
        email = "user@test.com"
        token = create_access_token(email)
        result = verify_token(token)
        self.assertEqual(result, email)

    def test_invalid_token_returns_none(self):
        result = verify_token("not-a-valid-token")
        self.assertIsNone(result)

    def test_empty_string_returns_none(self):
        result = verify_token("")
        self.assertIsNone(result)

    def test_tampered_token_returns_none(self):
        token = create_access_token("user@test.com")
        tampered = token[:-5] + "XXXXX"
        result = verify_token(tampered)
        self.assertIsNone(result)

    def test_roundtrip_preserves_email(self):
        email = "roundtrip@example.com"
        token = create_access_token(email)
        self.assertEqual(verify_token(token), email)

    def test_verify_wrong_signature_returns_none(self):
        # Build a token with different secret by mangling the signature segment
        token = create_access_token("user@test.com")
        header_payload, _, _ = token.rpartition(".")
        bad_token = header_payload + ".invalidsignature"
        self.assertIsNone(verify_token(bad_token))

    def test_verify_random_string_returns_none(self):
        self.assertIsNone(verify_token("randomgarbage12345"))


if __name__ == "__main__":
    unittest.main()
