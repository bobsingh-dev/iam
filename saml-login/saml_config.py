from pathlib import Path

from onelogin.saml2.idp_metadata_parser import OneLogin_Saml2_IdPMetadataParser

BASE_URL = "http://localhost:8000"

metadata = Path(__file__).with_name("keycloak-metadata.xml").read_text()
keycloak = OneLogin_Saml2_IdPMetadataParser.parse(metadata)

SAML_SETTINGS = {
    "strict": True,
    "debug": False,
    "sp": {
        "entityId": f"{BASE_URL}/saml/metadata",
        "assertionConsumerService": {
            "url": f"{BASE_URL}/saml/acs",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST",
        },
        "NameIDFormat": (
            "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified"
        ),
    },
    "idp": keycloak["idp"],
    "security": {
        "authnRequestsSigned": False,
        "wantMessagesSigned": True,
        "wantAssertionsSigned": True,
        "wantAttributeStatement": False,
        "rejectDeprecatedAlgorithm": True,
    },
}
