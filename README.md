# Kowsar & Ramin — QR / Cloudflare Pages Starter v1.2

Purpose: deploy a minimal, respectable Cloudflare Pages landing page and freeze one durable, retargetable business-card route at `/card` before the cards are designed or printed.

## Approved naming decision

Visible identity remains:

`Kowsar & Ramin`

Preferred Cloudflare Pages project/subdomain name:

`kowsar-ramin`

Preferred permanent printed-card URL, **only if Cloudflare actually assigns that exact production hostname**:

`https://kowsar-ramin.pages.dev/card`

Fallback if the first project name is unavailable:

`kowsarandramin`

If both approved names are unavailable, **stop and ask before creating or accepting another `pages.dev` hostname**. Do not accept a random suffix automatically.

Recommended GitHub repository name:

`kowsar-ramin-site`

The repository name does not define the public Pages hostname; the Pages project name does.

## Why `kowsar-ramin`

It is the strongest balance of human readability, international clarity, brand continuity, and QR efficiency. Removing the hyphen or abbreviating to initials does not provide enough practical benefit to justify weakening recognition. `/card` remains intentionally human-readable and gives us a stable routing endpoint separate from the root landing page.

See `NAMING_DECISION.md` for the locked rationale and fallback policy.

## Two permanent invariants after QR freeze

The printed QR will encode:

`https://<FINAL-APPROVED-PROJECT-SUBDOMAIN>.pages.dev/card`

After that QR has been approved for print:

1. **Never delete or repurpose `/card`.** Keep it as an HTTP 302 temporary redirect to the currently approved destination.
2. **Never delete/recreate the Cloudflare Pages project casually.** Cloudflare documents that the assigned `*.pages.dev` subdomain currently cannot be changed. Treat the verified production host as part of the physical card once printed.

Initial rule:

```text
/card / 302
```

Future examples:

```text
/card https://kowsarandramin.gamma.site 302
/card https://kowsarandramin.com 302
```

## Scope tonight

Do not build a sophisticated website. Tonight's irreversible decision is the URL embedded in the physical QR. The page behind it is intentionally minimal and can evolve later.

Do not add Pages Functions, JavaScript, frameworks, npm dependencies, trackers, forms, analytics, or another QR/URL-shortener service.

## Recommended deployment path

Use **Cloudflare Pages Git integration** for the first deployment.

1. Run `scripts/verify-source.ps1`.
2. Create a GitHub repository, recommended name: `kowsar-ramin-site`.
3. Commit this bundle to `main` and push.
4. In Cloudflare: Workers & Pages → Create → Pages → import/connect an existing Git repository.
5. Connect the GitHub repository.
6. Try Pages project name **`kowsar-ramin` first**.
7. If unavailable, try **`kowsarandramin`**.
8. If both are unavailable, stop and ask before creating another permanent hostname.
9. Framework preset: None.
10. Build command: `exit 0` (a blank build command is also valid for a frameworkless static project; this package uses `exit 0` explicitly).
11. Build output directory: `site`.
12. Production branch: `main`.
13. Deploy.
14. Record the exact production `*.pages.dev` URL Cloudflare assigns.

## QR freeze gate

Do **not** generate the production QR until all checks pass:

- exact production host has been recorded;
- the assigned hostname matches one of the approved names above, or a later name explicitly approved by the user;
- `https://<host>/` returns HTTP 200 and shows the expected landing page;
- `https://<host>/card` returns HTTP 302;
- the 302 has a valid `Location` target;
- following `/card` reaches the expected page;
- test succeeds in a private/incognito context or on a phone not authenticated to Cloudflare;
- the chosen `*.pages.dev` hostname is acceptable to print permanently.

Run:

```powershell
pwsh ./scripts/verify-card-route.ps1 -BaseUrl "https://<project>.pages.dev"
```

## After verification

1. Fill `DEPLOYMENT_RECORD.md`.
2. Return the exact verified `/card` URL to ChatGPT.
3. Generate one canonical static SVG QR from that exact URL.
4. Use the same SVG in both the one-sided and two-sided card masters.
5. Print at 100% physical size and scan-test before final print production.
