# Vestaboard Solar Display

Displays (currently simulated) rooftop solar production on a Vestaboard
Note, updated automatically every 5 minutes via GitHub Actions.

Files in this project:
- `solar_display.py` - the script that generates the message and sends it
- `requirements.txt` - Python packages needed
- `.github/workflows/update_board.yml` - tells GitHub to run the script every 5 minutes
- `README.md` - this file

---

## PART 1: Get your Vestaboard API key

1. Go to https://web.vestaboard.com and log in.
2. Find the **Developer** / **API** section of your account settings.
3. Look for **Cloud API** (this is the current name for what used to be
   called the "Read/Write API"). Generate a key for your Note.
4. Copy the key somewhere safe temporarily (a plain text file on your
   computer is fine for now - do NOT put it in the code).

---

## PART 2: Create a GitHub account

1. Go to https://github.com and click **Sign up**.
2. Follow the prompts (email, password, username). Verify your email
   when GitHub asks.
3. You can use the free plan - everything in this project fits inside it.

---

## PART 3: Create the repository

1. Once logged in, click the **+** icon (top right) → **New repository**.
2. Name it something like `vestaboard-solar`.
3. Set visibility to **Public**. (Don't worry - your actual API key
   will never be stored in the code itself, so this is safe. See Part 5.)
4. Click **Create repository**.

---

## PART 4: Upload the project files

You do NOT need to install git or use the command line for this - GitHub's
website lets you upload files directly.

1. On your new (empty) repository page, click **uploading an existing file**
   (or **Add file → Upload files**).
2. Drag in `solar_display.py` and `requirements.txt`.
3. Click **Commit changes**.
4. Now for the workflow file, which needs to live in a specific folder
   path (`.github/workflows/`). Click **Add file → Create new file**.
5. In the "Name your file" box, type the FULL path:
   `.github/workflows/update_board.yml`
   (GitHub will automatically create the folders for you as you type
   the `/` characters.)
6. Open `update_board.yml` from this project, copy its entire contents,
   and paste it into GitHub's editor.
7. Click **Commit changes**.

---

## PART 5: Add your Vestaboard API key as a GitHub Secret

This keeps your key out of the code entirely - GitHub injects it
securely only when the workflow runs.

1. In your repository, click **Settings** (top menu of the repo, not
   your account settings).
2. In the left sidebar: **Secrets and variables → Actions**.
3. Click **New repository secret**.
4. Name: `VESTABOARD_API_KEY`
5. Value: paste the API key from Part 1.
6. Click **Add secret**.

---

## PART 6: Test it manually

Don't wait for the 5-minute schedule - trigger it by hand first so you
can catch any errors quickly.

1. Click the **Actions** tab at the top of your repository.
2. In the left sidebar, click **Update Vestaboard Solar Display**.
3. Click the **Run workflow** dropdown button → **Run workflow**.
4. Refresh after a few seconds - you'll see a run appear. Click into it,
   then click **update-board** to watch the live log.
5. If it succeeds (green check), check your Vestaboard - it should now
   show simulated solar data.
6. If it fails (red X), click into the failed step to read the error
   message. Common issues:
   - Missing/misspelled secret name (must be exactly `VESTABOARD_API_KEY`)
   - Wrong API key copied
   - Typo introduced when pasting the workflow YAML

---

## PART 7: Let it run automatically

Once the manual test works, you're done - GitHub will now run the
workflow every 5 minutes on its own, forever, for free.

**One gotcha to know about:** GitHub automatically disables scheduled
workflows if a repository goes 60 days with no activity at all. If your
board ever silently stops updating after a couple months, go to the
Actions tab and manually re-enable the workflow (or just re-run it once).

---

## PART 8: Swap in real Solis data (once you have that API key)

Everything about the Vestaboard side of this stays exactly the same.
The only thing you'll change is the `simulate_solar_production()`
function in `solar_display.py` - instead of generating fake numbers,
it will call the Solis API and return real ones.

When you're ready for this step, come back and we'll:
1. Register for Solis API access and get your key/secret
2. Add those as two more GitHub Secrets (same process as Part 5)
3. Replace `simulate_solar_production()` with a real API call
4. Test manually again (Part 6) before trusting the schedule

---

## Testing locally on your own computer (optional but recommended)

If you have Python installed, you can test the script before ever
touching GitHub:

```bash
cd vestaboard-solar
pip install -r requirements.txt

# Mac/Linux:
export VESTABOARD_API_KEY="your-key-here"
python3 solar_display.py

# Windows (PowerShell):
$env:VESTABOARD_API_KEY="your-key-here"
python solar_display.py
```

If your board updates, you're good to go.
