import { NextResponse } from "next/server";
import { computeBudget, fetchExecutor, fetchUsage } from "@/lib/api";

export const dynamic = "force-dynamic";

export async function GET() {
  const [executor, usage] = await Promise.allSettled([
    fetchExecutor(),
    fetchUsage(),
  ]);
  let usageValue =
    usage.status === "fulfilled" ? usage.value : { error: String(usage.reason) };
  // A console-set budget override (stored by the executor) beats the env
  // defaults, so the bar shows the same allowance the Doctor enforces.
  if (
    executor.status === "fulfilled" &&
    usage.status === "fulfilled" &&
    usage.value &&
    "windows" in usage.value
  ) {
    const override = (
      executor.value.stats as {
        doctor_budget?: { daily_percent: number | null; reserve_percent: number | null };
      }
    )?.doctor_budget;
    usageValue = {
      ...usage.value,
      budget: computeBudget(
        usage.value.windows,
        usage.value.source,
        override?.daily_percent,
        override?.reserve_percent,
      ),
    };
  }
  return NextResponse.json({
    generatedAt: new Date().toISOString(),
    executor:
      executor.status === "fulfilled"
        ? executor.value
        : { error: String(executor.reason) },
    usage: usageValue,
  });
}
