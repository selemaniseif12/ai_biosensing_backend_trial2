import { NextResponse } from "next/server";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

/**
 * GET /api/government/all
 * Returns all government communication records.
 */

export async function GET() {
  try {
    const records = await prisma.governmentContact.findMany({
      orderBy: { createdAt: "desc" },
    });

    return NextResponse.json(
      {
        success: true,
        data: records,
      },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error fetching government records:", error);

    return NextResponse.json(
      {
        success: false,
        error: "Internal server error while fetching government records.",
      },
      { status: 500 }
    );
  }
}
