# Foundational source mapping

Read RECONSTRUCTION.md and DEPENDENCY_DAG.json. This preserves the pre-implementation historical reconstruction and its status labels. Later reviewed bridge packets are separate successors; old NOT_ATTEMPTED labels are not current denials of their existence.

Read PROJECTION_NOTES.md and SOURCE_PACKAGE.json for the finite public selection. Source and receipt locators are not a payload allowlist. No proof compilation is needed to inspect these maps.

Run python3 verify.py for local identity/locator consistency. Optionally use python3 verify.py --reports "$REPORT_DOCX_DIRECTORY" to compare all 270 locator hashes to six externally supplied authoritative report/guide DOCX files. The checker reads only, emits no paragraph bodies and writes no output.
