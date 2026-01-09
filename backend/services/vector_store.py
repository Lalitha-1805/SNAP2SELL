"""
Vector Store for RAG
Manages embeddings, FAISS index, and document retrieval
"""

import os
import json
import numpy as np
from typing import List, Dict, Tuple
import pickle

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    print('[WARN] sentence-transformers not available; using keyword fallback')

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False
    print('[WARN] FAISS not available; using cosine similarity')


class VectorStore:
    """
    Manages embeddings and retrieval for agriculture documents.
    Uses sentence-transformers + FAISS if available, falls back to cosine similarity.
    """
    
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.embeddings_model = None
        self.faiss_index = None
        self.documents = []
        self.embeddings = None
        self.index_path = os.path.join('data', 'faiss_index.pkl')
        self.docs_path = os.path.join('data', 'documents.json')
        self._initialized = False
        
        # LAZY INITIALIZATION: Model loads on first use only
        # This avoids slow embedding model download on startup
        print(f'[OK] VectorStore initialized (lazy mode - embeddings load on first use)')
    
    def _initialize(self):
        """Lazy initialization of embeddings model"""
        if self._initialized:
            return
        
        if HAS_SENTENCE_TRANSFORMERS:
            try:
                print(f'[...] Loading embeddings model: {self.model_name}...')
                self.embeddings_model = SentenceTransformer(self.model_name)
                print(f'[OK] Embeddings model loaded')
            except Exception as e:
                print(f'[ERROR] Failed to load embeddings model: {e}')
                self.embeddings_model = None
        
        # Try loading existing index
        self._load_index()
        self._initialized = True
    
    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store and build index"""
        # Trigger lazy initialization if needed
        if not self._initialized:
            self._initialize()
        
        self.documents = documents
        
        if not self.embeddings_model:
            print('[WARN] No embeddings model; documents stored without indexing')
            self._save_index()
            return
        
        try:
            # Extract texts for embedding
            texts = [doc.get('content', '') for doc in documents]
            
            # Generate embeddings
            self.embeddings = self.embeddings_model.encode(texts, convert_to_numpy=True)
            
            # Build FAISS index
            if HAS_FAISS:
                dimension = self.embeddings.shape[1]
                self.faiss_index = faiss.IndexFlatL2(dimension)
                self.faiss_index.add(self.embeddings.astype(np.float32))
                print(f'[OK] Built FAISS index with {len(documents)} documents')
            else:
                print(f'[OK] Indexed {len(documents)} documents (cosine similarity mode)')
            
            # Save index
            self._save_index()
        except Exception as e:
            print(f'[ERROR] Failed to build index: {e}')
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """Retrieve top-k documents most similar to query"""
        # Trigger lazy initialization if needed
        if not self._initialized:
            self._initialize()
        
        if not self.documents:
            return []
        
        if not self.embeddings_model:
            # Keyword fallback
            return self._keyword_search(query, k)
        
        try:
            # Encode query
            query_embedding = self.embeddings_model.encode([query], convert_to_numpy=True)
            
            if HAS_FAISS and self.faiss_index:
                # FAISS search
                distances, indices = self.faiss_index.search(query_embedding.astype(np.float32), k)
                results = []
                for idx, distance in zip(indices[0], distances[0]):
                    if idx >= 0 and idx < len(self.documents):
                        results.append({
                            'score': float(1 / (1 + distance)),  # Convert distance to similarity
                            **self.documents[idx]
                        })
                return results
            else:
                # Cosine similarity search
                return self._cosine_search(query_embedding, k)
        except Exception as e:
            print(f'[WARN] Search failed: {e}; falling back to keyword search')
            return self._keyword_search(query, k)
    
    def _cosine_search(self, query_embedding: np.ndarray, k: int) -> List[Dict]:
        """Retrieve using cosine similarity (fallback when FAISS unavailable)"""
        if self.embeddings is None or len(self.embeddings) == 0:
            return []
        
        # Normalize embeddings
        query_norm = query_embedding / (np.linalg.norm(query_embedding) + 1e-10)
        doc_norms = self.embeddings / (np.linalg.norm(self.embeddings, axis=1, keepdims=True) + 1e-10)
        
        # Compute cosine similarities
        similarities = np.dot(doc_norms, query_norm.T).flatten()
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:k]
        
        results = []
        for idx in top_indices:
            results.append({
                'score': float(similarities[idx]),
                **self.documents[idx]
            })
        return results
    
    def _keyword_search(self, query: str, k: int) -> List[Dict]:
        """Keyword-based fallback search"""
        query_terms = set(query.lower().split())
        scored = []
        
        for doc in self.documents:
            text = (doc.get('content', '') + ' ' + doc.get('crop', '') + ' ' + doc.get('topic', '')).lower()
            score = sum(1 for term in query_terms if term in text)
            if score > 0:
                scored.append((score, doc))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{'score': float(score), **doc} for score, doc in scored[:k]]
    
    def _save_index(self):
        """Save index and documents to disk"""
        try:
            os.makedirs('data', exist_ok=True)
            
            # Save documents
            with open(self.docs_path, 'w') as f:
                json.dump(self.documents, f)
            
            # Save embeddings
            if self.embeddings is not None:
                with open(self.index_path, 'wb') as f:
                    pickle.dump({'embeddings': self.embeddings, 'faiss_index': self.faiss_index}, f)
        except Exception as e:
            print(f'[WARN] Failed to save index: {e}')
    
    def _load_index(self):
        """Load index and documents from disk if available"""
        try:
            if os.path.exists(self.docs_path):
                with open(self.docs_path, 'r') as f:
                    self.documents = json.load(f)
            
            if os.path.exists(self.index_path) and HAS_SENTENCE_TRANSFORMERS:
                with open(self.index_path, 'rb') as f:
                    data = pickle.load(f)
                    self.embeddings = data.get('embeddings')
                    self.faiss_index = data.get('faiss_index')
                    if self.embeddings is not None:
                        print(f'[OK] Loaded cached index with {len(self.documents)} documents')
        except Exception as e:
            print(f'[WARN] Failed to load index: {e}')
