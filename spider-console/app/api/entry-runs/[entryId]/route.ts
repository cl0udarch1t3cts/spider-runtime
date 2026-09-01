import { NextResponse } from "next/server";
import { fetchEntryRuns } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ entryId: string }> },
) {
  const { entryId } = await params;
  try {
    // Entry IDs contain no "%", so decoding an already-decoded segment is safe.
    return NextResponse.json(await fetchEntryRuns(decodeURIComponent(entryId)));
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
