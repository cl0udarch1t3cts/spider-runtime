import { NextResponse } from "next/server";
import { requestRepair } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function POST(
  _request: Request,
  { params }: { params: Promise<{ runId: string }> },
) {
  const { runId } = await params;
  try {
    const result = await requestRepair(runId);
    return NextResponse.json(result.body ?? {}, { status: result.status });
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
