# DocuMind

> An intelligent document processing and AI-powered document assistant that extracts, understands, classifies, searches, and answers questions about documents using OCR, embeddings, vector search, RAG, and Large Language Models.

---

## Overview

**DocuMind** is an AI-powered document intelligence platform designed to simplify the process of working with digital and scanned documents.

Instead of manually reading through large documents, users can upload files and let DocuMind automatically:

- Extract text from documents
- Perform OCR on scanned documents and images
- Classify documents by type
- Extract structured information using an LLM
- Split documents into searchable chunks
- Generate semantic embeddings
- Store embeddings in PostgreSQL using pgvector
- Perform semantic document search
- Ask questions about documents using Retrieval-Augmented Generation (RAG)
- Receive AI-generated answers based only on relevant document content

The system combines traditional document processing with modern AI techniques to create an end-to-end document intelligence pipeline.

---

## Features

### Document Upload

Users can upload multiple document formats including:

- PDF
- DOCX
- TXT
- JPG
- JPEG
- PNG

Uploaded files are stored securely using generated document IDs instead of relying on the original filename.

---

### Text Extraction

DocuMind extracts text from different document types using specialized processing methods.

| File Type | Processing |
|---|---|
| PDF | PyMuPDF |
| DOCX | python-docx |
| TXT | Native text processing |
| JPG/JPEG | PaddleOCR |
| PNG | PaddleOCR |
| Scanned PDF | PDF rendering + OCR |

For PDFs containing little or no extractable text, DocuMind automatically falls back to OCR.

---

### OCR

DocuMind supports Optical Character Recognition for scanned documents and images.

OCR is handled using:

**PaddleOCR**

This allows the system to process documents where the text is stored as an image rather than selectable digital text.

---

### Document Classification

The system automatically identifies the type of uploaded document.

Currently supported categories include:

- Invoice
- Resume
- Contract
- Report
- Receipt
- Research Paper

A classification confidence score is also generated.

---

### Structured Information Extraction

After classification, DocuMind can use an LLM to extract structured information from the document.

For example, an invoice may produce:

```json
{
  "invoice_number": "INV-1024",
  "vendor": "ABC Company",
  "invoice_date": "2026-08-20",
  "total_amount": "125000",
  "currency": "PKR"
}