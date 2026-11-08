# Nepali Rhyme Hub: YouTube Studio branding plan (waiting for Sanam's approval)

Prepared 2026-11-08. NOTHING has been published. Page: https://studio.youtube.com/channel/UCuZRsCjjzvlLPdL5AsgWE7w/editing/profile

## 1. Account read on the page

- Top-right account chip: **"Nepali Rhyme Hub / You're a manager"**
- Left nav: "Channel / Nepali Rhyme Hub"; header element: "Nepali Rhyme Hub"
- Name field: `Nepali Rhyme Hub`; handle: `@NepaliRhymeHub`; channel URL ends `UCuZRsCjjzvlLPdL5AsgWE7w`. Matches.

## 2. Current values (BEFORE, for rollback)

Screenshots: `brand/studio_before_top.png` (banner + picture), `brand/studio_before_bottom.png` (links, contact, watermark).

| Item | Current value |
|---|---|
| Banner | **Empty** (Studio placeholder graphic; public channel page has no banner) |
| Profile picture | **Default** purple letter "N" avatar, `https://yt3.googleusercontent.com/ytc/AIdro_mkLO97kTQBhD1y6_12_RwCBlZbvm0lFWC1fm-6j2EAW9Vj9t7ftMX_By3gz5Ppz7-oIQ=s900-c-k-c0x00ffffff-no-rj` (`ytc/` = auto-generated) |
| Watermark | **Empty** (placeholder) |
| Name / handle | Nepali Rhyme Hub / @NepaliRhymeHub (do not touch) |
| Description | Set (Nepali + English, starts "नेपाली बालगीत, भैलो-देउसी र चाडपर्वका रमाइला गीत! 🪔 ...", ends "📩 सम्पर्क: info.bhrikuty@gmail.com") (do not touch) |
| Links | **None shown**, only an "Add link" button. Earlier notes said links were set; they are not on this page. Not changed here. |
| Contact email | info.bhrikuty@gmail.com (do not touch) |

Rollback: banner and watermark have a "Remove" option after upload; picture goes back to the default letter avatar via "Remove". Then Publish.

## 3. Proposed values (AFTER)

| Item | File | Checked |
|---|---|---|
| Profile picture | `D:\claude_project\nepalirhymehub\brand\flow\profile_A.png` | 800x800 PNG, 742,461 bytes (limit ≥98x98, ≤4 MB): OK. The circle crop cuts only the ribbon tips; "नेपाली राइम हब" stays inside. At small sizes the text is too small to read, but the red panda still reads. |
| Banner | `D:\claude_project\nepalirhymehub\brand\banner.png` | 2560x1440 PNG, 4,205,632 bytes (limit ≥2048x1152, ≤6 MB): OK |
| Watermark | `D:\claude_project\nepalirhymehub\brand\watermark_A.png` (new, made from `flow/logo_A_transparent.png` 606x593: scaled to 150x147, centred on a transparent 150x150 canvas) | 150x150 RGBA PNG, 51,295 bytes (limit 150x150, ≤1 MB): OK |

No file broke a limit, so no `_studio` copies were made.

**Watermark display time:** recommend **Entire video**. The logo is the brand mark, and showing it all the time builds recognition. "End of video" only covers the last 15 seconds, which most toddler viewers never reach.
**Caveat:** YouTube's list of features turned off for made-for-kids videos includes the channel branding watermark. Every video on this channel is meant to be made for kids, so the watermark will probably not appear on them. Setting it costs nothing and covers any non-kids upload. Check this before relying on it.

## 4. Staging done so far (preview only, not live)

- **Profile picture: STAGED.** profile_A.png was uploaded through the picture `file-selector` and Customize picture > Done was clicked. Studio now shows it as a local `data:` preview and the Publish button became enabled. The public channel page still shows the default avatar, which confirms that staging does not go live.
- **Banner and watermark: NOT staged.** During the banner upload another process using the same browser-harness session switched the active tab to TikTok Studio, and the upload did not reach Studio. To avoid interfering with that job, I stopped switching tabs. Both go in as part of the steps below.
- The staged picture is lost if the Studio tab reloads. That is harmless: just redo step A.

## 5. Exact steps to apply (after Sanam approves)

0. Make sure no other agent is driving the browser. Switch to the Studio tab, `4B85155BA2B129D26BC8FA0E0AB193D1` (`.../editing/profile`). Read the top-right chip: it must say "Nepali Rhyme Hub". Stop if it does not.
A. Picture (skip if the preview already shows the red panda): `browser_upload_file("ytcp-profile-image-upload input[type=file]", profile_A.png)` → in "Customize picture" keep the full-square crop → JS `document.querySelector('ytcp-button#done-button').click()`.
B. Banner: `browser_upload_file("ytcp-banner-upload input[type=file]", banner.png)` → "Customize banner art" dialog: keep the default full crop and check the logo and name sit inside the "viewable on all devices" box → click `ytcp-button#done-button`.
C. Watermark: `browser_upload_file("ytcp-video-watermark-upload input[type=file]", watermark_A.png)` → in the dialog accept the crop/Done → choose display time **Entire video** (a radio button: use a coordinate click, screenshot px x 1.28 = viewport px if scaled) → Done/Save in the dialog.
D. Screenshot the whole page. Check that the name, handle, description, contact email and (empty) links are unchanged against section 2.
E. Click **Publish** (top right) once. This is the only public action.

## 6. Read-back after saving

1. Reload `.../editing/profile`. Check that `img.profile-preview` src is a `yt3.ggpht.com` URL without `/ytc/`, that the banner and watermark sections show the new images, and that the watermark display time reads "Entire video".
2. Check the public page: `curl -s -A "Mozilla/5.0" https://www.youtube.com/channel/UCuZRsCjjzvlLPdL5AsgWE7w | grep -oE 'og:image" content="[^"]+'` should show a new avatar URL (not `ytc/AIdro_mkLO97...`), and `grep -c '"banner":'` should be ≥1 (it was 0 before). Changes can take a few minutes to spread.
3. Re-read the description, email and links and compare them with section 2. Save after-screenshots as `brand/studio_after_*.png`.

## Applied 2026-11-08 (Sanam: "1 upload everything")
- Account read before publishing: "Nepali Rhyme Hub" / @NepaliRhymeHub / UCuZRsCjjzvlLPdL5AsgWE7w.
- Uploaded banner.png, flow/profile_A.png, watermark_A.png (Entire video); Publish clicked once.
- Read back: Studio reload shows banner + watermark (Entire video) + new picture; public page shows the new Puntu avatar (old ytc/AIdro avatar gone). Banner live on the public page a minute later (checked).
- Name, handle, description, contact email unchanged. Links still empty.
