<p align="center">

![Screenshot](./art/cover.png)

# Deligoez Theme

</p>

A minimalist color theme family with light and dark variants.

## Supported Editors

| Editor | Light | Dark | Path |
|--------|-------|------|------|
| **PHPStorm** | deligoez-light | deligoez-dark | `phpstorm/` |
| **Zed** | Deligoez Light | Deligoez Dark | `zed/` |

## Installation

### PHPStorm

1. Download `phpstorm/deligoez-light.icls` and/or `phpstorm/deligoez-dark.icls`
2. Import via `Preferences → Editor → Color Scheme → Import Scheme...`
3. Select the imported scheme

### Zed

Copy `zed/deligoez.json` (contains both light and dark) to your Zed themes directory:

```bash
cp zed/deligoez.json ~/.config/zed/themes/
```

Then select via `Cmd+K, Cmd+T` → "Deligoez Light" or "Deligoez Dark".

## Palette

All colors are defined in [`palette.json`](./palette.json) as the single source of truth. Platform-specific themes are derived from this palette.

The dark variant is generated using **OKLCH perceptual lightness inversion** — not simple RGB/HSL flipping. This preserves hue identity while ensuring proper contrast on dark backgrounds.

## Fonts

- [Mono Lisa](https://www.monolisa.dev/)

## Screenshots

### PHP
![PHP](./art/php.png)

### HTML
![HTML](./art/html.png)

### Javascript
![Javascript](./art/javascript.png)

### JSON
![JSON](./art/json.png)

### CSS
![CSS](./art/css.png)

### YAML
![YAML](./art/yaml.png)

## License

[MIT](./LICENSE)
