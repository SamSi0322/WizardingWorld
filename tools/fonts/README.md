# Guide fonts

Fonts embedded in the player guide PDFs (`generate_english_pdf.py`, `generate_chinese_pdf.py`).
Both families are licensed under the SIL Open Font License 1.1 (see the `OFL-*.txt` files).

| File | Font | Source |
| --- | --- | --- |
| `PlayfairDisplay-Bold.ttf`, `-SemiBold.ttf`, `-MediumItalic.ttf` | Playfair Display (Latin subset, static instances) | [clauseggers/Playfair-Display](https://github.com/clauseggers/Playfair-Display) via Fontsource |
| `IBMPlexSans-Regular.ttf`, `-SemiBold.ttf`, `-Italic.ttf` | IBM Plex Sans (Latin subset, static instances) | [IBM/plex](https://github.com/IBM/plex) via Fontsource |

The Chinese guide uses a system font instead (Microsoft YaHei or SimHei on Windows, Heiti SC on
macOS, Noto Sans CJK on Linux), or any font set with `WW_CJK_FONT=/path/to/font`.
