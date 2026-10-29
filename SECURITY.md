# Security Policy

Chronoscape is a static website: HTML, JavaScript, images and 3D models served from Cloudflare, with no server code,
accounts, database or user data. The browser keeps a few preferences (like the desk toggle) and the list of maps you've opened in
`localStorage`, on your device only. Still, problems can exist, for example in how content is rendered, in the build and deploy pipeline,
or in a dependency.

## Supported versions

Only the current `main` branch and the live site it deploys are supported.

## Reporting a vulnerability

**Please don't open a public issue.** Report it privately through GitHub:
go to the repository's **Security** tab and choose **Report a vulnerability**.

Include what you found, how to reproduce it, and what an attacker could do with it. You can expect an
acknowledgement within a week; once confirmed, a fix will be prepared privately and released, and you'll be credited
in the advisory unless you'd rather not be.

## Out of scope

- Historical inaccuracies (please open a **Content correction** issue instead)
- Reports from automated scanners without a demonstrated impact
- Missing security headers on a static site without a concrete exploit
