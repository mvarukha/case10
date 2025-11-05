from collections import defaultdict
import re


def create_categories() -> dict:
    """
    Create a dictionary mapping categories to their keyword lists.

    Returns:
        Dictionary where keys are category names and values are lists of keywords.
    """
    return {
        "food": [
            "pyaterochka", "magnit", "spar", "bystronom", "yarcher", "lenta", 
            "maria-ra", "products", "food", "supermarket", "vegetables", 
            "fruits", "bread", "bakery", "confectionery", "gastronomy", 
            "grocery", "market"
        ],
        "transport": [
            "metro", "bus", "trolleybus", "tram", "train", "electric train", 
            "taxi", "gasoline", "fuel", "travel", "troika card", "transport", 
            "motorcycle", "bicycle", "carsharing", "electric scooter", 
            "gazpromneft", "lukoil", "rosneft", "gas station", "fine", 
            "traffic police", "parking", "car wash", "insurance", "osago", "casco"
        ],
        "entertainment": [
            "cinema", "movie", "restaurant", "cafe", "concert", "theater", 
            "bar", "club", "ticket", "aquapark", "bowling", "karaoke", 
            "attraction", "game", "formula kino", "cinema park", "quest", 
            "shooting range", "zoo"
        ],
        "health": [
            "pharmacy", "doctor", "hospital", "medicine", "medication", "dentist",
            "tests", "consultation", "vitamins", "x-ray", "mri", "msct", "scan"
        ],
        "travel": [
            "travel", "hotel", "hostel", "air ticket", "train", "airplane",
            "station", "airport", "excursion", "resort"
        ],
        "sport": [
            "sportmaster", "sporting goods", "sports suit", "trainer", "dumbbells",
            "weights", "barbell", "elliptical", "treadmill", "bicycle", "bike helmet",
            "bike accessories", "swimsuit", "swimming goggles", "swimming cap",
            "skis", "skates", "snowboard", "football", "ball", "sports nutrition",
            "protein", "water bottle", "fitness bracelet"
        ],
        "clothes_and_shoes": [
            "clothing", "clothes", "shoes", "footwear", "t-shirt", "polo", "shirt",
            "blouse", "sweater", "sweatshirt", "hoodie", "cardigan", "pants",
            "jeans", "shorts", "skirt", "dress", "jacket", "coat", "down jacket",
            "raincoat", "sneakers", "sports shoes", "shoes", "loafers", "moccasins",
            "boots", "sandals", "slippers", "heels", "ballet flats", "espadrilles"
        ],
        "children": [
            "children's world", "toys", "toy", "children's clothing", "baby food",
            "kindergarten", "nursery", "car seat", "pediatrician", "clubs",
            "sections", "school", "stationery", "doll", "car", "constructor",
            "puzzle", "crib", "stroller"
        ],
        "pets": [
            "pet store", "pet supplies", "wet nose", "pet food", "carrier",
            "bed", "scratching post", "house", "leash", "collar", "harness",
            "bowl", "water dispenser", "grooming", "veterinarian", "boarding",
            "pet hotel", "walking", "training", "dog trainer", "kennel",
            "shelter", "animal help", "animal charity"
        ],
        "home": [
            "lemana pro", "construction", "furniture", "interior", "repair",
            "wallpaper", "paint", "laminate", "tile", "plumbing", "electrical goods",
            "tools", "garden", "vegetable garden", "plants", "flowers", "textiles",
            "bedding", "towels", "dishes", "kitchen", "household appliances",
            "cleaning", "detergents", "lighting", "decor"
        ],
        "electronics": [
            "m.video", "eldorado", "citilink", "dns", "appliances", "electronics",
            "computer", "laptop", "phone", "smartphone", "tablet", "headphones",
            "speakers", "tv", "television", "photo", "video", "gadgets",
            "accessories", "charging", "cable", "router", "printer", "games",
            "software", "service", "repair", "apple", "iphone", "ipad", "samsung",
            "xiaomi", "huawei", "honor", "sony", "philips", "hp", "panasonic", "intel"
        ],
        "beauty": [
            "rive gauche", "letoile", "golden apple", "cosmetics", "perfume",
            "beauty salon", "hairdresser", "barbershop", "stylist", "makeup artist",
            "manicure", "pedicure", "nail service", "eyebrows", "eyelashes",
            "extensions", "lamination", "cosmetologist", "massage", "spa", "sauna"
        ],
        "finance": [
            "bank", "insurance", "credit", "mortgage", "deposit", "investment",
            "taxes", "transfer", "payment", "bill", "receipt", "fine", "duty",
            "debt", "loan", "leasing", "factoring"
        ],
        "education": [
            "education", "studying", "university", "institute", "college",
            "courses", "tutor", "training", "school", "kindergarten", "student",
            "textbooks", "stationery", "pens", "notebooks", "album", "paints", "brushes"
        ],
        "home_services": [
            "utilities", "rent", "electricity", "water", "heating", "gas",
            "internet", "television", "intercom", "concierge", "cleaning",
            "laundry", "dry cleaning", "tailor", "shoe repair", "keys",
            "master call", "plumber", "electrician", "installation", "mounting",
            "water delivery", "garbage disposal", "security"
        ],
        "gifts_flowers_jewelry": [
            "gift", "flowers", "bouquet", "jewelry", "gold", "silver",
            "jewellery", "diamond", "ring", "earrings", "chain", "souvenir",
            "postcard", "packaging", "crystal", "porcelain", "antiques",
            "painting", "frame", "costume jewelry", "watch", "watchmaker",
            "florist", "flower"
        ],
        "business": [
            "stationery", "office", "advertising", "marketing", "printing",
            "copying", "courier", "mail", "delivery", "packaging", "materials",
            "tools", "equipment", "communication", "mobile", "internet"
        ],
        "subscriptions": [
            "subscription", "streaming", "ivi", "wink", "okko", "more.tv", "start",
            "yandex plus", "vk music", "sberprime", "apple music", "yandex music",
            "telegram premium", "online course", "software", "antivirus", "cloud",
            "hosting", "domain"
        ],
        "auto": [
            "auto service", "tire fitting", "car wash", "spare parts", "battery",
            "oil", "filter", "brakes", "glass", "tires", "wheels", "maintenance",
            "diagnostics", "painting", "body repair", "tow truck", "inspection",
            "insurance", "garage", "parking", "auto detailing", "polishing"
        ]
    }


def get_keyword_match_score(description: str, keyword: str) -> int:
    """
    Calculate the match score between a description and a keyword.

    Args:
        description: The transaction description to search in.
        keyword: The keyword to search for.

    Returns:
        Integer score: 3 for exact match, 1 for partial match, 0 for no match.
    """
    # Exact word match with word boundaries.
    if re.search(rf'\b{re.escape(keyword)}\b', description, re.IGNORECASE):
        return 3
    
    # Partial match (word starts with keyword).
    if re.search(rf'\b{re.escape(keyword)}', description, re.IGNORECASE):
        return 1
    
    return 0


def pick_best_category(category_scores: dict) -> str:
    """
    Select the best category from scored categories using priority rules.

    Args:
        category_scores: Dictionary with category names as keys and scores as values.

    Returns:
        String representing the selected category name.
    """
    priority_order = [
        "finance", "health", "home_services", "education",
        "transport", "food", "subscriptions", "auto"
    ]

    best_score = max(category_scores.values())

    top_candidates = [
        category for category, score in category_scores.items() 
        if score == best_score
    ]

    if len(top_candidates) == 1:
        return top_candidates[0]

    for important_category in priority_order:
        if important_category in top_candidates:
            return important_category

    return top_candidates[0]


def categorize_transaction(description: str, categories: dict) -> str:
    """
    Categorize a single transaction based on its description.

    Args:
        description: The transaction description text.
        categories: Dictionary of categories and their keywords.

    Returns:
        String representing the assigned category or "other" if no match found.
    """
    if not description or not isinstance(description, str):
        return "other"
    
    clean_description = description.lower().strip()
    scores = defaultdict(int)

    for category_name, keywords in categories.items():
        category_score = 0
        
        for keyword in keywords:
            category_score += get_keyword_match_score(clean_description, keyword)

        if category_score > 0:
            scores[category_name] = category_score

    if scores:
        return pick_best_category(scores)

    return "other"


def categorize_all_transactions(transactions: list) -> list:
    """
    Categorize all transactions in a list by adding category fields.

    Args:
        transactions: List of transaction dictionaries.

    Returns:
        List of transactions with added 'category' field for each transaction.
    """
    category_map = create_categories()
    
    processed_transactions = []
    for transaction in transactions:
        categorized_transaction = transaction.copy()
        categorized_transaction['category'] = categorize_transaction(
            transaction.get('description', ''), 
            category_map
        )
        processed_transactions.append(categorized_transaction)
    
    return processed_transactions


def get_classification_stats(transactions: list) -> dict:
    """
    Generate statistics about the classification results.

    Args:
        transactions: List of categorized transactions.

    Returns:
        Dictionary containing classification statistics and top categories.
    """
    category_counts = defaultdict(int)
    total = len(transactions)

    for transaction in transactions:
        category = transaction.get('category', 'other')
        category_counts[category] += 1

    unclassified_pct = 0.0
    if total > 0:
        unclassified_pct = round(category_counts['other'] / total * 100, 2)

    most_common = sorted(
        category_counts.items(), 
        key=lambda x: x[1],
        reverse=True
    )[:5]

    stats = {
        'total_processed': total,
        'unique_categories': len(category_counts),
        'unclassified_rate': unclassified_pct,
    }

    for rank, (category, count) in enumerate(most_common, 1):
        stats[f'top_{rank}'] = f"{category} ({count} transactions)"
    
    return stats