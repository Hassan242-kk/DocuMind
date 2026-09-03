"use client";

import { useState } from "react";
import BackButton from "@/components/ui/BackButton";
import {
  Search as SearchIcon,
  Loader2,
} from "lucide-react";

import {
  searchDocuments,
} from "@/lib/api";

import {
  SearchResult,
} from "@/types/document";


export default function SearchPage() {

  const [query, setQuery] =
    useState("");

  const [results, setResults] =
    useState<SearchResult[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  async function handleSearch(
    event: React.FormEvent
  ) {

    event.preventDefault();

    if (!query.trim()) {
      return;
    }

    try {

      setLoading(true);
      setError(null);

      const response =
        await searchDocuments(
          query,
          10
        );

      setResults(
        response.results
      );

    } catch (error) {

      setError(
        error instanceof Error
          ? error.message
          : "Search failed."
      );

    } finally {

      setLoading(false);

    }
  }


  return (
    <div className="p-6 md:p-8">
        <BackButton label="Back to Dashboard" />
        <div className="mb-8">

        <h1 className="text-3xl font-bold">
          Semantic Search
        </h1>

        <p className="mt-2 text-gray-500">
          Search your documents using natural language.
        </p>

      </div>


      <form
        onSubmit={handleSearch}
        className="flex gap-3"
      >

        <div className="relative flex-1">

          <SearchIcon className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />

          <input
            value={query}
            onChange={(event) =>
              setQuery(event.target.value)
            }
            placeholder="e.g. What is the invoice total?"
            className="w-full rounded-xl border bg-white py-4 pl-12 pr-4 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />

        </div>


        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-blue-600 px-6 font-medium text-white hover:bg-blue-700 disabled:opacity-60"
        >
          {loading ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : (
            "Search"
          )}
        </button>

      </form>


      {error && (
        <div className="mt-6 rounded-lg bg-red-50 p-4 text-red-700">
          {error}
        </div>
      )}


      <div className="mt-8 space-y-4">

        {results.map((result) => (

          <div
            key={result.chunk_id}
            className="rounded-xl border bg-white p-6 shadow-sm"
          >

            <div className="mb-3 flex items-center justify-between">

              <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700">
                Chunk {result.chunk_index + 1}
              </span>

              <span className="text-xs text-gray-400">
                {result.document_id}
              </span>

            </div>

            <p className="whitespace-pre-wrap text-sm leading-7 text-gray-700">
              {result.text}
            </p>

          </div>

        ))}


        {!loading &&
          query &&
          results.length === 0 && (

            <div className="py-16 text-center text-gray-500">
              No relevant information found.
            </div>

          )}

      </div>

    </div>
  );
}