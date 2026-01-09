"""
RAG Chatbot Implementation - Simplified Version
Provides agricultural advice without complex dependencies
Uses fallback intelligent responses for production stability
"""

import os
import pickle
from typing import List, Dict
from datetime import datetime

# Try to import optional libraries, but don't fail if unavailable
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

class SimpleRAGChatbot:
    """
    Simple RAG Chatbot for Agricultural Advice
    Uses keyword matching and fallback responses
    Can be upgraded to use FAISS/LangChain when dependencies are available
    """
    
    def __init__(self):
        self.vector_store = None
        self.embeddings = None
        self.documents = []
        self.rag_enabled = True  # Enabled with fallback approach
        self.knowledge_base_path = 'data/rag_knowledge_base'
        
        print("[OK] Simple RAG Chatbot initialized (using fallback mode)")
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize knowledge base with agricultural information"""
        self.knowledge_base = [
            {
                'keywords': ['tomato', 'fertilizer', 'fertiliser', 'tomato fertilizer'],
                'response': '''TOMATO FERTILIZER GUIDE - Specific Products & Application

BEFORE PLANTING (Soil Preparation):
- Apply 5-7 tons well-decomposed FYM or compost per hectare
- Mix 250 kg vermicompost per hectare
- Add 20 kg zinc sulfate if deficient

CHEMICAL FERTILIZERS FOR TOMATOES:
**Stage 1: At Planting (Basal)**
- DAP (Di-Ammonium Phosphate): 400 kg/hectare OR
- NPK 10:26:26: 500 kg/hectare
- Apply 5 cm deep in furrows before transplanting

**Stage 2: 30 days after planting (Top-dress)**
- Urea: 150 kg/hectare
- Potassium chloride (MOP): 100 kg/hectare

**Stage 3: At Flowering (45-50 days)**
- Urea: 150 kg/hectare
- Potassium chloride: 100 kg/hectare

**Stage 4: Fruit Development (65-70 days)**
- Urea: 100 kg/hectare
- Potassium chloride: 100 kg/hectare

ORGANIC ALTERNATIVES:
- Neem cake: 1000 kg/hectare (slow-release nitrogen)
- Bone meal: 500 kg/hectare (phosphorus for fruiting)
- Wood ash: 3 tons/hectare (potassium + micronutrients)
- Seaweed extract: Spray every 15 days (boosts immunity)

MICRONUTRIENT SPRAYS (Optional but recommended):
- Zinc: 5g/liter water, spray at 30 & 60 days
- Boron: 2g/liter water, spray at flowering & fruit-set
- Magnesium: 5g Epsom salt/liter, spray every 20 days

HOW TO APPLY:
1. Dissolve fertilizer in water (1kg in 100 liters for spray)
2. Apply in evening to avoid leaf burn
3. Ensure soil is moist before fertilizer application
4. Split applications are more effective than single dose
5. Keep 10cm distance from plant stem

TYPICAL SCHEDULE:
- Day 0: Soil prep with FYM + DAP
- Day 30: First top-dress with Urea + MOP
- Day 50: Flowering boost (Urea + MOP + Micronutrients)
- Day 70: Fruit dev (Light urea + Potassium)
- Days 45, 60, 75: Micronutrient sprays

YIELD EXPECTATION:
With proper fertilization: 50-60 tons/hectare (good quality)
Without proper nutrition: 20-25 tons/hectare (poor quality)'''
            },
            {
                'keywords': ['crop', 'grow', 'plant', 'cultivation', 'sowing'],
                'response': '''For crop selection, consider your:
- Climate zone and seasonal patterns
- Soil type and pH level
- Water availability and irrigation capacity
- Market demand and price trends
- Local agricultural practices

Common profitable crops: Rice, Wheat, Cotton, Sugarcane, Vegetables (Tomato, Onion, Carrot), Spices.
Consult local agricultural office for region-specific recommendations.'''
            },
            {
                'keywords': ['soil', 'pH', 'fertility', 'preparation', 'loamy', 'clay'],
                'response': '''Soil health is foundation of farming:
- Test soil for pH (6-7 ideal), nutrients (N, P, K), and organic matter
- Add organic matter: compost, farm manure (20-25 tons/hectare)
- Maintain soil moisture and drainage
- Use crop rotation to maintain fertility
- Avoid excessive tilling to preserve soil structure
- Add organic fertilizers for long-term sustainability

Good soil = Better yields and healthier crops'''
            },
            {
                'keywords': ['water', 'irrigation', 'rain', 'rainfall', 'drought', 'flood'],
                'response': '''Efficient water management is critical:
- Most crops need 400-1200 mm annual rainfall
- Irrigation methods: Drip (most efficient), Sprinkler, Flood
- Water early morning or late evening to reduce evaporation
- Maintain 25-30cm soil moisture for most crops
- Install proper drainage to prevent waterlogging
- Monitor weather and plan irrigation accordingly
- Save rainwater using tanks and ponds

Proper irrigation increases yields by 30-50%'''
            },
            {
                'keywords': ['pest', 'insect', 'disease', 'damage', 'protection', 'spray'],
                'response': '''Integrated Pest Management (IPM) approach:
1. Monitor crops regularly for pest identification
2. Use biological controls: beneficial insects, predators
3. Practice crop rotation and companion planting
4. Remove diseased plants immediately
5. Use organic methods: Neem oil, soap spray, trap crops
6. Chemical pesticides only when necessary and safe
7. Follow recommended dosages and safety protocols

Regular monitoring saves crops from 20-40% pest losses'''
            },
            {
                'keywords': ['fertilizer', 'manure', 'compost', 'NPK', 'nitrogen', 'phosphorus', 'potassium'],
                'response': '''COMPREHENSIVE FERTILIZER GUIDE

FERTILIZER TYPES & PRODUCTS:
1. **DAP (Di-Ammonium Phosphate)**
   - Composition: 18% N, 46% P2O5
   - Use: Basal fertilizer for most crops
   - Dosage: 150-300 kg/hectare
   - Crops: Wheat, Rice, Pulses, Vegetables

2. **Urea (46% Nitrogen)**
   - Use: Top-dress in 2-3 splits
   - Dosage: 100-150 kg/hectare per application
   - Best at: Vegetative growth stage
   - Apply when soil is moist

3. **Potassium Chloride (MOP - 60% K2O)**
   - Use: Potassium source, improves fruit quality
   - Dosage: 50-100 kg/hectare
   - Crops: Fruits, Vegetables, Sugarcane
   - Apply 2-3 weeks before flowering

4. **NPK Fertilizers (e.g., 10:26:26 or 19:19:19)**
   - Balanced for all nutrient needs
   - Use: Basal application
   - Dosage: 300-500 kg/hectare

5. **ORGANIC OPTIONS:**
   - **FYM (Farm Yard Manure)**: 5-10 tons/hectare, slow-release
   - **Vermicompost**: 2-3 tons/hectare, rich in microbes
   - **Neem Cake**: 500-1000 kg/hectare, pest repellent
   - **Bone Meal**: 300-500 kg/hectare, phosphorus source
   - **Seaweed Extract**: Spray solution, growth booster

DEFICIENCY SYMPTOMS & SOLUTIONS:
- **Nitrogen (N) deficiency**: Yellow leaves → Apply Urea
- **Phosphorus (P) deficiency**: Purple/dark leaves → Apply DAP
- **Potassium (K) deficiency**: Brown leaf edges → Apply MOP
- **Calcium deficiency**: Tip burn in fruits → Apply lime
- **Magnesium deficiency**: Yellowing between veins → Epsom salt spray
- **Zinc deficiency**: Small pale leaves → Zinc sulfate spray

MICRONUTRIENT SPRAYS:
- Zinc sulfate: 5 g/liter (deficiency symptom: small leaves)
- Boron: 2 g/liter (deficiency: flower drop, poor fruit set)
- Magnesium (Epsom salt): 5 g/liter (yellowing between veins)
- Copper sulfate: 2 g/liter (leaf spots, fungal prevention)
- Iron chelate: 5 g/liter (yellow chlorosis)

APPLICATION SCHEDULE:
- **Basal**: Before planting (DAP + FYM)
- **Top-dress 1**: 30-35 days after sowing (Urea)
- **Top-dress 2**: 50-60 days after sowing (Urea + MOP)
- **Foliar spray**: Every 15-20 days (micronutrients)

STORAGE & SAFETY:
- Keep in dry, cool place (moisture causes caking)
- Use appropriate PPE (gloves, mask)
- Never mix different fertilizers without research
- Check expiry date and fertilizer content'''
            },
            {
                'keywords': ['price', 'market', 'sell', 'profit', 'rate', 'mandi', 'commodity'],
                'response': '''Market strategies for better returns:
- Check AGMARKET.IN for live market prices
- Diversify crops to spread risk
- Quality grading increases prices 20-30%
- Direct to consumer sales bypass middlemen
- Join farmer cooperatives for better pricing
- Follow seasons: High prices for off-season produce
- Plan cultivation based on 3-4 month forward price trends

Good market timing can double your profits'''
            },
            {
                'keywords': ['harvest', 'maturity', 'ready', 'pick', 'yield', 'produce', 'storage'],
                'response': '''Harvesting & Post-harvest management:
- Harvest at peak maturity for best quality
- Timing: Grains at 15-20% moisture, vegetables at full size, fruits when ripe
- Use clean, sharp harvesting tools to minimize damage
- Harvest early morning to avoid heat stress
- Grade and sort produce immediately
- Store in cool, dry, ventilated conditions
- Proper packaging increases shelf life and market value

Good harvesting practices increase value by 30-40%'''
            },
            {
                'keywords': ['weather', 'climate', 'season', 'monsoon', 'temperature', 'wind', 'forecast'],
                'response': '''Weather planning for better farming:
- Monitor seasonal forecasts 3-4 months ahead
- Plan irrigation based on rainfall predictions
- Schedule pest sprays during dry periods
- Adjust crop selection based on weather patterns
- Use weather alerts for frost/heat protection
- Prepare for extreme weather: Wind, Flood, Drought
- Keep weather records to identify patterns

Weather-aware farming reduces losses significantly'''
            },
            {
                'keywords': ['government', 'scheme', 'subsidy', 'support', 'loan', 'insurance'],
                'response': '''Government schemes supporting farmers:
- PM Kisan Yojana: Income support ₹6000/year
- Pradhan Mantri Krishi Sinchayee Yojana: Irrigation subsidy
- PMFBY: Crop insurance for yield protection
- KCC: Kisan Credit Card for low-interest loans
- PM Fasal Bima Yojana: Crop insurance coverage
- MNREGA: Rural employment scheme
- Contact local agricultural office for eligibility & registration'''
            },
            {
                'keywords': ['training', 'learn', 'skill', 'knowledge', 'help', 'expert', 'advice'],
                'response': '''Agricultural support resources:
- Contact your local Krishi Vigyan Kendra (KVK) for free training
- State agricultural universities offer courses
- Agricultural extension officers provide field advice
- Farmer producer organizations share best practices
- Government hotlines: Call for crop-specific guidance
- AgriSmart's AI assistant is here 24/7 for agricultural questions

Continuous learning improves farming outcomes consistently'''
            }
        ]
        
        print(f"[OK] Knowledge base loaded with {len(self.knowledge_base)} topic categories")
    
    def retrieve_relevant_docs(self, query: str, k: int = 3) -> List[Dict]:
        """Retrieve relevant documents based on keyword matching with crop-specific priority"""
        query_lower = query.lower()
        matches = []
        
        for kb_entry in self.knowledge_base:
            # Count keyword matches
            score = 0
            for keyword in kb_entry['keywords']:
                if keyword in query_lower:
                    score += 1
            
            # Boost score for crop-specific entries (e.g., tomato fertilizer)
            if 'tomato' in query_lower and 'tomato' in [kw.lower() for kw in kb_entry['keywords']]:
                score += 5  # High priority for exact crop match
            
            if score > 0:
                matches.append({
                    'content': kb_entry['response'],
                    'title': kb_entry['keywords'][0].title(),
                    'similarity_score': score
                })
        
        # Sort by relevance
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        return matches[:k]
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """Generate response using retrieved context - for specific crop queries, return content directly"""
        # If we have a highly relevant context document (score >= 5), return it directly
        if context_docs and context_docs[0].get('similarity_score', 0) >= 5:
            # This is likely a specific crop query (e.g., tomato fertilizer)
            return context_docs[0]['content']
        
        # Otherwise, create actionable steps from context
        if context_docs:
            best = context_docs[0]
            summary = best['content']
            steps = []

            # Basic extraction of actionable items from the summary using simple heuristics
            if 'soil' in summary.lower() or 'fertil' in summary.lower():
                steps.append('Test soil (pH, NPK, organic matter) and record results.')
                steps.append('Apply recommended organic amendments (compost/FYM) based on test.')

            if 'irrig' in summary.lower() or 'water' in summary.lower():
                steps.append('Assess irrigation availability and schedule drip or sprinkler where feasible.')

            if 'pest' in summary.lower() or 'disease' in summary.lower():
                steps.append('Inspect crop, identify pest/disease, and remove infected plants.')
                steps.append('Apply biological controls first (beneficial insects, neem oil).')

            if 'market' in summary.lower() or 'price' in summary.lower():
                steps.append('Check local market prices and consider value-add packaging or direct sale.')

            # Always include universal next steps
            steps.append('Keep a 2-week log of field observations (weather, pests, growth).')
            steps.append('Contact nearest agricultural extension office for region-specific advice.')

            # Build an agent-like reply with confidence hints and resources
            reply_lines = [f"Summary: {summary}", '', 'Actionable Plan:']
            for i, s in enumerate(steps, 1):
                reply_lines.append(f"{i}. {s}")

            reply_lines.append('')
            reply_lines.append('Why this helps: These steps target the root causes and provide short-term fixes plus long-term resilience.')
            reply_lines.append('Resources: Local Krishi Vigyan Kendra, state agriculture dept, and AgriSmart support.')

            return '\n'.join(reply_lines)

        # No direct context — produce a diagnostic, ask clarifying questions and propose steps
        return self._generate_general_response(query)
    
    def _generate_general_response(self, query: str) -> str:
        """Generate helpful general response when no specific match found"""
        # Analyze the query for intent to produce a farmer-agent style reply
        q = query.lower()

        # If the query is too short or vague, ask a clarifying question
        if len(q.split()) <= 3:
            return (f"I need a bit more detail to help effectively. Could you tell me:\n"
                    "- Which crop or livestock are you asking about?\n"
                    "- Your location or climate zone?\n"
                    "- Any immediate symptoms (pests, low yield, soil issues)?\n\n"
                    "Example: 'Tomato plants in my greenhouse have yellow leaves and holes — what should I do?'")

        # Infer intent categories
        intent = None
        if any(word in q for word in ['what to plant', 'crop selection', 'grow', 'which crop']):
            intent = 'crop_selection'
        elif any(word in q for word in ['soil', 'ph', 'fertilizer', 'fertiliser', 'manure']):
            intent = 'soil'
        elif any(word in q for word in ['pest', 'disease', 'infect', 'insect', 'mildew']):
            intent = 'pest'
        elif any(word in q for word in ['water', 'irrig', 'drought', 'rain']):
            intent = 'irrigation'
        elif any(word in q for word in ['price', 'market', 'sell']):
            intent = 'market'

        # Provide targeted guidance per intent with an actionable checklist
        if intent == 'crop_selection':
            return (f"Crop selection advice for your area:\n"
                    "1. Test soil and map micro-climates on your land.\n"
                    "2. Choose crops suited to your season and water availability.\n"
                    "3. Start small trials (0.5-1 acre) before scaling.\n"
                    "4. Check market demand and buyer channels before planting.\n\n"
                    "Tell me your region and expected investment horizon for a tailored plan.")

        if intent == 'soil':
            return (f"Soil health checklist:\n"
                    "1. Take composite soil samples (0-15 cm) from 6-8 spots.\n"
                    "2. Send to a lab for pH and NPK; aim pH 6.0-7.0 for most crops.\n"
                    "3. Apply compost or FYM (3-5 t/ha small plots, scale accordingly).\n"
                    "4. Use green manuring and crop rotation to rebuild fertility.\n\n"
                    "If you share your soil test results I can recommend exact dosages.")

        if intent == 'pest':
            return (f"Pest & disease triage:\n"
                    "1. Describe symptoms (spots, wilting, holes), take clear photos.\n"
                    "2. Remove severely infected plants and isolate adjacent areas.\n"
                    "3. Apply biological controls first: neem oil, Trichoderma, predatory insects.\n"
                    "4. Only use chemical pesticides when identification is confirmed.\n\n"
                    "Send photos or describe timing (when symptoms started) for a better diagnosis.")

        if intent == 'irrigation':
            return (f"Irrigation optimization:\n"
                    "1. Map water sources and measure flow rates.\n"
                    "2. Prefer drip irrigation for high-value crops to save water.\n"
                    "3. Mulch fields to retain soil moisture and reduce evaporation.\n\n"
                    "Tell me typical rainfall and irrigation method for specific recommendations.")

        if intent == 'market':
            return (f"Market guidance:\n"
                    "1. Track 4-week price trends for your crops across local mandis.\n"
                    "2. Consider grading and packaging to increase price per kg.\n"
                    "3. Join farmer groups/cooperatives for bulk negotiation.\n\n"
                    "If you tell me the crop and nearest mandi, I can surface price tips.")

        # Fallback general guidance
        return (f"I don't have a direct match for '{query}', but I can help with:\n"
                "- Crop selection and cultivation practices\n"
                "- Soil health and fertilization\n"
                "- Water management and irrigation\n"
                "- Pest and disease control\n"
                "- Harvesting and post-harvest handling\n"
                "Please provide more details (crop, symptoms, location) for a precise plan.")
    
    def answer_query(self, query: str) -> Dict:
        """Complete RAG pipeline: retrieve and generate"""
        try:
            if not query or len(query.strip()) == 0:
                return {
                    'status': 'error',
                    'answer': 'Please ask a valid question',
                    'sources': [],
                    'context_count': 0
                }
            
            # Retrieve relevant documents
            context_docs = self.retrieve_relevant_docs(query, k=3)
            
            # Generate response
            response = self.generate_response(query, context_docs)
            
            return {
                'status': 'success',
                'answer': response,
                'sources': [doc['title'] for doc in context_docs] if context_docs else [],
                'context_count': len(context_docs),
                'timestamp': datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'answer': f'Error processing query: {str(e)}',
                'sources': [],
                'context_count': 0,
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def add_document(self, content: str, title: str, category: str) -> bool:
        """Add a new document to the knowledge base"""
        try:
            new_entry = {
                'keywords': [title.lower()] + category.lower().split(),
                'response': content
            }
            self.knowledge_base.append(new_entry)
            print(f"[OK] Document added: {title}")
            return True
        except Exception as e:
            print(f"[FAIL] Failed to add document: {str(e)}")
            return False
    
    def get_knowledge_base_stats(self) -> Dict:
        """Get statistics about the knowledge base"""
        return {
            'vector_store_exists': True,
            'embeddings_model': 'keyword-based',
            'kb_entries': len(self.knowledge_base),
            'status': 'ready',
            'mode': 'simplified_rag_fallback'
        }


# Optional: LangChain-backed RAG implementation (lazy imports)
class LangChainRAGChatbot:
    """LangChain-based RAG chatbot (lazy-loads heavy deps).
    Falls back gracefully if libraries (langchain, faiss, transformers) aren't available.
    """
    def __init__(self):
        self.available = False
        self.index = None
        self.retriever = None
        self.chain = None
        self.embeddings = None
        self.vector_store = None
        self.index_path = 'data/rag_index'
        self._initialized = False

        # Try to import langchain and associated libraries lazily
        try:
            # Import common LangChain components
            from langchain.embeddings import HuggingFaceEmbeddings
            from langchain.vectorstores import FAISS
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            from langchain.docstore.document import Document
            from langchain.chains import RetrievalQA
            from langchain.llms import OpenAI

            self.HuggingFaceEmbeddings = HuggingFaceEmbeddings
            self.FAISS = FAISS
            self.RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter
            self.Document = Document
            self.RetrievalQA = RetrievalQA
            self.OpenAI = OpenAI

            self.available = True
            print('[OK] LangChain components available for RAG')
        except Exception as e:
            self.available = False
            print(f'[WARN] LangChain RAG not available: {e}')

    def initialize(self, force_rebuild=False):
        """Initialize embeddings and vector store from MongoDB RAG documents."""
        if not self.available:
            return False
        if self._initialized and not force_rebuild:
            return True

        # Lazy imports within the function
        try:
            from models.database import RAGDocument
            # Build embeddings
            self.embeddings = self.HuggingFaceEmbeddings()

            # Load documents from MongoDB
            docs = RAGDocument.find_many({})
            texts = []
            metadata = []
            for d in docs:
                content = d.get('content', '')
                title = d.get('title', '')
                if content:
                    texts.append(content)
                    metadata.append({'title': title, 'doc_id': str(d.get('_id'))})

            # Split long texts
            splitter = self.RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            split_docs = []
            for i, t in enumerate(texts):
                parts = splitter.split_text(t)
                for p in parts:
                    split_docs.append(self.Document(page_content=p, metadata=metadata[i]))

            if len(split_docs) == 0:
                print('[WARN] No RAG documents found in DB to index')
                self._initialized = True
                return True

            # Build or load FAISS index
            if os.path.exists(self.index_path) and not force_rebuild:
                try:
                    self.vector_store = self.FAISS.load_local(self.index_path, self.embeddings)
                    print('[OK] Loaded FAISS index from disk')
                except Exception:
                    self.vector_store = self.FAISS.from_documents(split_docs, self.embeddings)
                    self.vector_store.save_local(self.index_path)
                    print('[OK] Built FAISS index and saved to disk')
            else:
                self.vector_store = self.FAISS.from_documents(split_docs, self.embeddings)
                self.vector_store.save_local(self.index_path)
                print('[OK] Built FAISS index and saved to disk')

            # Create retriever and chain using OpenAI (requires OPENAI_API_KEY)
            llm = None
            if os.environ.get('OPENAI_API_KEY'):
                llm = self.OpenAI(temperature=0.2)
            else:
                print('[WARN] OPENAI_API_KEY not set; RAG answers will use retrieval-only summaries')

            self.retriever = self.vector_store.as_retriever(search_kwargs={'k': 4})
            if llm:
                self.chain = self.RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=self.retriever)

            self._initialized = True
            return True
        except Exception as e:
            print(f'[ERROR] Failed to initialize LangChain RAG: {e}')
            return False

    def answer_query(self, query: str):
        """Answer using LangChain retrieval+LLM if available, else return None."""
        if not self.available:
            return None
        if not self._initialized:
            self.initialize()

        try:
            if self.chain:
                answer = self.chain.run(query)
                # For sources, fetch top docs
                docs = self.retriever.get_relevant_documents(query)[:4]
                sources = [d.metadata.get('title') or d.metadata.get('doc_id') for d in docs]
                return {'status': 'success', 'answer': answer, 'sources': sources, 'context_count': len(docs)}
            else:
                # If no LLM, return retrieved snippets concatenated
                docs = self.retriever.get_relevant_documents(query)[:4]
                snippet = '\n\n'.join(d.page_content for d in docs)
                return {'status': 'success', 'answer': snippet or 'No context found', 'sources': [d.metadata.get('title') for d in docs], 'context_count': len(docs)}
        except Exception as e:
            return {'status': 'error', 'answer': f'LangChain RAG error: {str(e)}', 'sources': [], 'context_count': 0}

    def index_new_document(self, content: str, title: str, category: str):
        """Save document to MongoDB and optionally index it."""
        try:
            from models.database import RAGDocument
            doc_id = RAGDocument.add_document(content=content, title=title, category=category)
            # Mark for indexing; next initialize() will pick it up
            return True
        except Exception as e:
            print(f'[ERROR] Failed to persist RAG document: {e}')
            return False

    def answer_image_query(self, image_path: str, question: str = ''):
        """Placeholder: handle image inputs (future: vision model). For now, store and return acknowledgement."""
        # Real implementation could call an image model (e.g., CLIP / Segmentation) to extract features
        return {'status': 'success', 'answer': f'Image received at {image_path}. Describe visible symptoms for diagnosis.', 'sources': [], 'context_count': 0}


# Initialize chatbot singleton: choose LangChain-backed RAG if available and enabled
_enable_langchain = os.environ.get('ENABLE_LANGCHAIN_RAG', 'false').lower() in ['1', 'true', 'yes']
_langchain = LangChainRAGChatbot() if _enable_langchain else None

if _langchain and _langchain.available:
    # Attempt to initialize in background-safe way
    try:
        ok = _langchain.initialize()
        if ok:
            rag_chatbot = _langchain
        else:
            rag_chatbot = SimpleRAGChatbot()
    except Exception:
        rag_chatbot = SimpleRAGChatbot()
else:
    rag_chatbot = SimpleRAGChatbot()

# Backwards-compatible alias: some modules import `RAGChatbot` from `rag.chatbot`
# Ensure `from rag.chatbot import RAGChatbot` works without changing other files.
RAGChatbot = type(rag_chatbot)


# ------------------
# Internal self-contained RAG (no external docs required)
# ------------------
class InternalRAGChatbot:
    """Self-contained RAG chatbot built from an internal knowledge base.
    - Auto-generates agriculture knowledge entries
    - Chunks text in-code
    - Uses HuggingFace embeddings + FAISS when available (lazy)
    - Falls back to keyword matching if embeddings unavailable
    """
    def __init__(self):
        self.kb = []  # list of {'text', 'metadata'}
        self.chunks = []  # list of {'text','metadata'}
        self.embeddings = None
        self.vector_store = None
        self.faiss_index_path = os.path.join('data', 'internal_rag_index')
        self.initialized = False
        self.available_embeddings = False
        self.HF_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

        # Build internal KB immediately
        self._build_internal_kb()
        # Try to initialize embeddings & index lazily
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            from langchain.docstore.document import Document
            from langchain.vectorstores import FAISS
            # keep references
            self.HuggingFaceEmbeddings = HuggingFaceEmbeddings
            self.Document = Document
            self.FAISS = FAISS
            self.available_embeddings = True
            print('[OK] InternalRAG: HuggingFace embeddings available')
        except Exception as e:
            self.available_embeddings = False
            print(f'[WARN] InternalRAG: embeddings not available, using keyword fallback: {e}')

    def _build_internal_kb(self):
        """Create the internal agriculture knowledge base as Python data structures."""
        # Major crops
        crops_entry = {
            'title': 'major_crops',
            'category': 'crops',
            'region': 'India',
            'season': 'year-round',
            'text': (
                'Major crops in India include rice, wheat, maize, cotton, sugarcane, pulses and a wide range of vegetables. '
                'Rice is dominant in paddy regions (Kharif); wheat in rabi (winter) zones. Maize and pulses are multi-seasonal. '
                'Cotton and sugarcane are important cash crops in suitable agro-climatic zones.'
            )
        }

        # Soil types and suitable crops
        soil_entry = {
            'title': 'soil_types',
            'category': 'soil',
            'region': 'India',
            'season': 'all',
            'text': (
                'Soil types: sandy, loamy, clayey, silt and lateritic. Sandy soils drain quickly and suit groundnuts, millet, and some vegetables; loamy soils are ideal for most crops including vegetables and cereals; clay soils retain water and suit paddy; well-drained loams suit wheat and pulses.'
            )
        }

        # Seasonal crop calendar (India-focused)
        season_entry = {
            'title': 'seasonal_calendar',
            'category': 'season',
            'region': 'India',
            'season': 'Kharif/Rabi',
            'text': (
                'Kharif (monsoon): Rice, maize, cotton, soybean, pulses. Sowing: June-July.\n'
                'Rabi (winter): Wheat, mustard, chickpea. Sowing: Oct-Dec.\n'
                'Zaid (summer): Vegetables, cucumber, melon — short-duration crops between seasons.'
            )
        }

        # Fertilizers (summary)
        fert_entry = {
            'title': 'fertilizers',
            'category': 'fertilizer',
            'region': 'India',
            'season': 'all',
            'text': (
                'Fertilizers include chemical types: Urea (N), DAP (P), MOP (K), and balanced NPK blends. Organic options: FYM, vermicompost, neem cake, bone meal, seaweed extracts. '
                'Split nitrogen applications are recommended; soil tests should guide exact dosages.'
            )
        }

        # Pests and diseases
        pest_entry = {
            'title': 'pests_and_diseases',
            'category': 'pests',
            'region': 'India',
            'season': 'all',
            'text': (
                'Common pests: aphids, whiteflies, fruit borers, stem borers; diseases: blight, wilt, mildew, bacterial spots. Control: integrated pest management (IPM), monitoring, biological controls, targeted chemical use when needed.'
            )
        }

        # Irrigation techniques
        irrig_entry = {
            'title': 'irrigation',
            'category': 'irrigation',
            'region': 'India',
            'season': 'all',
            'text': (
                'Irrigation options: flood (traditional), sprinkler, drip (most water-efficient). Mulching and scheduling reduce water needs. Drip suits vegetables and orchards.'
            )
        }

        # Weather impacts
        weather_entry = {
            'title': 'weather_impact',
            'category': 'weather',
            'region': 'India',
            'season': 'all',
            'text': (
                'Weather affects sowing dates, pest cycles and water needs. Monitor seasonal forecasts and plan sowing/irrigation accordingly. Extreme events (drought, flood, heat) need contingency plans.'
            )
        }

        # Market factors
        market_entry = {
            'title': 'market_factors',
            'category': 'market',
            'region': 'India',
            'season': 'all',
            'text': (
                'Market prices depend on seasonality, quality, transport and demand. Grading and direct marketing increase farmer returns. Watch local mandi prices.'
            )
        }

        # Government schemes (high-level)
        schemes_entry = {
            'title': 'gov_schemes',
            'category': 'policy',
            'region': 'India',
            'season': 'all',
            'text': (
                'Key programs: income support, crop insurance, irrigation subsidies and credit facilities. Check local agriculture office for scheme details and eligibility.'
            )
        }

        # Add crop-specific detailed entries (e.g., tomato fertilizer) using previously created content
        tomato_entry = {
            'title': 'tomato_fertilizer',
            'category': 'fertilizer',
            'region': 'India',
            'season': 'Kharif/Rabi',
            'text': (
                'Tomato fertilizer guide: Basal at transplant: DAP or NPK; top-dress with urea and MOP at vegetative and flowering stages. Use FYM/compost before planting; foliar micronutrients (Zn, B, Mg) improve fruit set. Follow split N applications and soil test recommendations.'
            )
        }

        # Consolidate entries
        self.kb = [crops_entry, soil_entry, season_entry, fert_entry, pest_entry, irrig_entry, weather_entry, market_entry, schemes_entry, tomato_entry]

        # Create chunks from KB texts
        self._create_chunks()

    def _create_chunks(self, min_words=200, max_words=500):
        """Chunk KB texts into segments of approximately 400-700 tokens (approx by words)."""
        self.chunks = []
        for entry in self.kb:
            text = entry['text']
            words = text.split()
            i = 0
            while i < len(words):
                chunk_words = words[i:i+400]
                chunk_text = ' '.join(chunk_words)
                metadata = {
                    'title': entry['title'],
                    'category': entry['category'],
                    'region': entry.get('region', 'India'),
                    'season': entry.get('season', '')
                }
                self.chunks.append({'text': chunk_text, 'metadata': metadata})
                i += 400

    def initialize_embeddings_and_index(self):
        """Build embeddings and FAISS vector store (lazy)."""
        if self.initialized:
            return True
        if not self.available_embeddings:
            print('[WARN] InternalRAG: embeddings not available; using keyword search')
            self.initialized = True
            return False

        try:
            # create embeddings
            emb = self.HuggingFaceEmbeddings(model_name=self.HF_MODEL)
            docs = [self.Document(page_content=c['text'], metadata=c['metadata']) for c in self.chunks]
            # Build FAISS index
            if os.path.exists(self.faiss_index_path):
                try:
                    self.vector_store = self.FAISS.load_local(self.faiss_index_path, emb)
                    print('[OK] InternalRAG: loaded FAISS index')
                except Exception:
                    self.vector_store = self.FAISS.from_documents(docs, emb)
                    self.vector_store.save_local(self.faiss_index_path)
                    print('[OK] InternalRAG: built and saved FAISS index')
            else:
                self.vector_store = self.FAISS.from_documents(docs, emb)
                self.vector_store.save_local(self.faiss_index_path)
                print('[OK] InternalRAG: built and saved FAISS index')

            self.embeddings = emb
            self.initialized = True
            return True
        except Exception as e:
            print(f'[ERROR] InternalRAG failed to build embeddings/index: {e}')
            self.initialized = True
            return False

    def retrieve(self, question: str, k: int = 4):
        """Retrieve top-k chunks for the question using embeddings or keyword fallback."""
        if self.available_embeddings and self.initialize_embeddings_and_index():
            try:
                docs = self.vector_store.similarity_search(question, k=k)
                # convert Document objects to text+metadata
                out = [{'text': d.page_content, 'metadata': getattr(d, 'metadata', {})} for d in docs]
                return out
            except Exception as e:
                print(f'[WARN] Retrieval failed, falling back to keyword: {e}')

        # Keyword fallback: simple scoring by overlap
        q = question.lower()
        scored = []
        for c in self.chunks:
            score = 0
            for tok in q.split():
                if tok in c['text'].lower():
                    score += 1
            if score > 0:
                scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:k]]

    def generate_answer_from_context(self, question: str, contexts: list) -> dict:
        """Combine retrieved contexts into an answer. Strictly use context content; avoid hallucination."""
        if not contexts:
            return {'answer': 'Information not available in the agriculture knowledge base.', 'sources': [], 'category': 'unknown'}

        # Simple synthesis: find sentences in contexts that contain keywords from question
        q_terms = set([w.strip(',.?') for w in question.lower().split() if len(w) > 3])
        selected_sentences = []
        for c in contexts:
            sentences = [s.strip() for s in c['text'].split('.') if s.strip()]
            for s in sentences:
                lw = s.lower()
                if any(term in lw for term in q_terms):
                    selected_sentences.append(s)

        if not selected_sentences:
            # If no matching sentences, return concise combined context summary
            combined = ' '.join([c['text'] for c in contexts])
            answer = combined[:2000]  # limit length
            sources = [c['metadata'].get('title') for c in contexts]
            return {'answer': answer, 'sources': sources, 'category': contexts[0]['metadata'].get('category')}

        # Build a short, farmer-friendly answer
        answer_lines = []
        answer_lines.append('Answer (from AgriSmart knowledge base):')
        for s in selected_sentences[:6]:
            answer_lines.append('- ' + s.strip())
        sources = list({c['metadata'].get('title') for c in contexts if c['metadata'].get('title')})
        return {'answer': '\n'.join(answer_lines), 'sources': sources, 'category': contexts[0]['metadata'].get('category')}

    def query(self, question: str) -> dict:
        """Public method: run retrieval and generate answer following strict rules."""
        try:
            question = question.strip()
            if not question:
                return {'answer': 'Please provide a valid question.', 'sources': [], 'category': 'invalid', 'context_count': 0}

            contexts = self.retrieve(question, k=5)
            result = self.generate_answer_from_context(question, contexts)
            # Ensure India-focused and agriculture-only policy in reply metadata
            result['note'] = 'Agriculture-focused. India-context. No medical/financial advice.'
            result['context_count'] = len(contexts)
            return result
        except Exception as e:
            print(f'[ERROR] InternalRAG query error: {e}')
            return {'answer': 'Service temporarily unavailable.', 'sources': [], 'category': 'error', 'context_count': 0}

    # Compatibility API expected by routes
    def answer_query(self, question: str) -> dict:
        """Compatible wrapper returning status + structured data as earlier implementation expected."""
        res = self.query(question)
        status = 'success' if res.get('answer') and res.get('category') != 'error' else 'error'
        return {
            'status': status,
            'answer': res.get('answer'),
            'sources': res.get('sources', []),
            'context_count': res.get('context_count', 0)
        }

    def get_knowledge_base_stats(self) -> dict:
        """Return stats about internal KB for the /kb-stats endpoint."""
        return {
            'kb_entries': len(self.kb),
            'chunks': len(self.chunks),
            'embeddings_available': self.available_embeddings,
            'status': 'ready'
        }

    def add_document(self, content: str, title: str, category: str) -> bool:
        """Add document to internal KB and persist to MongoDB RAGDocument if available."""
        try:
            new_entry = {'title': title, 'category': category, 'region': 'India', 'season': 'all', 'text': content}
            self.kb.append(new_entry)
            # create chunks for the new entry
            words = content.split()
            i = 0
            while i < len(words):
                chunk_words = words[i:i+400]
                chunk_text = ' '.join(chunk_words)
                metadata = {'title': title, 'category': category, 'region': 'India', 'season': 'all'}
                self.chunks.append({'text': chunk_text, 'metadata': metadata})
                i += 400

            # Try persisting to MongoDB RAGDocument
            try:
                from models.database import RAGDocument
                RAGDocument.add_document(content=content, title=title, category=category)
            except Exception:
                # non-fatal if DB not available
                pass

            return True
        except Exception as e:
            print(f'[ERROR] InternalRAG add_document error: {e}')
            return False


# Instantiate internal RAG chatbot (self-contained)
try:
    internal_rag = InternalRAGChatbot()
    # prefer internal_rag as primary chatbot
    rag_chatbot = internal_rag
    RAGChatbot = type(rag_chatbot)
    print('[OK] Using InternalRAGChatbot as primary chatbot')
except Exception as e:
    print(f'[WARN] Failed to instantiate InternalRAGChatbot: {e}')
