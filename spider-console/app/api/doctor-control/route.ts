import { NextResponse } from "next/server";

const EXECUTOR_API_URL = (
  process.env.EXECUTOR_API_URL ?? "http://127.0.0.1:8000"
).replace(/\/$/, "");

export const dynamic = "force-dynamic";

export async function PUT(request: Request) {
  const body = (await request.json().catch(() => ({}))) as {
    paused?: boolean;
    daily_percent?: number;
    reserve_percent?: number;
  };
  const payload: Record<string, boolean | number> = {};
  if (typeof body.paused === "boolean") payload.paused = body.paused;
  if (typeof body.daily_percent === "number")
    payload.daily_percent = body.daily_percent;
  if (typeof body.reserve_percent === "number")
    payload.reserve_percent = body.reserve_percent;
  if (Object.keys(payload).length === 0) {
    return NextResponse.json(
      { error: "provide paused, daily_percent, or reserve_percent" },
      { status: 400 },
    );
  }
  try {
    const response = await fetch(`${EXECUTOR_API_URL}/api/v1/doctor-control`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      cache: "no-store",
      signal: AbortSignal.timeout(10_000),
    });
    return NextResponse.json(await response.json(), { status: response.status });
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
