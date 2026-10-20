#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p build dist
xcodebuild -version
xcodebuild -project KeyboardProbe.xcodeproj -scheme KeyboardProbe \
    -configuration Release -sdk iphoneos -destination 'generic/platform=iOS' \
    -derivedDataPath build/DerivedData \
    CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO CODE_SIGN_IDENTITY='' \
    ARCHS=arm64 ONLY_ACTIVE_ARCH=NO build 2>&1 | tee build/xcodebuild.log

# Use a fresh staging directory so an old app cannot contaminate the IPA.
staging=$(mktemp -d)
trap 'rm -rf "$staging"' EXIT
mkdir -p "$staging/Payload"
ditto build/DerivedData/Build/Products/Release-iphoneos/KeyboardProbe.app \
    "$staging/Payload/KeyboardProbe.app"
ipa="$PWD/dist/KeyboardProbe-unsigned.ipa"
ditto -c -k --keepParent "$staging/Payload" "$ipa"
python3 scripts/validate_ipa.py "$ipa" | tee dist/validation.json
shasum -a 256 "$ipa" > dist/KeyboardProbe-unsigned.ipa.sha256
