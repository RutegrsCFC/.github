# RutegrsCFC/.github

The organization profile for **Rutgers Chinese Finance Club · 罗格斯华人金融社团**, shown at
[github.com/RutegrsCFC](https://github.com/RutegrsCFC).

- `profile/README.md` is the page itself.
- `profile/assets/*.svg` are generated. Edit `scripts/build_profile_assets.py`, then regenerate:

```bash
python3 scripts/build_profile_assets.py profile/assets scripts/logo360.png
```

Every SVG is self-contained (system fonts, embedded logo), because GitHub shows README images
through `<img>`, which blocks external fonts and images. Section images come in `-light` and
`-dark` variants; the README picks one with `<picture>` and `prefers-color-scheme`.
