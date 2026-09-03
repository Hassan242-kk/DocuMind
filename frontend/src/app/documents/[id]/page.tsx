"use client";

import { useEffect, useState } from "react";

import Link from "next/link";
import BackButton from "@/components/ui/BackButton";
import {
  FileText,
  MessageSquare,
  Loader2,
} from "lucide-react";

import {
  getDocument,
} from "@/lib/api";

import {
  Document,
} from "@/types/document";


interface Props {
  params: Promise<{
    id: string;
  }>;
}


export default function DocumentDetails({
  params,
}: Props) {

  const [document, setDocument] =
    useState<Document | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {

    async function load() {

      try {

        const { id } = await params;

        const response =
          await getDocument(id);

        setDocument(
          response.document
        );

      } catch (error) {

        setError(
          error instanceof Error
            ? error.message
            : "Failed to load document."
        );

      } finally {

        setLoading(false);

      }
    }

    load();

  }, [params]);


  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }


  if (error || !document) {
    return (
      <div className="p-8">

        <div className="rounded-xl bg-red-50 p-6 text-red-700">
          {error || "Document not found."}
        </div>

      </div>
    );
  }


  return (
    <div className="p-6 md:p-8">

      <BackButton
        label="Back to Documents"
        fallback="/documents"
      />


      <div className="mb-8 flex flex-col justify-between gap-4 md:flex-row md:items-center">

        <div className="flex items-center gap-4">

          <div className="rounded-xl bg-blue-50 p-4">

            <FileText className="h-8 w-8 text-blue-600" />

          </div>

          <div>

            <h1 className="text-2xl font-bold">
              {document.filename}
            </h1>

            <p className="mt-1 text-sm text-gray-500">
              {document.document_type || "Unknown document"}
            </p>

          </div>

        </div>


        <Link
          href={`/chat?document=${document.id}`}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-5 py-3 font-medium text-white hover:bg-blue-700"
        >
          <MessageSquare className="h-5 w-5" />
          Chat with document
        </Link>

      </div>


      {/* Metadata */}

      <div className="grid gap-5 md:grid-cols-3">

        <div className="rounded-xl border bg-white p-5">

          <p className="text-sm text-gray-500">
            Document Type
          </p>

          <p className="mt-2 font-semibold capitalize">
            {document.document_type || "Unknown"}
          </p>

        </div>


        <div className="rounded-xl border bg-white p-5">

          <p className="text-sm text-gray-500">
            Classification Confidence
          </p>

          <p className="mt-2 font-semibold">
            {document.classification_confidence
              ? `${Math.round(
                  document.classification_confidence * 100
                )}%`
              : "N/A"}
          </p>

        </div>


        <div className="rounded-xl border bg-white p-5">

          <p className="text-sm text-gray-500">
            Status
          </p>

          <p className="mt-2 font-semibold capitalize text-green-600">
            {document.processing_status}
          </p>

        </div>

      </div>


      {/* Structured Data */}

      {document.structured_data && (
        <div className="mt-8 rounded-xl border bg-white p-6">

          <h2 className="text-xl font-semibold">
            Extracted Information
          </h2>

          <div className="mt-5 grid gap-4 md:grid-cols-2">

            {Object.entries(
              document.structured_data
            ).map(([key, value]) => (

              <div
                key={key}
                className="rounded-lg bg-gray-50 p-4"
              >

                <p className="text-xs font-medium uppercase text-gray-500">
                  {key.replaceAll("_", " ")}
                </p>

                <p className="mt-1 font-medium text-gray-900">
                  {String(value ?? "N/A")}
                </p>

              </div>

            ))}

          </div>

        </div>
      )}


      {/* Extracted Text */}

      <div className="mt-8 rounded-xl border bg-white p-6">

        <h2 className="text-xl font-semibold">
          Extracted Text
        </h2>

        <div className="mt-5 max-h-[600px] overflow-y-auto rounded-lg bg-gray-50 p-5">

          <pre className="whitespace-pre-wrap font-sans text-sm leading-7 text-gray-700">
            {document.extracted_text || "No text extracted."}
          </pre>

        </div>

      </div>

    </div>
  );
}