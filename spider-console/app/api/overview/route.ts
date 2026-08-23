import { NextResponse } from "next/server";
import { fetchExecutor, fetchUsage } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function GET() {
  const [executor, usage] = await Promise.allSettled([
    fetchExecutor(),
    fetchUsage(),
  ]);
  return NextResponse.json({
    generatedAt: new Date().toISOString(),
    executor:
      executor.status === "fulfilled"
        ? executor.value
        : { error: String(executor.reason) },
    usage:
      usage.status === "fulfilled"
        ? usage.value
        : { error: String(usage.reason) },
  });
}
