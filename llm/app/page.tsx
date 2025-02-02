"use client"

import { useState } from "react"
import { FileUpload } from "@/components/file-upload"
import { ResultsTable } from "@/components/results-table"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useToast } from "@/components/ui/use-toast"

interface Entity {
  entity: string
  type: string
}

interface AnalysisResult {
  openai_results: Entity[]
  huggingface_results: Entity[]
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [results, setResults] = useState<AnalysisResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const handleSubmit = async () => {
    if (!file) return

    setIsLoading(true)
    const formData = new FormData()
    formData.append("file", file)

    try {
      console.log("Sending request to /api/analyze")
      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      })
      console.log("Response status:", response.status)
      const responseText = await response.text()
      console.log("Response text:", responseText)

      if (!response.ok) {
        throw new Error(`Failed to analyze text: ${response.status} ${responseText}`)
      }

      const data: AnalysisResult = JSON.parse(responseText)
      setResults(data)
      toast({
        title: "Analysis Complete",
        description: "The text has been successfully analyzed.",
      })
    } catch (error) {
      console.error("Error analyzing text:", error)
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "An unknown error occurred",
        variant: "destructive",
      })
    }
    setIsLoading(false)
  }

  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle>Upload Text File</CardTitle>
        </CardHeader>
        <CardContent>
          <FileUpload onFileSelect={setFile} />
          <Button className="mt-4 w-full" onClick={handleSubmit} disabled={!file || isLoading}>
            {isLoading ? "Analyzing..." : "Analyze Text"}
          </Button>
        </CardContent>
      </Card>

      {results && (
        <Card>
          <CardHeader>
            <CardTitle>Named Entity Recognition Results</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <ResultsTable title="OpenAI Results" entities={results.openai_results} />
              <ResultsTable title="Hugging Face Results" entities={results.huggingface_results} />
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

