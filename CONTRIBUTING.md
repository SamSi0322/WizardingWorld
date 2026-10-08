# Contributing to Wizarding World

Thanks for the interest. This is a single-maintainer fan project at the **release-candidate** stage: the main single-player route has been played through from the Hogwarts Letter to the Deathly Hallows ending, so the most valuable help now is wider testing (multiplayer sync, balance, fresh installs), localization proofreading and sprite polish. The maintainer has limited bandwidth; collaborators who **take ownership of an issue** are exactly what the project needs.

See the **[Looking for help](README.md#looking-for-help)** section in the README for the current collaboration tracks and their labels. Browse [open issues](https://github.com/SamSi0322/WizardingWorld/issues) or open a new one — comment "I'll take this" to claim, work on a fork, open a PR.

Pull requests are welcome — please skim the constraints below before sinking time into a large change.

## Quick start (building the mod)

This is a tModLoader mod, not a standalone .NET project. You **cannot** `dotnet build` it from a checkout alone — the csproj imports `../tModLoader.targets`, which lives inside your tModLoader install directory.

1. Install **tModLoader** from Steam (free DLC for Terraria).
2. Install the **.NET 8 SDK**.
3. Clone this repo into your tModLoader `ModSources/` folder:
   - Windows: `%userprofile%\Documents\My Games\Terraria\tModLoader\ModSources\WizardingWorld\`
   - Linux: `~/.local/share/Terraria/tModLoader/ModSources/WizardingWorld/`
   - macOS: `~/Library/Application Support/Terraria/tModLoader/ModSources/WizardingWorld/`
4. Open tModLoader → **Workshop → Develop Mods → Build + Reload**.

For deeper architecture and naming conventions, read [`CLAUDE.md`](CLAUDE.md) (project context), [`AGENTS.md`](AGENTS.md) (build commands & style), and [`ContentManifest.md`](ContentManifest.md) (content inventory).

## Reporting bugs

Open a [GitHub Issue](https://github.com/SamSi0322/WizardingWorld/issues) with:

- tModLoader version + .NET SDK version + OS
- Mod version (top of `build.txt`)
- Reproduction steps — a "do X, observe Y" path or a save file
- The relevant tModLoader log if there's a crash (`%userprofile%\Documents\My Games\Terraria\tModLoader\Logs\` on Windows)

## Proposing changes

For non-trivial changes, open an issue first describing the problem and your approach. Changes touching `Common/Players/` or `Common/Systems/` need save/load and multiplayer-sync verification before merge.

### Code style

- **Tabs** for indentation.
- C# identifiers: PascalCase for public types and members, camelCase for locals and fields.
- Namespaces mirror folder paths: `WizardingWorld.Content.Items.Weapons`.
- One main type per file; file naming follows existing patterns (`[BossName]Boss.cs`, `[SpellName]Projectile.cs`, `[HouseName]Robes.cs`).
- When renaming content, update all three localization HJSON files (`Localization/`) at once.
- If guide counts or progression data change, run `python scripts/verify_guide.py` and regenerate the affected PDF (`generate_english_pdf.py` / `generate_chinese_pdf.py`).

### Testing

There's no automated test suite — `dotnet test` will not work for a tModLoader mod. Every change should:

- Build without errors inside tModLoader.
- Load without missing-asset or localization errors.
- Be smoke-tested in-game on a fresh character (exercise the changed content path).
- For `Common/Players/` and `Common/Systems/`: include save/load and multiplayer-sync verification.

## What's out of scope

PRs that bolt on these without prior discussion are likely to be closed:

- Cosmetic-only refactors of large content files.
- Changes that contradict the canon-audited Hallows / Horcrux / Master-of-Death progression.
- **Any third-party Harry Potter IP**: sprite rips from films, audio from games, copyrighted text from books. Self-created sprites and original audio only — see the IP note below.

## License & intellectual property

By submitting a pull request you agree that your contribution is released under the [MIT License](LICENSE).

This is an **unofficial fan project**. Do not include sprite rips, audio rips, copyrighted images, or copyrighted text from any Harry Potter film, game, book, or other commercial product. The MIT license here applies only to original code and self-created assets; it does not — and cannot — license any third-party intellectual property.
