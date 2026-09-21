import { NextResponse } from "next/server";

export function middleware(request) {
  const url = request.nextUrl;

  // Protect the admin route
  if (url.pathname.startsWith("/dashboard/government/admin")) {
    const token = request.cookies.get("auth_token");

    // If no token, block access
    if (!token) {
      return NextResponse.redirect(new URL("/dashboard", request.url));
    }
  }

  return NextResponse.next();
}
