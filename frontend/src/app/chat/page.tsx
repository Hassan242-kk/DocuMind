"use client";

import {
  useEffect,
  useState,
} from "react";
import BackButton from "@/components/ui/BackButton";
import {
  useSearchParams,
} from "next/navigation";

import {
  Bot,
  User,
  Send,
  Loader2,
} from "lucide-react";

import {
  chatWithDocument,
} from "@/lib/api";

import {
  ChatResponse,
} from "@/types/document";


interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: ChatResponse["sources"];
}


export default function ChatPage() {

  const searchParams =
    useSearchParams();

  const documentId =
    searchParams.get("document");


  const [question, setQuestion] =
    useState("");

  const [messages, setMessages] =
    useState<Message[]>([]);

  const [loading, setLoading] =
    useState(false);


  async function handleSubmit(
    event: React.FormEvent
  ) {

    event.preventDefault();

    if (
      !question.trim() ||
      loading
    ) {
      return;
    }


    const currentQuestion =
      question.trim();


    setQuestion("");


    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: currentQuestion,
      },
    ]);


    try {

      setLoading(true);


      const response =
        await chatWithDocument(
          currentQuestion,
          documentId || undefined,
          5
        );


      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: response.answer,
          sources: response.sources,
        },
      ]);

    } catch (error) {

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            error instanceof Error
              ? error.message
              : "Something went wrong.",
        },
      ]);

    } finally {

      setLoading(false);

    }
  }


  return (
    <div className="flex h-screen flex-col">

      {/* Header */}

      <div className="border-b bg-white px-6 py-5">
        <BackButton label="Back to Dashboard" />
        <h1 className="text-xl font-bold">
          DocuMind AI
        </h1>

        <p className="text-sm text-gray-500">
          {documentId
            ? "Chatting with selected document"
            : "Ask questions about your documents"}
        </p>

      </div>


      {/* Messages */}

      <div className="flex-1 overflow-y-auto bg-gray-50 p-6">

        <div className="mx-auto max-w-4xl space-y-6">

          {messages.length === 0 && (

            <div className="py-20 text-center">

              <Bot className="mx-auto h-14 w-14 text-blue-600" />

              <h2 className="mt-5 text-2xl font-bold">
                Ask your documents anything
              </h2>

              <p className="mx-auto mt-2 max-w-md text-gray-500">
                DocuMind searches your documents and uses AI to answer questions using the relevant content.
              </p>

            </div>
          )}


          {messages.map(
            (message, index) => (

              <div
                key={index}
                className={`flex gap-4 ${
                  message.role === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >

                {message.role ===
                  "assistant" && (

                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-blue-100">
                    <Bot className="h-5 w-5 text-blue-600" />
                  </div>

                )}


                <div
                  className={`max-w-2xl rounded-2xl px-5 py-4 ${
                    message.role === "user"
                      ? "bg-blue-600 text-white"
                      : "border bg-white text-gray-800"
                  }`}
                >

                  <div className="flex gap-2">

                    {message.role ===
                      "user" && (
                      <User className="mt-0.5 h-5 w-5 shrink-0" />
                    )}

                    <p className="whitespace-pre-wrap text-sm leading-7">
                      {message.content}
                    </p>

                  </div>


                  {message.sources &&
                    message.sources.length > 0 && (

                    <div className="mt-4 border-t pt-3">

                      <p className="mb-2 text-xs font-semibold text-gray-500">
                        Sources
                      </p>

                      <div className="space-y-1">

                        {message.sources.map(
                          (source) => (

                            <p
                              key={
                                source.chunk_id
                              }
                              className="text-xs text-gray-500"
                            >
                              Chunk{" "}
                              {source.chunk_index + 1}
                            </p>

                          )
                        )}

                      </div>

                    </div>
                  )}

                </div>

              </div>
            )
          )}


          {loading && (

            <div className="flex gap-4">

              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-100">

                <Bot className="h-5 w-5 text-blue-600" />

              </div>

              <div className="rounded-2xl border bg-white px-5 py-4">

                <Loader2 className="h-5 w-5 animate-spin text-blue-600" />

              </div>

            </div>
          )}

        </div>

      </div>


      {/* Input */}

      <div className="border-t bg-white p-4">

        <form
          onSubmit={handleSubmit}
          className="mx-auto flex max-w-4xl gap-3"
        >

          <input
            value={question}
            onChange={(event) =>
              setQuestion(
                event.target.value
              )
            }
            placeholder="Ask something about your documents..."
            className="flex-1 rounded-xl border px-5 py-4 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />

          <button
            type="submit"
            disabled={
              loading ||
              !question.trim()
            }
            className="flex items-center justify-center rounded-xl bg-blue-600 px-6 text-white hover:bg-blue-700 disabled:opacity-50"
          >

            {loading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}

          </button>

        </form>

      </div>

    </div>
  );
}