import { NextResponse } from "next/server";
import { fetchRecord } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  try {
    return NextResponse.json(await fetchRecord(id));
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
