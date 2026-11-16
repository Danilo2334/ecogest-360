export type Row = Record<string, any>;
export async function api(
  path: string,
  data?: unknown,
  method = "POST",
  key?: string,
): Promise<any> {
  const headers: Record<string, string> = {};
  if (data !== undefined) {
    const csrf = await fetch("/api/session/csrf", {
      credentials: "same-origin",
    }).then((r) => r.json());
    headers["X-CSRFToken"] = csrf.csrfToken;
    headers["Idempotency-Key"] = key || crypto.randomUUID();
    if (!(data instanceof FormData))
      headers["Content-Type"] = "application/json";
  }
  const response = await fetch("/api/" + path, {
    method: data === undefined ? "GET" : method,
    credentials: "same-origin",
    headers,
    body:
      data === undefined
        ? undefined
        : data instanceof FormData
          ? data
          : JSON.stringify(data),
  });
  const payload = await response
    .json()
    .catch(() => ({ message: "Respuesta no válida del servidor." }));
  if (!response.ok)
    throw new Error(payload.message || "No se pudo completar la operación.");
  return payload;
}
