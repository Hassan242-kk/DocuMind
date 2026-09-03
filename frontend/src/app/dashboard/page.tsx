"use client";

import { useEffect, useState } from "react";
import {
  FileText,
  Database,
  MessageSquare,
  Upload,
  ArrowRight,
  Loader2,
} from "lucide-react";
import Link from "next/link";
import { getDocuments } from "@/lib/api";
import { Document } from "@/types/document";
import UploadDocument from "@/components/documents/UploadDocument";

export default function DashboardPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadDocuments() {
    try {
      const response = await getDocuments();
      setDocuments(response.documents || []);
    } catch {
      setDocuments([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDocuments();
  }, []);

  const processed = documents.filter(
    (doc) => doc.processing_status === "completed"
  ).length;

  return (
    <div className="p-6 md:p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-500">
          Welcome to your intelligent document workspace.
        </p>
      </div>

      {/* Statistics */}
      <div className="grid gap-5 md:grid-cols-3">
        <StatCard icon={FileText} title="Documents" value={documents.length} />
        <StatCard icon={Database} title="Processed" value={processed} />
        <StatCard icon={MessageSquare} title="AI Assistant" value="Ready" />
      </div>

      {/* Upload Section */}
      <div className="mt-8">
        <UploadDocument onUploaded={loadDocuments} />
      </div>

      {/* Recent Documents */}
      <div className="mt-10">
        <div className="mb-5 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900">Recent Documents</h2>
          <Link
            href="/documents"
            className="flex items-center gap-1 text-sm font-medium text-blue-600 hover:text-blue-700"
          >
            View all
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>

        {loading ? (
          <div className="flex justify-center py-10">
            <Loader2 className="h-7 w-7 animate-spin text-blue-600" />
          </div>
        ) : documents.length === 0 ? (
          <div className="rounded-2xl bg-white py-14 text-center shadow-sm border border-gray-100">
            <Upload className="mx-auto h-10 w-10 text-gray-300" />
            <p className="mt-4 font-medium text-gray-700">No documents yet</p>
            <p className="mt-1 text-sm text-gray-500">
              Upload your first document to get started.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {documents.slice(0, 5).map((doc) => (
              <Link
                key={doc.id}
                href={`/documents/${doc.id}`}
                className="flex items-center justify-between rounded-xl bg-white p-5 shadow-sm border border-gray-100 hover:shadow-md transition-all"
              >
                <div className="flex items-center gap-4">
                  <div className="rounded-lg bg-blue-50 p-3">
                    <FileText className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{doc.filename}</p>
                    <p className="mt-1 text-xs text-gray-500">
                      {doc.document_type || "Unknown"}
                    </p>
                  </div>
                </div>

                <span className="text-xs font-semibold text-green-600 bg-green-50 px-2.5 py-1 rounded-full capitalize">
                  {doc.processing_status}
                </span>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({
  icon: Icon,
  title,
  value,
}: {
  icon: React.ElementType;
  title: string;
  value: string | number;
}) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm border border-gray-100">
      <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-lg bg-blue-50">
        <Icon className="h-6 w-6 text-blue-600" />
      </div>
      <p className="text-sm font-medium text-gray-500">{title}</p>
      <p className="mt-1 text-3xl font-bold text-gray-900">{value}</p>
    </div>
  );
}