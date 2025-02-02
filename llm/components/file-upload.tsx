"use client"

import { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
import { Card, CardContent } from "@/components/ui/card"
import { UploadCloud } from "lucide-react"

export function FileUpload({ onFileSelect }: { onFileSelect: (file: File) => void }) {
  const [fileName, setFileName] = useState<string>("")

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      const file = acceptedFiles[0]
      if (file) {
        setFileName(file.name)
        onFileSelect(file)
      }
    },
    [onFileSelect],
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "text/plain": [".txt"] },
    multiple: false,
  })

  return (
    <Card className="w-full">
      <CardContent className="p-6">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
            ${isDragActive ? "border-primary bg-primary/10" : "border-gray-300 dark:border-gray-700"}`}
        >
          <input {...getInputProps()} />
          <UploadCloud className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            {isDragActive ? "Drop the file here" : "Drag and drop a text file here, or click to select"}
          </p>
          {fileName && <p className="mt-2 text-sm font-medium text-primary">{fileName}</p>}
        </div>
      </CardContent>
    </Card>
  )
}

