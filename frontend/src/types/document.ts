export interface Document {
  id: string;
  filename: string;
  file_type: string;
  file_size: number;

  document_type: string | null;

  classification_confidence:
    | number
    | null;

  processing_status: string;

  structured_data:
    | Record<string, unknown>
    | null;

  extracted_text?: string | null;

  created_at: string;
}


export interface DocumentsResponse {
  success: boolean;
  count: number;
  documents: Document[];
}


export interface DocumentResponse {
  success: boolean;
  document: Document;
}


export interface UploadResponse {
  success: boolean;
  message: string;
  document: Document;
  chunks_created: number;
}


export interface SearchResult {
  chunk_id: string;
  document_id: string;
  chunk_index: number;
  text: string;
}


export interface SearchResponse {
  query: string;
  results: SearchResult[];
  count: number;
}


export interface ChatResponse {
  answer: string;
  sources: SearchResult[];
}