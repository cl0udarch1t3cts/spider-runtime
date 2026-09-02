import { NextResponse } from "next/server";
import { fetchRunLog } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ runId: string }> },
) {
  const { runId } = await params;
  try {
    return NextResponse.json(await fetchRunLog(runId));
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
