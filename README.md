# EnglishModernization

Tools for simplifying traditional English spellings using CMU pronunciations or direct dictionary lookups. Includes:
- A browser-based dictionary translator (`eng_to_us.html`) that uses `american.txt` only.
- The prior CMU-driven browser translator, preserved as `eng_to_us_2.html`.
- A CLI modernizer (`modernize.py`) that reads stdin and writes simplified text (CMU-based).

Repo: https://github.com/mikeNickaloff/EnglishModernization.git

## Quick Start
1) Clone  
```bash
git clone https://github.com/mikeNickaloff/EnglishModernization.git
cd EnglishModernization
```

2) Ensure Python 3 is installed  
- Linux/macOS: `python3 --version`  
- Windows: install from https://www.python.org/downloads/ and ensure `python` (or `python3`) is on PATH.

3) Get CMU dictionary  
`CMU.txt` is included. If you replace it, keep CMU formatting: `WORD  PH1 PH2 ...`.

## Run the Web Translator (self-hosted)
You need a small HTTP server so the page can fetch the dictionaries (`american.txt` for `eng_to_us.html`, `CMU.txt` for `eng_to_us_2.html`).

- Linux/macOS:  
  ```bash
  python3 -m http.server 8000
  ```  
  Then open:
  - http://localhost:8000/eng_to_us.html for the dictionary-only translator (american.txt)
  - http://localhost:8000/eng_to_us_2.html for the CMU-based translator

- Windows (PowerShell):  
  ```powershell
  python -m http.server 8000
  ```  
  Then open:
  - http://localhost:8000/eng_to_us.html
  - http://localhost:8000/eng_to_us_2.html

Usage: Type or paste text; the translated version appears live. Unknown words stay unchanged.

## Run the CLI Modernizer
Transform text via stdin → stdout using CMU pronunciations.

- Linux/macOS (bash):
  ```bash
  echo "The neighborhood brought weighty sacks through the thorough fair." \
    | python3 modernize.py --dict CMU.txt
  ```

- Windows (PowerShell):
  ```powershell
  "The neighborhood brought weighty sacks through the thorough fair." `
    | python modernize.py --dict CMU.txt
  ```

Convert a file to a new file (bash):
```bash
python3 modernize.py --dict CMU.txt < input.txt > output.txt
```

Convert a file (PowerShell):
```powershell
Get-Content input.txt | python modernize.py --dict CMU.txt | Set-Content output.txt
```

## Why a US-focused spelling?
Simplified, phoneme-driven spellings reduce ambiguity and better reflect American pronunciation (e.g., `weight → wate`, `through → throo`, `sacks → sax`). Using CMU ensures consistent phoneme inputs, yielding predictable modernized outputs for education, readability, and tooling that targets US English norms.

## Files
- `eng_to_us.html`: Browser translator using `american.txt` (dictionary replacements only).
- `eng_to_us_2.html`: Browser translator using `CMU.txt` (rule-based phoneme flow).
- `modernize.py`: CLI modernizer (stdin → stdout).
- `CMU.txt`: CMU Pronouncing Dictionary (primary dependency for CMU-based flows).  
- `CMU-PHONES.txt`, `IPA.txt`: Reference lists.

## Credits
- Project: EnglishModernization — https://github.com/mikeNickaloff/EnglishModernization.git
- Pronunciations: CMU Pronouncing Dictionary.
