import Link from "next/link";

import {
  FileText,
  ArrowRight,
} from "lucide-react";

import { Document } from "@/types/document";


interface Props {
  document: Document;
}


function formatFileSize(
  bytes: number
) {
  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(
    bytes /
    (1024 * 1024)
  ).toFixed(1)} MB`;
}


export default function DocumentCard({
  document,
}: Props) {

  return (
    <Link
      href={`/documents/${document.id}`}
      className="group block rounded-xl border bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
    >

      <div className="flex items-start justify-between">

        <div className="flex items-center gap-3">

          <div className="rounded-lg bg-blue-50 p-3">

            <FileText className="h-6 w-6 text-blue-600" />

          </div>


          <div>

            <h3 className="max-w-xs truncate font-semibold text-gray-900">
              {document.filename}
            </h3>

            <p className="mt-1 text-xs text-gray-500">
              {formatFileSize(document.file_size)}
            </p>

          </div>

        </div>


        <ArrowRight className="h-5 w-5 text-gray-400 transition group-hover:translate-x-1 group-hover:text-blue-600" />

      </div>


      <div className="mt-5 flex items-center justify-between">

        <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700">
          {document.document_type || "Unknown"}
        </span>


        <span className="text-xs text-green-600">
          {document.processing_status}
        </span>

      </div>

    </Link>
  );
}