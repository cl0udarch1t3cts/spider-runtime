import { NextResponse } from "next/server";
import { scrapeFailed } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function POST() {
  try {
    const result = await scrapeFailed();
    return NextResponse.json(result.body ?? {}, { status: result.status });
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
