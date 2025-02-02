import { type NextRequest, NextResponse } from "next/server"

export async function POST(req: NextRequest) {
  const formData = await req.formData()
  const file = formData.get("file") as File | null

  if (!file) {
    return NextResponse.json({ error: "No file uploaded" }, { status: 400 })
  }

  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)

  // Send the file to your FastAPI backend
  const backendUrl = process.env.BACKEND_URL || "http://localhost:8000"
  try {
    console.log("Sending request to backend:", `${backendUrl}/analyze/`)
    const backendFormData = new FormData()
    backendFormData.append("file", new Blob([buffer], { type: file.type }), file.name)

    const response = await fetch(`${backendUrl}/analyze/`, {
      method: "POST",
      body: backendFormData,
    })

    console.log("Backend response status:", response.status)
    const responseText = await response.text()
    console.log("Backend response text:", responseText)

    if (!response.ok) {
      return NextResponse.json(
        { error: `Backend error: ${response.status} ${responseText}` },
        { status: response.status },
      )
    }

    const data = JSON.parse(responseText)
    return NextResponse.json(data)
  } catch (error) {
    console.error("Error communicating with backend:", error)
    return NextResponse.json({ error: `Failed to communicate with backend: ${error}` }, { status: 500 })
  }
}

