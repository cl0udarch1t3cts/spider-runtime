import { NextResponse } from "next/server";
import { enqueueExecution } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  const { entryId } = (await request.json().catch(() => ({}))) as {
    entryId?: string;
  };
  if (!entryId || typeof entryId !== "string") {
    return NextResponse.json({ error: "entryId is required" }, { status: 400 });
  }
  try {
    const result = await enqueueExecution(entryId);
    return NextResponse.json(result.body ?? {}, { status: result.status });
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
