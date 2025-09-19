
#!/usr/bin/env bash
set -euo pipefail

# Build a PyInstaller bundle that includes necessary data files
# Usage: ./build_pyinstaller.sh
# Requires: pyinstaller installed in the active environment

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

PYINSTALLER=${PYINSTALLER:-}
# Prefer pyinstaller in common venv locations to avoid requiring the caller to
# activate a venv. Check ./venv, ./.venv, and ../Data-visualization/.venv.
if [ -z "$PYINSTALLER" ]; then
  CANDIDATES=("${ROOT_DIR}/.venv/bin/pyinstaller" "${ROOT_DIR}/venv/bin/pyinstaller" "${ROOT_DIR}/../Data-visualization/.venv/bin/pyinstaller" "$(which pyinstaller 2>/dev/null || true)")
  for c in "${CANDIDATES[@]}"; do
    if [ -n "$c" ] && [ -x "$c" ]; then
      PYINSTALLER="$c"
      break
    fi
  done
fi
if [ -z "$PYINSTALLER" ]; then
  echo "Error: pyinstaller not found. Install it in a virtualenv or ensure it's on PATH.\nTry: pip install pyinstaller" >&2
  exit 2
fi
APP=Main
SPEC_OPTS=(--onefile --noconfirm --windowed)

echo "Root: ${ROOT_DIR}"


# Collect data folders and files to include in the bundle. We read them
# from package_files.txt if present so packaging stays stable while you
# edit source files (no need to modify this script when Main.py changes).
ADD_DATA=()

PACKAGE_MANIFEST="${ROOT_DIR}/package_files.txt"
if [ -f "$PACKAGE_MANIFEST" ]; then
	echo "Reading package manifest: $PACKAGE_MANIFEST"
	while IFS= read -r line || [ -n "$line" ]; do
		# strip leading/trailing whitespace
		line="$(echo "$line" | sed -e 's/^\s*//' -e 's/\s*$//')"
		# skip empty or comment lines
		case "$line" in
			""|\#*) continue ;;
		esac
		# expect format src:dest
		src="$(echo "$line" | cut -d':' -f1)"
		dest="$(echo "$line" | cut -d':' -f2-)"
		# expand relative to ROOT_DIR
		full_src="${ROOT_DIR}/$src"
		if [ -e "$full_src" ]; then
			ADD_DATA+=("${full_src}:${dest}")
			echo "Including: $full_src -> $dest"
		else
			echo "Warning: manifest entry not found: $full_src"
		fi
	done < "$PACKAGE_MANIFEST"
else
	echo "No package_files.txt manifest found; no extra data will be included"
fi

PYINSTALLER_CMD=("${PYINSTALLER}" "${APP}.py" "${SPEC_OPTS[@]}")
for d in "${ADD_DATA[@]}"; do
	PYINSTALLER_CMD+=(--add-data "$d")
done

echo "Running: ${PYINSTALLER_CMD[*]}"
"${PYINSTALLER_CMD[@]}"

echo "Done. Output in dist/"

# Create packages/ and zip the produced artifact for easy download
PKG_DIR="${ROOT_DIR}/packages"
mkdir -p "$PKG_DIR"
if [ -d "${ROOT_DIR}/dist" ]; then
	# pick the first produced item (file or folder)
	ARTIFACT_NAME=$(ls -1 "${ROOT_DIR}/dist" | head -n1 || true)
	if [ -n "$ARTIFACT_NAME" ]; then
		ARTIFACT_PATH="${ROOT_DIR}/dist/${ARTIFACT_NAME}"
		ZIP_NAME="$PKG_DIR/HK-rainfall-mac.zip"
		echo "Zipping $ARTIFACT_PATH -> $ZIP_NAME"
		# remove old zip
		rm -f "$ZIP_NAME"
		if [ -d "$ARTIFACT_PATH" ]; then
			(cd "${ROOT_DIR}/dist" && zip -r "$ZIP_NAME" "$ARTIFACT_NAME")
		else
			(cd "${ROOT_DIR}/dist" && zip -r "$ZIP_NAME" "$ARTIFACT_NAME")
		fi
		echo "Created $ZIP_NAME"
	else
		echo "No artifact found in dist/ to zip"
	fi
else
	echo "dist/ not found; nothing to zip"
fi

echo "Done. Output in dist/"
