// Staging front door: forwards every request to one of the release containers.
// The customer form is stateless (signed build tokens), so any instance serves
// any request. When STAGING_PASSWORD is set, the whole site asks for it.
import { Container, getRandom } from "@cloudflare/containers";
import { env } from "cloudflare:workers";

export class CatalogForm extends Container {
  defaultPort = 8080;
  sleepAfter = "15m";
  envVars = {
    CATALOG_ORIGIN: env.CATALOG_ORIGIN,
    CATALOG_BUILD_TOKEN_KEY: env.CATALOG_BUILD_TOKEN_KEY,
    // Staging never sends build requests to the dealership.
    CATALOG_DEALER_SUBMISSIONS: "0",
  };
}

function authorized(request, password) {
  if (!password) return true;
  const header = request.headers.get("Authorization") || "";
  const [scheme, encoded] = header.split(" ");
  if (scheme !== "Basic" || !encoded) return false;
  let supplied;
  try {
    // atob() yields byte-valued characters; decode those bytes as UTF-8 so
    // credentials with non-ASCII characters compare correctly.
    const bytes = Uint8Array.from(atob(encoded), (c) => c.charCodeAt(0));
    supplied = new TextDecoder("utf-8").decode(bytes).split(":").slice(1).join(":");
  } catch {
    return false;
  }
  // Constant-time comparison, so response timing does not reveal the password.
  const encoder = new TextEncoder();
  const a = encoder.encode(supplied), b = encoder.encode(password);
  return a.length === b.length && crypto.subtle.timingSafeEqual(a, b);
}

export default {
  async fetch(request, env) {
    if (!env.CATALOG_ORIGIN || !env.CATALOG_BUILD_TOKEN_KEY) {
      return new Response("Staging is not configured: set CATALOG_ORIGIN and CATALOG_BUILD_TOKEN_KEY.", { status: 503 });
    }
    if (!authorized(request, env.STAGING_PASSWORD)) {
      return new Response("Staging access requires a password.", {
        status: 401,
        headers: { "WWW-Authenticate": 'Basic realm="Corvette staging", charset="UTF-8"' },
      });
    }
    const container = await getRandom(env.CATALOG_FORM, Number(env.CONTAINER_INSTANCES || 2));
    return container.fetch(request);
  },
};
