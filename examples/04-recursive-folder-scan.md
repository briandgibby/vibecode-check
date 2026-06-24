# Example 4 — "recursive folder scan" — goal vs. mechanism

## The original prompt
What a newer programmer might actually type:

> hey can you write me a javascript function for an n8n code node that does a recursive folder scan of a google drive folder and returns every file path, going through all the subfolders no matter how deep

---

## Without the skill
A coding agent takes the prompt at face value and runs with it:

# Recursive Google Drive Folder Scanner for n8n Code Node

Here's a JavaScript function for an n8n Code node that recursively scans a Google Drive folder and returns every file path, no matter how deep the folder structure goes.

## Prerequisites

This uses the **Google Drive node credentials** via n8n's built-in HTTP request with OAuth. You'll need to pass in the root folder ID and have Google Drive credentials configured.

## The Code

```javascript
// n8n Code Node - Recursive Google Drive Folder Scanner
// Input: Set the rootFolderId variable below, or pass it in via $json.folderId

const rootFolderId = $json.folderId || 'YOUR_FOLDER_ID_HERE';

// Helper: fetch items in a folder (files + subfolders)
async function listFolderContents(folderId, token) {
  let allItems = [];
  let pageToken = null;

  do {
    const params = new URLSearchParams({
      q: `'${folderId}' in parents and trashed = false`,
      fields: 'nextPageToken, files(id, name, mimeType)',
      pageSize: '1000',
      ...(pageToken ? { pageToken } : {}),
    });

    const response = await $helpers.httpRequest({
      method: 'GET',
      url: `https://www.googleapis.com/drive/v3/files?${params.toString()}`,
      headers: {
        Authorization: `Bearer ${token}`,

> _…baseline truncated — the full no‑skill response ran 138 lines (it just started building)._

---

## With Vibecode Check

## Clarifying questions before I rewrite this

A few forks where a wrong guess would produce broken or useless code. Each has a recommended default — reply "use the defaults" to skip straight to the rewritten prompt.

**1. How is Google Drive authenticated in your n8n setup?**
n8n Code nodes can call external APIs, but they don't automatically have access to your Google Drive credentials — you need to either use the `googleapis` npm package with a service account key, or pass an OAuth2 access token in from a previous node (e.g. a Google Drive node that fetches the token).

- a) I have a Google Drive OAuth2 credential set up in n8n, and I'll pass the access token from a preceding node
- b) I'm using a Google service account (JSON key)
- c) I haven't set up auth yet — include a placeholder and point me to what I need

*Default: (a) — OAuth2 access token passed in from a preceding node via `$json.accessToken` or similar.*

**2. What's the input — how do you identify the root folder?**
- a) A Google Drive folder ID (the string from the URL, e.g. `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74`)
- b) A folder name (string search)
- c) The URL of the Drive folder

*Default: (a) — folder ID, passed in as `$json.folderId`.*

**3. What should the output look like?**
- a) An array of file path strings (e.g. `["FolderA/SubfolderB/report.pdf", ...]`)
- b) An array of objects with metadata (name, id, mimeType, path)
- c) n8n items — one item per file, so the next node can process them

*Default: (b) — array of objects with at least `name`, `id`, `mimeType`, and `path`, returned as n8n items (one per file).*

**4. What should count as a "file" — include or exclude Google Workspace files?**
Google Docs, Sheets, Slides, etc. live in Drive but have no real download URL. Do you want them in the results?

- a) Yes, include everything (Google Docs, Sheets, Slides, Forms, etc.)
- b) Only "real" files (PDFs, images, Office docs, CSVs — exclude Google Workspace native types)

*Default: (a) — include everything, with `mimeType` in the output so you can filter downstream.*

---

*Proceeding on all defaults.*

---

## The cleaned-up prompt

```
In an n8n Code node (JavaScript, "Run once for all items" mode), write a function that
traverses a Google Drive folder to any depth and returns every file it finds as n8n output
items.

**Context / inputs:**
- The root folder ID comes from the incoming item: `items[0].json.folderId`
- An OAuth2 access token is available at: `items[0].json.accessToken`
  (This token is fetched upstream by a Google Drive or HTTP Request node.)

**What the traversal must do:**
- Start at the root folder identified by `folderId`
- Find every file in that folder and in every nested subfolder, no matter how many
  levels deep the tree goes
- It must always terminate — even on very deep or large trees
- Do NOT include folders themselves in the output — only files

**Output:**
Return one n8n item per file, where each item's `json` contains:
- `id`     — the Drive file ID
- `name`   — the file's name
- `mimeType` — the full MIME type string (e.g. "application/vnd.google-apps.document")
- `path`   — the full path from the root folder to the file, using "/" as separator
              (e.g. "SubfolderA/SubfolderB/report.pdf")

Include all file types, including Google Workspace native types (Docs, Sheets, Slides, etc.).

**Implementation notes:**
- Use the Google Drive REST API: `https://www.googleapis.com/drive/v3/files`
  with the `q` parameter to list children and `fields=files(id,name,mimeType)`.
- Handle API pagination: follow `nextPageToken` until it is absent.
- Use `fetch` for HTTP calls (available in n8n Code nodes without imports).
- Use an iterative approach (an explicit queue/stack) rather than JavaScript call-stack
  recursion, so the function cannot hit a stack overflow on deep or wide trees.
- If the API returns an error status, throw a descriptive error.

**Verification:**
After writing the code, show me a sample of what the output items array would look like
for a folder tree with two levels of subfolders, so I can confirm the shape is right
before I wire it into my workflow.
```

---

## What I changed & corrected — and the convention behind it

**"Recursive folder scan" → goal + iterative implementation**
You wrote "recursive folder scan." "Recursive" names a *technique* — a function that calls itself — not just an outcome. The actual goal is: visit every nested subfolder, at any depth, and collect all files. Those aren't the same thing.

JavaScript call-stack recursion on a large Drive tree is genuinely risky: deep trees can overflow the call stack (Node has a default limit around 10,000–15,000 frames), and if the stop condition is wrong, the function never terminates. An iterative traversal — maintain an explicit queue of folders to visit, pop one, list its children, push any subfolders back — reaches the exact same outcome without those risks. It's the standard pattern for tree traversal in production code. The prompt now specifies the *goal* ("find every file in every nested subfolder, no matter how deep; must always terminate") and requests the iterative approach, because that's almost certainly what you want. If you specifically need true call-stack recursion — for example, to match an existing codebase's style — add that and the agent will write it, but the rewritten prompt uses the safer pattern by default.

**Auth approach made explicit**
The original prompt assumed the agent would know how to authenticate against Google Drive inside an n8n Code node. It wouldn't — there are several incompatible patterns (raw `googleapis` package with a service account, `$credentials` helper, token passed from upstream, etc.). The prompt now specifies OAuth2 access token passed in from a preceding node, which is the most common n8n pattern and requires no npm imports.

**"Returns every file path" → structured output items**
"Returns every file path" is ambiguous about shape. A plain array of strings gets the job done for a quick script but is hard to use in the next n8n node, which expects items with a `json` object. The rewritten prompt specifies one n8n item per file with `id`, `name`, `mimeType`, and `path`, which is the conventional shape for a Code node that feeds into downstream nodes.

**Pagination added explicitly**
Google Drive's list API is paginated — it returns at most 100 results per call and a `nextPageToken` if there are more. An agent not told to handle this will write a function that silently misses files in any large folder. Made explicit.

**Verification step added**
The original had no way to check the output. Added a request for a concrete sample output so you can confirm the shape before wiring it into your workflow — the fastest way to catch a wrong assumption early.

---

## Assumptions & possible misunderstandings — are we still in sync?

- I took "javascript function for an n8n code node" to mean the Code node in **"Run once for all items"** mode, where you return an array of item objects. If you're using "Run once per item" mode, the structure is slightly different — correct me if so.
- I assumed the access token is passed in from a preceding node. If you're using n8n's `$credentials('googleDriveOAuth2Api')` helper or a service account key baked into the node, the auth lines will look different.
- I assumed `folderId` (not a folder name or URL) is the input, coming from `items[0].json.folderId`. If your upstream node provides the folder ID under a different key, swap that reference.
- I assumed you want *only* files in the output (not folders). If you want folders listed too — say, to mirror a directory tree — add that.
- I assumed Google Workspace native types (Docs, Sheets, Slides) should be included, with `mimeType` in the output so you can filter them downstream if needed. If you want them excluded upfront, add a filter on `mimeType` not starting with `application/vnd.google-apps` (except `application/vnd.google-apps.folder`).
- "Path" is constructed during traversal by concatenating folder names with `/`. If the root folder itself should appear in the path prefix (e.g. `RootFolder/SubA/file.pdf` vs. `SubA/file.pdf`), that's a one-line change — let me know your preference.

---

## Prompt tips for next time

**Describe what you want, pin the "how" only when you mean to.**
"Recursive" is an implementation word — it tells the agent *how* to traverse, not *what* you want to achieve. When you bake in a technique you half-remember, the agent takes it literally, and literal recursion has real limits (stack depth, termination). The move that pays off every time: state the goal and its constraints ("visit every nested subfolder, to any depth; must always terminate; return all files"), and let the agent pick the implementation. If you genuinely need a specific technique — for performance, for stylistic consistency with existing code — name it *and* say why, so the agent knows it's deliberate. You'll get better, safer code and you'll learn which techniques are actually load-bearing in your requirements.

**For API-backed tasks, name the auth pattern.**
Any time you're hitting an external API (Drive, GitHub, Stripe, etc.) from a Code node, the single most likely way the generated code breaks is wrong or missing auth. One sentence — "OAuth2 access token available at `items[0].json.accessToken`" — removes what is otherwise the first thing the agent has to guess, and the guess is usually wrong.
