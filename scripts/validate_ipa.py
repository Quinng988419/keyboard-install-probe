"""Reject IPAs that cannot serve as this offline, device-only keyboard probe."""

import json
import plistlib
import re
import struct
import sys
import zipfile
from pathlib import PurePosixPath


def validate_device_executable(data, name):
    if len(data) < 32:
        raise ValueError(f"Missing or truncated executable: {name}")
    magic, cpu, _, file_type, commands, command_bytes, _, _ = struct.unpack_from("<8I", data)
    if magic != 0xFEEDFACF or cpu != 0x0100000C or file_type != 2:
        raise ValueError(f"Expected an arm64 iOS device executable: {name}")
    if 32 + command_bytes > len(data):
        raise ValueError(f"Truncated executable load commands: {name}")
    offset = 32
    for _ in range(commands):
        if offset + 8 > 32 + command_bytes:
            raise ValueError(f"Invalid executable load commands: {name}")
        command, size = struct.unpack_from("<2I", data, offset)
        if size < 8 or offset + size > 32 + command_bytes:
            raise ValueError(f"Invalid executable load command size: {name}")
        if command == 0x32 and size >= 24:
            platform = struct.unpack_from("<I", data, offset + 8)[0]
            if platform != 2:
                raise ValueError(f"Expected iOS device platform, got {platform}: {name}")
            return
        offset += size
    raise ValueError(f"No iOS device build version in executable: {name}")


def validate_ipa(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("IPA contains duplicate entries")
        apps = [name for name in names if re.fullmatch(r"Payload/[^/]+\.app/Info\.plist", name)]
        if len(apps) != 1:
            raise ValueError("Expected exactly one host app in Payload")
        app_root = str(PurePosixPath(apps[0]).parent) + "/"
        extensions = [name for name in names if re.fullmatch(
            re.escape(app_root) + r"PlugIns/[^/]+\.appex/Info\.plist", name
        )]
        if len(extensions) != 1:
            raise ValueError("Expected exactly one embedded keyboard extension")

        app_info = plistlib.loads(archive.read(apps[0]))
        keyboard_info = plistlib.loads(archive.read(extensions[0]))
        if app_info.get("CFBundlePackageType") != "APPL":
            raise ValueError("Host package type must be APPL")
        if keyboard_info.get("CFBundlePackageType") != "XPC!":
            raise ValueError("Keyboard package type must be XPC!")
        app_id = app_info.get("CFBundleIdentifier", "")
        keyboard_id = keyboard_info.get("CFBundleIdentifier", "")
        if not app_id or not keyboard_id.startswith(app_id + "."):
            raise ValueError("Keyboard identifier must be prefixed by the host identifier")
        extension_info = keyboard_info.get("NSExtension", {})
        if extension_info.get("NSExtensionPointIdentifier") != "com.apple.keyboard-service":
            raise ValueError("Extension must use com.apple.keyboard-service")
        if not extension_info.get("NSExtensionPrincipalClass", "").endswith(".KeyboardViewController"):
            raise ValueError("Missing keyboard principal class")
        if extension_info.get("NSExtensionAttributes", {}).get("RequestsOpenAccess") is not False:
            raise ValueError("Offline probe must not request Full Access")

        for info_path, info in [(apps[0], app_info), (extensions[0], keyboard_info)]:
            executable = info.get("CFBundleExecutable", "")
            if not executable or "/" in executable or executable in (".", ".."):
                raise ValueError(f"Invalid executable name in {info_path}")
            executable_path = str(PurePosixPath(info_path).parent / executable)
            if executable_path not in names:
                raise ValueError(f"Missing executable: {executable_path}")
            validate_device_executable(archive.read(executable_path), executable_path)

        return {"app_id": app_id, "keyboard_id": keyboard_id, "platform": "iOS device arm64"}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 scripts/validate_ipa.py path/to/KeyboardProbe-unsigned.ipa")
    try:
        print(json.dumps(validate_ipa(sys.argv[1]), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError, zipfile.BadZipFile, plistlib.InvalidFileException) as error:
        sys.exit(f"IPA validation failed: {error}")
