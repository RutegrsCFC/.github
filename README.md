# RutegrsCFC/.github

The organization profile for **Rutgers Chinese Finance Club · 罗格斯华人金融社团**, shown at
[github.com/RutegrsCFC](https://github.com/RutegrsCFC).

- `profile/README.md` is the page itself.
- `profile/assets/*.svg` are generated. Edit `scripts/build_profile_assets.py`, then regenerate:

```bash
rm -rf profile/assets && python3 scripts/build_profile_assets.py profile/assets scripts/logo360.png
```

The script writes each SVG under a content-hashed name and updates `profile/README.md` to match,
so browsers never show a cached old image.

Every SVG is drawn at 846px wide (the README column on desktop) and is self-contained (system
fonts, embedded logo), because GitHub shows README images through `<img>`, which blocks external
fonts and images. Each image comes in `-light` and `-dark`; the README adds both with the
`#gh-light-mode-only` / `#gh-dark-mode-only` fragments, so GitHub shows the one matching the
viewer's GitHub theme.
