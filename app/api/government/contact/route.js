import { NextResponse } from "next/server";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export async function POST(request) {
  try {
    const body = await request.json();

    const {
      organization,
      department,
      contactName,
      email,
      phone,
      country,
      message,
      priority,
    } = body;

    if (!organization || !contactName || !email || !message) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Missing required fields: organization, contactName, email, and message are mandatory.",
        },
        { status: 400 }
      );
    }

    const saved = await prisma.governmentContact.create({
      data: {
        organization,
        department,
        contactName,
        email,
        phone,
        country,
        message,
        priority: priority || "medium",
      },
    });

    return NextResponse.json(
      {
        success: true,
        message: "Government contact request stored successfully.",
        data: saved,
      },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error in /api/government/contact:", error);
    return NextResponse.json(
      {
        success: false,
        error: "Internal server error while processing government contact request.",
      },
      { status: 500 }
    );
  }
}
