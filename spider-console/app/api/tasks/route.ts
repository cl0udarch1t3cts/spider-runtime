import { NextResponse } from "next/server";
import { fetchDoctorTasks } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const params = new URL(request.url).searchParams;
  const status = params.get("status");
  const entry = params.get("entry");
  try {
    return NextResponse.json(await fetchDoctorTasks(status, entry));
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
