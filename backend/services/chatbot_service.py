"""
Chatbot Service - Complete RAG system
Manages internal KB, embeddings, retrieval, and answer generation
"""

import logging
from typing import List, Dict, Optional
from services.vector_store import VectorStore
from services.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class ChatbotService:
    """
    Production RAG chatbot service.
    - Internal agriculture knowledge base
    - Vector search with FAISS/cosine similarity
    - Strict Gemini Flash integration
    """
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.gemini_client = GeminiClient()
        self.kb_initialized = False
        
        # Initialize KB on startup
        self._init_knowledge_base()
    
    def _init_knowledge_base(self):
        """Build and load internal agriculture knowledge base"""
        documents = self._build_kb()
        self.vector_store.add_documents(documents)
        self.kb_initialized = True
        logger.info(f'[OK] KB initialized with {len(documents)} documents')
    
    def _build_kb(self) -> List[Dict]:
        """
        Build internal agriculture knowledge base.
        Each document: crop name, topic, content
        """
        kb = [
            # TOMATO
            {
                'crop': 'Tomato',
                'topic': 'Fertilizer',
                'content': 'Tomato requires nitrogen during vegetative growth. Use urea (150 kg/ha) at 30 days and 50 days. DAP (400 kg/ha) at planting. Potassium chloride (100 kg/ha) at flowering. FYM 5-7 tons/ha before planting. Micronutrients: zinc, boron, magnesium sprays every 15 days.'
            },
            {
                'crop': 'Tomato',
                'topic': 'Cultivation',
                'content': 'Tomato grows best in well-drained loamy soil. Plant 60cm x 60cm spacing. Needs support stakes or strings. Pinch terminal buds to control height. Harvest when fully colored but still firm. Yield: 50-60 tons/hectare with good management.'
            },
            {
                'crop': 'Tomato',
                'topic': 'Pest',
                'content': 'Common pests: fruit borer, whitefly, aphid. Diseases: blight, wilt, leaf spot. Control: remove infected plants, spray neem oil fortnightly, use yellow sticky traps. Avoid overhead irrigation to reduce disease.'
            },
            {
                'crop': 'Tomato',
                'topic': 'Irrigation',
                'content': 'Tomato needs 400-500mm water. Drip irrigation is ideal. Water deeply 2-3 times per week during growth. Reduce frequency during flowering to improve fruiting. Maintain soil moisture but avoid waterlogging.'
            },
            
            # CUCUMBER
            {
                'crop': 'Cucumber',
                'topic': 'Fertilizer',
                'content': 'Cucumber needs balanced nutrition. Apply DAP 300 kg/ha at sowing. Urea 100 kg/ha at 30 days, 50 kg/ha at flowering. Potassium chloride 50 kg/ha at flowering. FYM 3-5 tons/ha. Foliar spray: zinc, boron during flowering.'
            },
            {
                'crop': 'Cucumber',
                'topic': 'Cultivation',
                'content': 'Cucumber grows on vines; requires trellising or ground coverage. Plant 45cm x 60cm spacing. Harvest every 2-3 days when 15-20cm long. Pollination by bees is essential. Cool weather extends harvest. Yield: 30-40 tons/hectare.'
            },
            {
                'crop': 'Cucumber',
                'topic': 'Pest',
                'content': 'Pests: fruit fly, spider mite, whitefly. Diseases: powdery mildew, downy mildew. Control: spray sulfur for mildew, neem for pests. Remove diseased leaves. Improve air circulation to prevent fungal diseases.'
            },
            {
                'crop': 'Cucumber',
                'topic': 'Irrigation',
                'content': 'Cucumber needs 300-400mm water in 20-25 days. Drip irrigation keeps foliage dry, reducing disease. Water early morning. During fruiting, keep soil consistently moist but not waterlogged.'
            },
            
            # WHEAT
            {
                'crop': 'Wheat',
                'topic': 'Fertilizer',
                'content': 'Wheat requires 60kg N, 40kg P2O5, 40kg K2O per hectare. Apply DAP 200kg/ha at planting. Urea 200kg/ha in 2 splits: 100kg/ha at tillering, 100kg/ha at boot stage. FYM 5 tons/ha. Zinc sulfate 12.5kg/ha if deficient.'
            },
            {
                'crop': 'Wheat',
                'topic': 'Cultivation',
                'content': 'Wheat is a rabi (winter) crop. Sow November-December, harvest March-April. Requires 400-500mm rainfall. Plant density: 100-120kg seed/hectare. Optimal spacing: 22-25cm rows. Irrigation: 4-5 times. Yield: 40-50 quintals/hectare.'
            },
            {
                'crop': 'Wheat',
                'topic': 'Pest',
                'content': 'Major pests: shoot fly, armyworm, termites. Diseases: rust, smut, bunt. Control: use resistant varieties, sow on time, spray carbendazim for fungal diseases. Soil treatment for termites.'
            },
            {
                'crop': 'Wheat',
                'topic': 'Irrigation',
                'content': 'Wheat needs 450-650mm water for optimal yield. Critical irrigation stages: after sowing, tillering, boot, anthesis. Total 4-5 irrigations in north India. In monsoon areas, 1-2 irrigations. Avoid waterlogging.'
            },
            
            # RICE
            {
                'crop': 'Rice',
                'topic': 'Fertilizer',
                'content': 'Rice needs 100kg N, 50kg P2O5, 40kg K2O per hectare. Apply DAP 250kg/ha + urea 100kg/ha at transplanting. Urea 100kg/ha at tillering, 100kg/ha at panicle emergence. FYM 5 tons/ha. Micronutrients: Zn, Fe, B as needed.'
            },
            {
                'crop': 'Rice',
                'topic': 'Cultivation',
                'content': 'Rice is a kharif (monsoon) crop. Sow June-July, harvest September-October. Flood irrigation is standard. Transplant seedlings 30-40 days old at 20cm x 15cm spacing. Maintain 5-7cm water depth during growth. Yield: 40-60 quintals/hectare.'
            },
            {
                'crop': 'Rice',
                'topic': 'Pest',
                'content': 'Pests: stem borer, leaf folder, brown planthopper, gall midge. Diseases: blast, sheath rot, brown spot. Control: use resistant varieties, clean fields, spray carbendazim or thiophanate-methyl. Avoid excess nitrogen to reduce pests.'
            },
            {
                'crop': 'Rice',
                'topic': 'Irrigation',
                'content': 'Rice requires 1000-2000mm water annually. Flooding is continuous during growth. 5-7cm water depth from transplanting to panicle emergence. Reduce to 2-3cm during grain filling. Drain 2 weeks before harvest.'
            },
            
            # ONION
            {
                'crop': 'Onion',
                'topic': 'Fertilizer',
                'content': 'Onion needs 80kg N, 40kg P2O5, 60kg K2O per hectare. Apply FYM 20 tons/ha + DAP 250kg/ha at planting. Urea 100kg/ha at 30 days, 100kg/ha at 60 days. Potassium chloride 100kg/ha for bulb development.'
            },
            {
                'crop': 'Onion',
                'topic': 'Cultivation',
                'content': 'Onion grows from sets or seeds. Plant 15cm x 10cm spacing. Days to harvest: 90-120 days. Requires cool weather for bulbing. Harvest when tops fall over and dry. Yield: 40-50 tons/hectare. Store in cool, dry place.'
            },
            {
                'crop': 'Onion',
                'topic': 'Pest',
                'content': 'Pests: thrips, stem borer. Diseases: pink root, basal rot, purple blotch. Control: spray dimethoate for thrips, copper fungicide for blotch. Avoid overhead irrigation. Ensure good drainage.'
            },
            {
                'crop': 'Onion',
                'topic': 'Irrigation',
                'content': 'Onion needs 400-600mm water in 90-120 days. Drip irrigation is best. Water weekly during growth, reduce during bulbing to concentrate sugars. Avoid waterlogging which causes rot.'
            },
            
            # COTTON
            {
                'crop': 'Cotton',
                'topic': 'Fertilizer',
                'content': 'Cotton needs 100kg N, 50kg P2O5, 50kg K2O per hectare. Apply DAP 250kg/ha at planting. Urea 100kg/ha at 45 days, 100kg/ha at 90 days. Potassium chloride 100kg/ha. FYM 5 tons/ha. Monitor for deficiencies.'
            },
            {
                'crop': 'Cotton',
                'topic': 'Cultivation',
                'content': 'Cotton is kharif crop. Sow June-July. Spacing: 90cm x 60cm. Top the plant at 90cm height to increase boll formation. Harvest September-December. Yield: 15-25 quintals/hectare of seed cotton. Requires warm climate.'
            },
            {
                'crop': 'Cotton',
                'topic': 'Pest',
                'content': 'Major pests: bollworm, leaf roller, aphid, spider mite. Diseases: leaf curl, wilt. Control: use Bt cotton varieties, spray neem oil, monitor with pheromone traps. Avoid excess nitrogen which promotes vegetative growth.'
            },
            {
                'crop': 'Cotton',
                'topic': 'Irrigation',
                'content': 'Cotton needs 600-1000mm water. Critical stages: flowering and boll development. Drip or flood irrigation. Water every 10-12 days during growth, increase frequency during flowering. Avoid waterlogging which promotes diseases.'
            },
            
            # POTATO
            {
                'crop': 'Potato',
                'topic': 'Fertilizer',
                'content': 'Potato needs 90kg N, 60kg P2O5, 90kg K2O per hectare. Apply FYM 20 tons/ha + DAP 300kg/ha at planting. Urea 100kg/ha at 30 days, 100kg/ha at 60 days. Potassium chloride 150kg/ha for quality tubers.'
            },
            {
                'crop': 'Potato',
                'topic': 'Cultivation',
                'content': 'Potato is rabi crop. Plant certified seed tubers (20-25g) 25cm x 10cm spacing. Hill soil to 5cm at 30-40 days for tuber development. Harvest 90-120 days after planting when leaves dry. Yield: 200-250 quintals/hectare.'
            },
            {
                'crop': 'Potato',
                'topic': 'Pest',
                'content': 'Pests: cut worm, aphid, mite. Diseases: late blight, early blight, scab. Control: use disease-resistant varieties, spray mancozeb for blight, avoid overhead irrigation. Rotate crops to reduce soil-borne diseases.'
            },
            {
                'crop': 'Potato',
                'topic': 'Irrigation',
                'content': 'Potato needs 400-500mm water in 90-120 days. Critical stages: tuberization (40-60 days). Drip irrigation ensures uniform growth. Avoid waterlogging which causes tuber rot. Mulching conserves moisture.'
            }
        ]
        
        return kb
    
    def query(self, question: str) -> Dict:
        """
        Process user question through RAG pipeline.
        
        Returns:
            {
                'answer': str,
                'sources': List[str] (crop+topic),
                'status': 'success' or 'error'
            }
        """
        try:
            question_clean = question.strip()
            if not question_clean:
                return {
                    'answer': 'Please ask a farming question.',
                    'sources': [],
                    'status': 'error'
                }
            
            # Retrieve relevant documents
            retrieved = self.vector_store.search(question_clean, k=3)
            
            if not retrieved:
                return {
                    'answer': "I don't have enough information to answer this question.",
                    'sources': [],
                    'status': 'success'
                }
            
            # Build context from retrieved documents
            context_parts = []
            sources = set()
            for doc in retrieved:
                crop = doc.get('crop', 'Unknown')
                topic = doc.get('topic', 'Unknown')
                content = doc.get('content', '')
                
                context_parts.append(f"{crop} - {topic}:\n{content}")
                sources.add(f"{crop} ({topic})")
            
            context = "\n\n".join(context_parts)
            
            # Generate answer using Gemini (or fallback)
            if self.gemini_client.is_available():
                answer = self.gemini_client.generate_answer(question_clean, context)
            else:
                # Fallback: return context directly
                answer = f"Based on available information:\n\n{context}"
            
            return {
                'answer': answer,
                'sources': list(sources),
                'status': 'success'
            }
        
        except Exception as e:
            logger.error(f'[ERROR] Query processing failed: {e}')
            return {
                'answer': 'Service error. Please try again.',
                'sources': [],
                'status': 'error'
            }
    
    def get_stats(self) -> Dict:
        """Return KB and system stats"""
        return {
            'total_documents': len(self.vector_store.documents),
            'gemini_available': self.gemini_client.is_available(),
            'vector_store_ready': self.kb_initialized,
            'status': 'healthy' if self.kb_initialized else 'initializing'
        }
