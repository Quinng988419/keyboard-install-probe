"""Checks for the IPA gate, using tiny synthetic archives, not installable apps."""

import importlib.util
import plistlib
import struct
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_ipa.py"


class ValidateIPATests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(VALIDATOR.exists(), "IPA validation gate has not been implemented")
        spec = importlib.util.spec_from_file_location("validate_ipa", VALIDATOR)
        self.validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.validator)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.ipa = Path(self.temp.name) / "probe.ipa"
        self.host = "Payload/KeyboardProbe.app/"
        self.extension = self.host + "PlugIns/ProbeKeyboard.appex/"
        self.host_info = {
            "CFBundleIdentifier": "com.example.KeyboardProbe",
            "CFBundleExecutable": "KeyboardProbe",
            "CFBundlePackageType": "APPL",
        }
        self.extension_info = {
            "CFBundleIdentifier": "com.example.KeyboardProbe.Keyboard",
            "CFBundleExecutable": "ProbeKeyboard",
            "CFBundlePackageType": "XPC!",
            "NSExtension": {
                "NSExtensionPointIdentifier": "com.apple.keyboard-service",
                "NSExtensionPrincipalClass": "ProbeKeyboard.KeyboardViewController",
                "NSExtensionAttributes": {"RequestsOpenAccess": False},
            },
        }

    def write_ipa(self, *, include_extension=True, platform=2, include_binary=True):
        # MH_EXECUTE / ARM64, with one LC_BUILD_VERSION command.
        binary = struct.pack("<8I", 0xFEEDFACF, 0x0100000C, 0, 2, 1, 24, 0, 0)
        binary += struct.pack("<6I", 0x32, 24, platform, 0x100000, 0x1A0000, 0)
        with zipfile.ZipFile(self.ipa, "w") as archive:
            archive.writestr(self.host + "Info.plist", plistlib.dumps(self.host_info))
            archive.writestr(self.host + "KeyboardProbe", binary)
            if include_extension:
                archive.writestr(self.extension + "Info.plist", plistlib.dumps(self.extension_info))
                if include_binary:
                    archive.writestr(self.extension + "ProbeKeyboard", binary)

    def test_accepts_host_with_embedded_device_keyboard(self):
        self.write_ipa()
        result = self.validator.validate_ipa(self.ipa)
        self.assertEqual(result["app_id"], "com.example.KeyboardProbe")
        self.assertEqual(result["keyboard_id"], "com.example.KeyboardProbe.Keyboard")

    def test_rejects_missing_extension(self):
        self.write_ipa(include_extension=False)
        with self.assertRaisesRegex(ValueError, "keyboard extension"):
            self.validator.validate_ipa(self.ipa)

    def test_rejects_missing_keyboard_executable(self):
        self.write_ipa(include_binary=False)
        with self.assertRaisesRegex(ValueError, "executable"):
            self.validator.validate_ipa(self.ipa)

    def test_rejects_arm64_simulator_build(self):
        self.write_ipa(platform=7)
        with self.assertRaisesRegex(ValueError, "iOS device"):
            self.validator.validate_ipa(self.ipa)

    def test_rejects_wrong_extension_type(self):
        self.extension_info["NSExtension"]["NSExtensionPointIdentifier"] = "com.apple.widgetkit-extension"
        self.write_ipa()
        with self.assertRaisesRegex(ValueError, "keyboard-service"):
            self.validator.validate_ipa(self.ipa)

    def test_rejects_unrelated_extension_identifier(self):
        self.extension_info["CFBundleIdentifier"] = "com.other.Keyboard"
        self.write_ipa()
        with self.assertRaisesRegex(ValueError, "identifier"):
            self.validator.validate_ipa(self.ipa)

    def test_rejects_unexpected_full_access_requirement(self):
        self.extension_info["NSExtension"]["NSExtensionAttributes"]["RequestsOpenAccess"] = True
        self.write_ipa()
        with self.assertRaisesRegex(ValueError, "Full Access"):
            self.validator.validate_ipa(self.ipa)


if __name__ == "__main__":
    unittest.main()
