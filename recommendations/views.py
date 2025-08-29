from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from catalog.models import Book
from catalog.serializers import BookSerializer
from .llm import call_groq, summarise_book
from rest_framework.permissions import IsAuthenticated, AllowAny

MOOD_KEYWORDS = {
    "happy": [
        "funny", "uplifting", "happy", "feel-good", "lighthearted", 
        "joyful", "cheerful", "optimistic", "playful", "wholesome",
        "humor", "bright", "positive", "entertaining"
    ],
    "sad": [
        "poignant", "grief", "tragic", "moving", 
        "emotional", "tearjerker", "sorrow", "heartbreaking",
        "loss", "lonely", "melancholy", "sentimental"
    ],
    "adventurous": [
        "adventure", "quest", "journey", "exploration", 
        "epic", "wild", "thrill", "action", "survival",
        "wanderlust", "danger", "heroic", "voyage", "mystery"
    ],
    "romantic": [
        "romance", "love", "relationship", "heart", 
        "passion", "affection", "flirt", "kiss", "desire",
        "longing", "intimacy", "soulmate", "charming", "wedding"
    ],
    "thoughtful": [
        "philosophy", "ideas", "reflective", "literary", 
        "deep", "introspective", "meaning", "existential",
        "contemplative", "insightful", "analytical", "abstract", "wisdom"
    ],
    "chill": [
        "cozy", "calm", "gentle", "comfort", 
        "relaxed", "peaceful", "slow", "soft", "serene",
        "soothing", "laid-back", "quiet", "dreamy", "tranquil"
    ],
    "scared": [
        "horror", "thriller", "fear", "creepy", 
        "dark", "nightmare", "terrifying", "spooky", "ghost",
        "suspense", "eerie", "haunted", "blood", "dread"
    ],
    "curious": [
        "science", "history", "discovery", "why", "how", 
        "mystery", "explained", "experiment", "knowledge",
        "learning", "odd", "unusual", "question", "facts"
    ],
}


class MoodRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = request.GET.get("mood").lower().strip()
        prompt = request.GET.get("prompt")
        limit = int(request.GET.get("limit", 10))

        q = Q()
        for kw in MOOD_KEYWORDS[category]:
            q |= Q(title__icontains=kw) | Q(description__icontains=kw) | Q(category__name__icontains=kw)

        candidates = Book.objects.filter(stock__gt=0).filter(q).order_by("-pub_date")[:30]
        for c in candidates:
            print("candidate", c.id)
        candidate_data = [
            {
                "id": b.id,
                "title": b.title,
                "author": str(b.author),
                "descrption": (b.description or ""),
                "category": str(b.category),
            }
            for b in candidates
        ]

        if not candidate_data:
            return Response({"mood": category, "results": [], "message": "No candidates found"})

        # messages = build_prompt(prompt=prompt, mood=category, books=candidate_data, limit=limit)
        picks = call_groq(prompt,mood=category, books=candidate_data,limit=limit)
        
        if not picks:
            ser = BookSerializer(candidates[:limit], many=True)
            return Response({"mood": category, "prompt": prompt, "ai_used": False, "results": ser.data})

        id_to_reason = {p["id"]: p["reason"] for p in picks}
        ids = [p["id"] for p in picks]
        qs = Book.objects.filter(id__in=ids)
        ser = BookSerializer(qs, many=True)
        results = []
        for item in ser.data:
            item["reason"] = id_to_reason.get(item["id"], "Matches your mood")
            results.append(item)

        return Response({"mood": category, "prompt": prompt, "ai_used": True, "results": results})


class BookSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        
        book = Book.objects.get(id=id)
        summary = summarise_book(title = book.title ,desc = book.description, )
        ser = BookSerializer(book)
        return Response(summary)
        
