"use client";

import { useRef, useState } from "react";

import {
  Upload,
  FileText,
  X,
  Loader2,
} from "lucide-react";

import {
  uploadDocument,
} from "@/lib/api";


interface Props {
  onUploaded?: () => void;
}


export default function UploadDocument({
  onUploaded,
}: Props) {

  const inputRef =
    useRef<HTMLInputElement>(null);

  const [file, setFile] =
    useState<File | null>(null);

  const [uploading, setUploading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  function handleFile(
    selectedFile: File
  ) {
    setError(null);

    setFile(selectedFile);
  }


  async function handleUpload() {

    if (!file) {
      return;
    }

    try {

      setUploading(true);
      setError(null);

      await uploadDocument(file);

      setFile(null);

      if (inputRef.current) {
        inputRef.current.value = "";
      }

      onUploaded?.();

    } catch (error) {

      setError(
        error instanceof Error
          ? error.message
          : "Upload failed."
      );

    } finally {

      setUploading(false);

    }
  }


  return (
    <div className="rounded-2xl bg-white p-8 shadow-sm border border-gray-100">

      <div className="text-center">

        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50">

          <Upload className="h-7 w-7 text-blue-600" />

        </div>


        <h2 className="text-xl font-semibold">
          Upload Document
        </h2>

        <p className="mt-2 text-sm text-gray-500">
          PDF, DOCX, TXT, JPG or PNG
        </p>


        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.txt,.jpg,.jpeg,.png"
          className="hidden"
          onChange={(event) => {

            const selected =
              event.target.files?.[0];

            if (selected) {
              handleFile(selected);
            }

          }}
        />


        {!file && (
          <button
            type="button"
            onClick={() =>
              inputRef.current?.click()
            }
            className="mt-6 rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700"
          >
            Choose File
          </button>
        )}


        {file && (
          <div className="mx-auto mt-6 max-w-md">

            <div className="flex items-center justify-between rounded-lg border p-4">

              <div className="flex items-center gap-3">

                <FileText className="h-6 w-6 text-blue-600" />

                <div className="text-left">

                  <p className="max-w-xs truncate text-sm font-medium">
                    {file.name}
                  </p>

                  <p className="text-xs text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>

                </div>

              </div>


              {!uploading && (
                <button
                  onClick={() =>
                    setFile(null)
                  }
                  className="rounded p-1 hover:bg-gray-100"
                >
                  <X className="h-4 w-4" />
                </button>
              )}

            </div>


            <button
              onClick={handleUpload}
              disabled={uploading}
              className="mt-4 flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >

              {uploading && (
                <Loader2 className="h-5 w-5 animate-spin" />
              )}

              {uploading
                ? "Processing document..."
                : "Upload & Process"}

            </button>

          </div>
        )}


        {error && (
          <div className="mx-auto mt-4 max-w-md rounded-lg bg-red-50 p-3 text-sm text-red-700">
            {error}
          </div>
        )}

      </div>

    </div>
  );
}