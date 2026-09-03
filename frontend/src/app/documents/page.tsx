"use client";

import { useEffect, useState } from "react";
import BackButton from "@/components/ui/BackButton";

import {
  Loader2,
  FileText,
} from "lucide-react";

import {
  getDocuments,
} from "@/lib/api";

import {
  Document,
} from "@/types/document";

import DocumentCard from "@/components/documents/DocumentCard";
import UploadDocument from "@/components/documents/UploadDocument";


export default function DocumentsPage() {

  const [documents, setDocuments] =
    useState<Document[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  async function loadDocuments() {

    try {

      setLoading(true);

      const response =
        await getDocuments();

      setDocuments(
        response.documents
      );

    } catch (error) {

      setError(
        error instanceof Error
          ? error.message
          : "Failed to load documents."
      );

    } finally {

      setLoading(false);

    }
  }


  useEffect(() => {
    loadDocuments();
  }, []);


  return (
    <div className="p-6 md:p-8">
        <BackButton label="Back to Dashboard" />
      <div className="mb-8">

        <h1 className="text-3xl font-bold text-gray-900">
          Documents
        </h1>

        <p className="mt-2 text-gray-500">
          Upload, Process and Manage your documents.
        </p>

      </div>


      <UploadDocument
        onUploaded={loadDocuments}
      />


      <div className="mt-10">

        <div className="mb-5 flex items-center justify-between">

          <h2 className="text-xl font-semibold">
            Your Documents
          </h2>

          <span className="text-sm text-gray-500">
            {documents.length} documents
          </span>

        </div>


        {loading && (
          <div className="flex justify-center py-12">

            <Loader2 className="h-7 w-7 animate-spin text-blue-600" />

          </div>
        )}


        {error && (
          <div className="rounded-lg bg-red-50 p-4 text-red-700">
            {error}
          </div>
        )}


        {!loading &&
          !error &&
          documents.length === 0 && (

            <div className="rounded-xl border bg-white py-16 text-center">

              <FileText className="mx-auto h-12 w-12 text-gray-300" />

              <h3 className="mt-4 font-semibold">
                No documents yet
              </h3>

              <p className="mt-2 text-sm text-gray-500">
                Upload your first document above.
              </p>

            </div>
          )}


        {!loading &&
          documents.length > 0 && (

            <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">

              {documents.map((document) => (
                <DocumentCard
                  key={document.id}
                  document={document}
                />
              ))}

            </div>
          )}

      </div>

    </div>
  );
}