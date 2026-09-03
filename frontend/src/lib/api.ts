const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";


async function handleResponse(
  response: Response
) {
  if (!response.ok) {
    let message = "Something went wrong.";

    try {
      const error = await response.json();
      message = error.detail || message;
    } catch {
      // Ignore JSON parsing errors
    }

    throw new Error(message);
  }

  return response.json();
}


export async function uploadDocument(
  file: File
) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_URL}/api/documents/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  return handleResponse(response);
}


export async function getDocuments() {
  const response = await fetch(
    `${API_URL}/api/documents/`,
    {
      cache: "no-store",
    }
  );

  return handleResponse(response);
}


export async function getDocument(
  documentId: string
) {
  const response = await fetch(
    `${API_URL}/api/documents/${documentId}`,
    {
      cache: "no-store",
    }
  );

  return handleResponse(response);
}


export async function searchDocuments(
  query: string,
  limit = 5,
  documentId?: string
) {
  const params = new URLSearchParams();

  params.set("query", query);
  params.set("limit", String(limit));

  if (documentId) {
    params.set(
      "document_id",
      documentId
    );
  }

  const response = await fetch(
    `${API_URL}/api/search/?${params.toString()}`,
    {
      cache: "no-store",
    }
  );

  return handleResponse(response);
}


export async function chatWithDocument(
  question: string,
  documentId?: string,
  topK = 5
) {
  const response = await fetch(
    `${API_URL}/api/chat/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        question,
        document_id: documentId,
        top_k: topK,
      }),
    }
  );

  return handleResponse(response);
}