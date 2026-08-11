# Web build

This repository includes a browser-playable build in `docs/`.

To rebuild it after game changes:

```bash
python -m pygbag --build --disable-sound-format-error .
```

Then replace the contents of `docs/` with the generated files from `build/web/` and publish GitHub Pages from the `main` branch's `/docs` folder.
