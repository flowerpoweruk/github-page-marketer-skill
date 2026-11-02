# Download

`github-page-marketer-1.0.1.skill` is the current portable bundle, including the supplied branding and skill icons. It is a ZIP-format archive with one `github-page-marketer` directory, including skill instructions, references, report template, worked example and runtime scripts. The original v1.0.0 bundle remains available alongside it.

Import it into a host that supports skill bundles, or extract the directory into your assistant's skills directory. Restart/reload skill discovery if needed. This does not create a separate AI service or require an API key.

Rebuild from the source checkout with `python3 scripts/build_skill.py --output /tmp/github-page-marketer-rebuilt.skill`. Archive timestamps and entry order are fixed so identical runtime sources produce identical archive bytes. Tests, evaluation fixtures, Git history and local evidence files are not included.
