# Changelog

## [1.0.0] - 2026-03-03

### Added

- **Theme generator** (`generate.py`): single-file, zero-dependency Python script that reads `palette.json` and regenerates all editor themes. No more manual syncing.
- **Ghostty** terminal theme (light + dark variants)
- **Palette extensions**: `status`, `rainbow`, `sass` sections for structured access to semantic colors
- `.gitignore` for macOS artifacts

### Changed

- **PHPStorm**: extracted ~12,000-line Markdown Navigator blocks into static templates (`phpstorm/templates/`), keeping core attributes readable and generator-friendly
- **README**: added Ghostty installation, generator usage, updated PHPStorm install instructions
- Removed active line highlight from all themes (cleaner editing experience)
- Toned down code folding and indent guide colors

### Fixed

- Dark theme background mismatch between editor and gutter
- Blue indent guide incorrectly inheriting wrong color on light theme
- Code folding outline and indent rainbow colors
- Missing color settings for light theme (method separators, tearline, etc.)
- Added PHP 8+ tokens (enums, readonly, named arguments, attributes)

## [0.1.0] - 2022-02-10

### Added

- Initial release with light and dark variants for PHPStorm and Zed
- `palette.json` as single source of truth
- Dark variant generated via OKLCH perceptual lightness inversion
