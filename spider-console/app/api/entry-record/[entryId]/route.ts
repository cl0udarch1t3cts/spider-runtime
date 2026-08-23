import { NextResponse } from "next/server";
import { fetchLatestRecordId } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ entryId: string }> },
) {
  const { entryId } = await params;
  try {
    return NextResponse.json({ recordId: await fetchLatestRecordId(entryId) });
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
