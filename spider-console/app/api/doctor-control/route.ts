import { NextResponse } from "next/server";

const EXECUTOR_API_URL = (
  process.env.EXECUTOR_API_URL ?? "http://127.0.0.1:8000"
).replace(/\/$/, "");

export const dynamic = "force-dynamic";

export async function PUT(request: Request) {
  const { paused } = (await request.json().catch(() => ({}))) as {
    paused?: boolean;
  };
  if (typeof paused !== "boolean") {
    return NextResponse.json({ error: "paused must be a boolean" }, { status: 400 });
  }
  try {
    const response = await fetch(`${EXECUTOR_API_URL}/api/v1/doctor-control`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ paused }),
      cache: "no-store",
      signal: AbortSignal.timeout(10_000),
    });
    return NextResponse.json(await response.json(), { status: response.status });
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
