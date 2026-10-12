// Prefix a site-root path with the deployment base. Since 12 October 2026 this
// archive is served from https://lerena.defranceski.com/ with base '/', so BASE
// is '' and u() is the identity on a site-root path. It is kept, and still used,
// because the base is a deployment fact and not a thing pages should assume.
const BASE = import.meta.env.BASE_URL.replace(/\/$/, "");
export const u = (p = "/") => `${BASE}${p.startsWith("/") ? p : "/" + p}`;
