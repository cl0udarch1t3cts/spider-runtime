import { NextResponse } from "next/server";
import { fetchDoctorTasks } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const status = new URL(request.url).searchParams.get("status");
  try {
    return NextResponse.json(await fetchDoctorTasks(status));
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 502 });
  }
}
