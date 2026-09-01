import { NextResponse } from "next/server";
import { fetchUnresolvedRuns } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    return NextResponse.json(await fetchUnresolvedRuns());
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
