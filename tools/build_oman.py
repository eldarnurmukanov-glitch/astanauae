#!/usr/bin/env python3
"""Builds oman/index.html — Oman Residential Catalog (Autumn 2026).

Edit DISTRICTS / PROJECTS below, then run:  python3 tools/build_oman.py
Images live in oman/img/: p{page}-1..3.jpg per project (page = PDF page number),
d-{district}.jpg per district banner.
"""
import html, json, os, urllib.parse

WA = "971507369833"
SITE = "https://eldarnurmukanov-glitch.github.io/astanauae/oman/"

DISTRICTS = [
    # key, name, eyebrow, tagline, banner
    ("al-mouj", "Al Mouj Muscat", "Muscat · District", "A resort district with golf, beaches and a marina", "al-mouj"),
    ("sultan-haitham", "Sultan Haitham City", "Muscat · District", "A new smart city with its own infrastructure", "sultan-haitham"),
    ("yiti", "Yiti", "Muscat · District", "A sustainable coastal district with resort amenities", "yiti"),
    ("muscat-hills", "Muscat Hills", "Muscat · District", "A green district built around golf courses", "muscat-hills"),
    ("muscat-bay", "Muscat Bay", "Muscat · District", "A coastal district at the foot of the mountains", "muscat-bay"),
    ("jebel-sifah", "Jebel Sifah", "Muscat · District", "A private community between the golf course and the mountains", "jebel-sifah"),
    ("knowledge-oasis", "Knowledge Oasis", "Muscat · District", "A technology park of 1 million sq ft", "knowledge-oasis"),
    ("other", "Other locations", "Oman", "Telal Al Qurum, Bidbid, Sur, Seeb and Shatti Al Qurum", "other"),
    ("salalah", "Salalah", "Oman · South", "A tropical oasis in the Arabian Desert — the summer khareef monsoon turns the Dhofar hills green", "salalah-khareef"),
]

# page, name, handover, developer, location, district, type, prices[(label, usd|None)], lead, desc, amenities
PROJECTS = [
    (5, "Vistal by Victoria Swarovski", "Q4 2029", "LEO Developments", "Al Mouj Muscat", "al-mouj", "Branded apartments",
     [("", 375000)], "Nine-storey beachfront building in Al Mouj. Payment plan 70/30 over 3 years, $13,000 on booking.",
     "Apartments come fully finished in a light palette, with floor-to-ceiling glazing of adjustable transparency. Selected units have private pools and gardens; custom interiors on request.",
     ["swimming pool", "private beach", "smart home", "BBQ zones", "lounge areas", "spa", "10+ more amenities"]),
    (6, "Bellevue", "Q4 2027", "Ideal Building", "Al Mouj Muscat", "al-mouj", "Apartments",
     [("", 390000)], "Payment plan: 15% down, 15% every 5 months until handover, 20% on handover, 20% six months after.",
     "A 9-storey club house by the sea in an established area: yacht club, restaurants, school and a beach within a 5-minute walk. 1- and 2-bedroom apartments from 721 sq ft, most with sea-facing windows; units with private patios available.",
     ["swimming pool", "private cinema", "gym", "landscaped gardens", "playground", "sport court", "kids’ club", "BBQ area", "parking"]),
    (7, "St. Regis Al Mouj Muscat", "Completed", "Alfardan Group", "Al Mouj Muscat", "al-mouj", "Hotel apartments",
     [("", 885000)], "Payment plan 40/60: 40% down, the balance in post-handover instalments of up to 3 years.",
     "Two boutique buildings with hotel-managed residences in a resort district with a golf club and a private beach. 1- to 4-bedroom layouts from 1,506 to 6,000 sq ft. 10 minutes to MCT Airport, 35 minutes to the city centre.",
     ["swimming pool", "rooftop gardens", "fitness club", "restaurants", "business lounge", "spa", "concierge", "beach and golf access"]),
    (9, "Yenaier", "Q4 2027", "Adrak Developers", "Sultan Haitham City", "sultan-haitham", "Apartments",
     [("", 150000)], "Six towers linked by green boulevards and cascading gardens. Payment plan 80/20 over 2.5 years with 20% down; a 5-year plan is also available.",
     "Studios and 1–3 bedroom apartments from 764 to 4,973 sq ft. 12 minutes to the beach, 30 minutes to MCT Airport; Oman Botanic Garden and Al Araimi Boulevard mall nearby.",
     ["swimming pool", "gym", "kindergarten", "playgrounds", "landscaped grounds", "clubhouse", "5+ more amenities"]),
    (10, "Wadi Zaha", "Q1 2028", "Ahly Sabbour", "Sultan Haitham City", "sultan-haitham", "Apartments",
     [("", 160000)], "Payment plan 98/2 over 5 years: 20% down, then 1–2% monthly. Discounts of up to 5% for a limited group of buyers.",
     "Mid-rise club houses around their own landscaped park, 15 minutes from the beach and close to Muscat. Studios and 1–3 bedroom apartments from 540 sq ft, plus villas with 3–7 bedrooms. Every unit has a balcony.",
     ["swimming pool", "gym", "walking area", "playground", "zen gardens", "sport courts", "cafes and retail", "parking", "wellness centre"]),
    (11, "Sarooj Oasis", "Q4 2029", "Sarooj Development", "Sultan Haitham City", "sultan-haitham", "Apartments and villas",
     [("apartments", 170000), ("villas", 450000)], "3-year instalment plan: 20% down, then 2.29% monthly. A 30/40/50% down payment cuts the monthly to 2/1.71/1.43%.",
     "A green neighbourhood of clubhouse residences and villas, with schools, a landscaped park and a business cluster. 1–4 bedroom apartments from 775 sq ft, finished, all with balconies.",
     ["swimming pool", "gym", "walking area", "playground", "landscaped park", "sport courts", "cafes and retail", "parking", "bicycle lanes"]),
    (12, "Jood", "Q1 2030", "Talaat Moustafa Group", "Sultan Haitham City", "sultan-haitham", "Apartments and townhouses",
     [("apartments", 204800), ("townhouses", 420000)], "A large-scale community of apartments and villas in Sultan Haitham City.",
     "A complex of 7,746 residences: 1–4 bedroom apartments and villas for large families. Sandstone-toned facades; terraces that work as a lounge or a garden-view workspace.",
     ["pools with sun terraces", "children’s playgrounds", "sports courts", "walking and cycling areas", "parks", "shops and restaurants", "mosques"]),
    (13, "Hay Alwafa", "Q4 2028", "Al Abrar Real Estate", "Sultan Haitham City", "sultan-haitham", "Furnished apartments, townhouses and villas",
     [("apartments", 240000), ("townhouses", 390000), ("villas", 630000)], "Part of the Sultan Haitham City masterplan. Payment plan 20/80: 20% down, 36-month instalment.",
     "1–3 bedroom apartments, 3–4 bedroom townhouses and 5-bedroom villas. Finishes in marble, stone and wood, built-in lighting and neutral tones.",
     ["swimming pool", "gym", "shopping mall", "playground", "clinic", "sport courts", "landscaped gardens", "parking", "school", "10+ more amenities"]),
    (14, "Al Ahlam District", "Q1 2027", "Dream Villa", "Sultan Haitham City", "sultan-haitham", "Villas",
     [("", 610000)], "Luxury villas in a private community with a park, lagoon, school and shopping centre, 10 minutes from the sea. Payment plan 95/5 over 1.5 years, 20% down.",
     "4–6 bedroom villas with swimming pools, gardens, terraces, patios and staff quarters. Smart home system in every villa.",
     ["promenade", "landscaped park", "sport courts", "kids’ playgrounds", "shopping mall", "cycling and jogging tracks"]),
    (16, "The Sustainable City Yiti", "Q4 2027", "SDIC", "Yiti", "yiti", "Apartments, villas and offices",
     [("apartments", 225000), ("villas", 620000)], "Payment plan 30/70 with a 5% reservation payment; 3- and 5-year plans also available.",
     "A mixed-use complex of six buildings at the heart of The Sustainable City, a new eco-community on the Gulf of Oman coast, 45 minutes from Muscat International Airport.",
     ["kindergarten and school", "swimming pool", "green parks", "kids’ playgrounds", "equestrian club and racetrack", "indoor and outdoor gyms", "cycling and jogging tracks"]),
    (17, "The Great Escape 2", "Q4 2029", "DarGlobal", "Yiti · AIDA", "yiti", "Apartments",
     [("", 335000)], "Resort-style clubhouse homes on the seafront in the AIDA community: beach, golf courses, restaurants. Payment plan 90/10 over 3.5 years, 20% down.",
     "1–3 bedroom apartments finished to full European standard, most with views over the Gulf of Oman.",
     ["golf course", "beach", "retail promenade", "restaurants", "palm promenade", "landscaped park", "luxury hotel services"]),
    (18, "AIDA Villas", "Q4 2028", "DarGlobal", "Yiti", "yiti", "Villas",
     [("", 460000)], "Hillside villas with panoramic views of the Gulf of Oman, a 10-minute walk from the beach. Payment plan 90/10 over 3 years, 10% down.",
     "The villas sit 130 metres above sea level: beige finishes, panoramic windows, a spacious patio with a jacuzzi. 25 minutes to downtown Muscat and the Royal Opera, 40 minutes to MCT Airport.",
     ["golf course", "swimming pool", "spa", "night club", "restaurant", "concierge", "terraces", "cycling and jogging tracks"]),
    (20, "Opal Residence", "Q4 2028", "Al Nama Real Estate", "Muscat Hills", "muscat-hills", "Furnished apartments",
     [("", 195000)], "A 7-storey residential complex in Muscat Hills. Payment plan 20/80 over 3 years, 20% down.",
     "Studios, 1- and 2-bedroom apartments, with selected layouts adding a home office and a staff room. Every unit has a balcony and a laundry area; larger layouts have several bathrooms.",
     ["swimming pool", "sauna and steam room", "playground", "BBQ area", "terraces", "cycling and jogging tracks", "park"]),
    (21, "Golf Hills", "Q4 2028", "Al Osool Properties", "Muscat Hills", "muscat-hills", "Apartments",
     [("", 200000)], "Three towers next to golf courses and an academic cluster, close to the airport and the EXPO centre. Payment plan 80/20 over 2.5 years, 10% down.",
     "All layouts have balconies and laundry areas; larger units have several bathrooms. European-style kitchens with built-in appliances; smart entry by fingerprint and code.",
     ["lounge area", "swimming pool", "spa", "playground", "BBQ area", "terraces", "cycling and jogging tracks", "park"]),
    (23, "Luma Residence", "Q1 2029", "Saraya Bandar Jissah", "Muscat Bay", "muscat-bay", "Apartments, townhouses and villas",
     [("apartments", 335000), ("townhouses", 570000), ("villas", 680000)], "Resort residences in the coastal community of Bandar Jissah. Payment plan 50/50 over 3.5 years, 2.5% reservation payment.",
     "240 residences: 1–2 bedroom apartments, 3-bedroom townhouses and villas. 6 minutes to Qantab Beach, 17 minutes to Mazoon Mall, about 35 minutes to Muscat International Airport.",
     ["swimming pool", "gym", "BBQ area", "yoga deck", "spa", "5+ more amenities"]),
    (24, "Zen Residences", "Q1 2027", "Zen Development", "Muscat Bay", "muscat-bay", "Apartments",
     [("", 365000)], "Five clubhouses with resort-style amenities and Gulf of Oman views, a 10-minute walk from the beach. Payment plan 80/20 over 2.5 years, 20% down.",
     "Every apartment has a spacious balcony; panoramic windows look onto the mountains and the surrounding landscape.",
     ["sport court", "swimming pool", "yoga deck", "playground", "BBQ area", "terraces", "cycling and jogging tracks", "private beach access"]),
    (25, "Muscat Bay", "Completed", "Saraya Bandar Jissah", "Muscat Bay", "muscat-bay", "Villas",
     [("", 805000)], "Villas and apartments around a green park and a lagoon, surrounded by mountains, 5–15 minutes from the beach. Flexible plan with a 2-year post-handover instalment, or 100% payment.",
     "All residences are delivered finished, in a mostly beige palette and contemporary style. Panoramic windows frame the bay and the mountains.",
     ["landscaped park", "swimming pool", "gym", "BBQ area", "cycling and jogging tracks", "concierge", "private beach access", "restaurants and cafes", "5+ more amenities"]),
    (26, "Al Mina", "Q1 2027", "Barr Al Jissah", "Muscat Bay", "muscat-bay", "Apartments and villas",
     [("", 1900000)], "The final project in Barr Al Jissah. Payment plan 20/80 with 16% instalments and 20% down.",
     "Waterfront residences in a resort community set in a natural bay between the Gulf of Oman and the Al Hajar Mountains. Designer finishes and panoramic sea views.",
     ["marina", "swimming pool", "promenade", "private beach access", "Hilton hotel infrastructure", "fully equipped gym", "parking"]),
    (28, "Solaris", "Handover 2 years after down payment", "Orascom", "Jebel Sifah", "jebel-sifah", "Apartments",
     [("", 225000)], "Payment plan 10/90 over 2 years, quarterly payments from 11.25%.",
     "A 4-storey complex on the Arabian Sea coast, within walking distance of both the beach and the golf course.",
     ["jogging track", "swimming pool", "spa", "fully equipped gym"]),
    (29, "Olive Farms", "Handover 3 years after down payment", "Orascom", "Jebel Sifah", "jebel-sifah", "Villas",
     [("", 350000)], "3-year payment plan: 10% down, then 12 quarterly payments of 7.5%. A villa with rental potential also qualifies the owner for residency.",
     "46 single-storey villas with 1–3 bedrooms and functional layouts. The patio takes a pool and a barbecue area; the project team can help with landscaping.",
     ["children’s playground", "recreation areas", "parking", "landscaped walkways"]),
    (30, "Raya", "Handover 2 years after down payment", "Orascom", "Jebel Sifah", "jebel-sifah", "Villas",
     [("", 570000)], "Payment plan 10/90 over 2.9 years, quarterly payments of 8.2%.",
     "Villas with pools in a seaside resort area with a private beach and a golf club. Every home has a private pool and a green patio.",
     ["jogging track", "swimming pool", "BBQ area", "fully equipped gym", "golf course", "yoga zone", "landscaped gardens"]),
    (32, "Central 7", "Q1 2027", "Wujha", "Knowledge Oasis", "knowledge-oasis", "Offices",
     [("", 105000)], "A seven-storey Tier 1 business centre with a pool and restaurants inside the tech park. 20% down, the balance in equal instalments over 30 months.",
     "Offices from 355 to 6,823 sq ft: ceilings over 4 metres, floor-to-ceiling windows, open layouts and 8 high-speed lifts.",
     ["cafe and restaurants", "swimming pool", "lobby", "gym", "parking", "lounge"]),
    (33, "Uptown Muscat", "Q1 2027", "Wujha", "Knowledge Oasis", "knowledge-oasis", "Apartments",
     [("", 140000)], "Low-rise complex of 445 residences in the growing Knowledge Oasis community. Payment plan 15/85 over 5 years, 15% down.",
     "1–3 bedroom apartments with balconies and panoramic windows, plus two-storey duplexes with private terraces. Interiors in a light neutral palette.",
     ["park", "swimming pool", "lobby", "gym", "parking", "lounge", "landscaped gardens", "children’s playgrounds", "clubhouse"]),
    (35, "Alef Qurum Residence", "Q2 2029", "Rozal Development", "Telal Al Qurum", "other", "Apartments",
     [("", 112300)], "Low-rise apartments overlooking the boulevard and park in Telal Al Qurum.",
     "32 residences with 1–3 bedrooms. The facade combines wood- and stone-effect materials in layered volumes; floor-to-ceiling glazing opens onto the district’s green spaces.",
     ["indoor pool", "gym", "gated grounds", "spacious lobby", "ground-floor retail", "mosque", "access control"]),
    (36, "Husn Al Zain", "Q4 2027", "Zain Property Development", "Bidbid", "other", "Villas",
     [("", 124500)], "Villas at the foot of the Al Hajar Mountains in the Bidbid area.",
     "637 villas with 3 or 5 bedrooms. Clean geometry with an asymmetric composition: milky and olive facades, dark window frames, slats and pergolas. Each villa has a garden and a terrace.",
     ["kindergarten and playground", "sports courts", "lounge areas", "walking trails and cycling path", "shops", "mosque", "access control"]),
    (37, "Nismat Zain", "Q4 2033", "Zain Property Development", "Sur", "other", "Villas and townhouses",
     [("", 130500)], "Villas and townhouses in Sur, Arab Tourism Capital 2024, on the Gulf of Oman.",
     "358 villas and townhouses with 3–5 bedrooms. Contemporary lines with Eastern minimalism: white facades with blue accents around the windows. Terraces, parking and a rooftop area.",
     ["children’s playground", "walking and cycling paths", "landscaped park", "leisure areas", "shops", "mosque", "access control"]),
    (38, "Yamal", "Q1 2030", "Talaat Moustafa Group", "Seeb", "other", "Apartments, villas and townhouses",
     [("", 166400)], "A resort quarter with a marina and yacht club on the Seeb shore.",
     "6,220 residences: 1–3 bedroom apartments and villas with 4–8 bedrooms. Light facades and floor-to-ceiling glazing open onto the Gulf of Oman; private terraces extend the living space outdoors.",
     ["pools with sun terraces", "hotel services", "children’s playgrounds", "sports courts", "entertainment areas", "shops and cafes", "yacht club and marina"]),
    (39, "Telal Al Qurm", "Q2 2028", "Alargan Towell", "Telal Al Qurum", "other", "Apartments",
     [("", 215000)], "A private community with clubhouses, a landscaped park, pools and a sports complex. Payment plan 80/20 over 2 years plus 6 months post-handover, 20% down.",
     "1–4 bedroom apartments from 667 to 2,972 sq ft. 10 minutes to Qurum beach, 20 minutes to MCT Airport; badminton academy, football stadium and Sabco Centre nearby. Planned: a retail promenade, a green amphitheatre and two luxury hotels.",
     ["outdoor pool", "landscaped park", "clubhouse with lounges and game room", "sports fields", "retail promenade"]),
    (40, "The Residences Mandarin Oriental", "Completed", "Eagle Hills", "Shatti Al Qurum", "other", "Branded apartments",
     [("", 445000)], "Resort complex with its own beach a 5-minute walk away. Payment plan 93.75/6.25: 25% down, 1.5-year post-handover instalment.",
     "5 minutes to the Royal Opera, 20 minutes to MCT Airport; luxury hotels, malls and the Wadi Adai reserve nearby. Contemporary finishes with Eastern accents; windows face the sea, the beach and the mountains.",
     ["swimming pool", "private beach", "gym", "24/7 concierge", "spa", "24/7 room service", "10+ more amenities"]),
    (43, "The Sea Front Residences", "Q4 2027", "Al Zaid", "Taqah", "salalah", "Furnished studios · 94 residences",
     [("", 110000)], "Low-rise beachfront complex of 94 furnished studios in Taqah, southern Oman. Payment plan 25/75 over 2 years, 25% down; discounts for full payment.",
     "Every apartment comes fully furnished, ready to move into or let out. Built-in appliances throughout; windows and balconies face the sea, the beach and the landscape.",
     ["beach", "swimming pool", "market", "landscaped gardens", "airport transfer", "lounge terraces", "gym", "spa", "conference room", "10+ more amenities"]),
    (44, "Taqah Long Beach", "Q4 2026", "Al Zaid", "Taqah", "salalah", "Apartments",
     [("", 204000)], "A seafront resort house with a private beach and club amenities in Taqah, near Salalah. Payment plan 96.25/3.75 over 20 months: 25% down, then 3.75% monthly.",
     "Studios and 1–3 bedroom apartments from 710 to 1,485 sq ft, all with balconies facing the Arabian Sea or the mountains; two-level units available. 25 minutes to Salalah, 35 to SLL airport; Wadi Darbat and coastal cafes nearby.",
     ["private beach", "rooftop pool", "restaurant", "airport transfers", "landscaped gardens", "fitness centre", "spa", "business lounge", "10+ more amenities"]),
    (45, "Taqah Long Beach Boutique", "Q3 2026", "Al Zaid", "Taqah", "salalah", "Studios",
     [("", 204000)], "A 5-storey club house with 29 studios, rooftop pool and gardens by the sea in Taqah, near Salalah. Payment plan: 1.5-year instalment, 50% down.",
     "Studios of 1,119–1,130 sq ft, each with a balcony facing the Arabian Sea or the mountains. 25 minutes to Salalah, 35 to SLL airport; a sea observation deck, waterfalls and Wadi Darbat nearby.",
     ["rooftop infinity pool", "spa", "beach", "airport transfers", "children’s room", "mini-market", "fitness club", "10+ more amenities"]),
    (46, "Amazi Hawana Salalah", "Handover 3 years after down payment", "Orascom", "Salalah", "salalah", "Villas",
     [("", 302000)], "Payment plan 20/80 over 3 years, quarterly payments from 2.5%.",
     "Villas around a man-made lagoon on the Arabian Sea, with private beaches. A walkable community linked through the lagoon to a 170-berth marina, 7 km of beach, an aquapark and 4- and 5-star hotels. Buy a completed villa, or a plot built by the developer to your specification.",
     ["beach", "swimming pool", "concierge", "spa", "private parking at each villa", "fully equipped gym", "5+ more amenities"]),
    (47, "Lubana Island", "Handover 3 years after down payment", "Orascom", "Salalah", "salalah", "Apartments and villas",
     [("", 258000)], "A separate part of the larger Amazi Hawana Salalah project, with access to all of its infrastructure. Payment plan with a 3-year instalment and 10% down.",
     "Detached villas and connected chalets with 1–3 bedrooms. All residences face the water, with gardens and private courtyards with pool areas.",
     ["swimming lagoons", "kayaking waterways", "all Amazi amenities: pools, beach club, wellness centre with gym and spa"]),
    (48, "Mira Ocean Estates", "Q4 2028", "MIRA Development", "Salalah", "salalah", "Apartments, villas and townhouses",
     [("", None)], "Residences with a private beach and a 5-star hotel in Salalah, on the Arabian Sea.",
     "263 residences: studios, 1–2 bedroom apartments, villas and townhouses. The stepped composition opens toward the sea, with beige facades and ornamental panels. Interiors by ELIE SAAB Maison, Trussardi Casa and John Richmond.",
     ["pools with sun terraces", "private beach", "gym and spa", "medical wellness centre", "five-star hotel", "concierge", "shops and restaurants"]),
]

e = html.escape


def usd(n):
    return f"${n:,.0f}"


def wa_link(text):
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(text)


def kind(p):
    t = p[6].lower()
    k = []
    if "office" in t:
        k.append("office")
    if "apartment" in t or "studio" in t:
        k.append("apartment")
    if "villa" in t or "townhouse" in t:
        k.append("villa")
    return " ".join(k)


def card(p):
    page, name, handover, dev, loc, dk, typ, prices, lead, desc, amen = p
    min_price = min((v for _, v in prices if v), default=0)
    price_html = []
    for label, v in prices:
        if v is None:
            price_html.append('<span class="price">Price on request</span>')
        else:
            lab = f'<small>{e(label)} from</small>' if label else '<small>from</small>'
            price_html.append(f'<span class="price">{lab}{usd(v)}</span>')
    img = f"img/p{page:02d}"
    thumbs = "".join(
        f'<button type="button" class="th{" on" if i == 1 else ""}" data-src="{img}-{i}.jpg" aria-label="Photo {i}">'
        f'<img src="{img}-{i}.jpg" alt="" loading="lazy" width="240" height="196"></button>'
        for i in (1, 2, 3))
    amen_html = "".join(f"<li>{e(a)}</li>" for a in amen)
    msg = f"Hello, I'm interested in {name} ({loc}, Oman) from your Oman catalog. Please send details."
    return f'''
<article class="proj" id="p-{page}" data-district="{dk}" data-price="{min_price}" data-kind="{kind(p)}">
  <div class="media">
    <div class="main"><img src="{img}-1.jpg" alt="{e(name)}, {e(loc)}" loading="lazy" width="1200" height="698"></div>
    <div class="thumbs">{thumbs}</div>
  </div>
  <div class="body">
    <div class="chips"><span>{e(handover)}</span><span>{e(dev)}</span><span class="loc">{e(loc)}</span></div>
    <h3 class="display">{e(name)}</h3>
    <div class="type">{e(typ)}</div>
    <div class="prices">{"".join(price_html)}</div>
    <p class="lead">{e(lead)}</p>
    <p class="desc">{e(desc)}</p>
    <ul class="amen">{amen_html}</ul>
    <a class="btn btn-solid btn-sm" href="{e(wa_link(msg))}" target="_blank" rel="noopener">Enquire on WhatsApp</a>
  </div>
</article>'''


def build():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    by_d = {d[0]: [p for p in PROJECTS if p[5] == d[0]] for d in DISTRICTS}
    assert sum(len(v) for v in by_d.values()) == len(PROJECTS) == 35

    filters = '<button type="button" class="on" data-f="all">All <i>35</i></button>' + "".join(
        f'<button type="button" data-f="{k}">{e(n)} <i>{len(by_d[k])}</i></button>' for k, n, *_ in DISTRICTS)

    sections = []
    for k, n, eyebrow, tag, banner in DISTRICTS:
        cards = "".join(card(p) for p in by_d[k])
        sections.append(f'''
<section class="district" id="{k}" data-district="{k}">
  <div class="banner" style="background-image:url('img/d-{banner}.jpg')">
    <div class="wrap"><div class="eyebrow light">{e(eyebrow)}</div><h2 class="display">{e(n)}</h2><p>{e(tag)}</p></div>
  </div>
  <div class="wrap"><div class="list">{cards}</div></div>
</section>''')

    ld = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": "Top residential developments in Oman — Autumn 2026",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p[1], "url": f"{SITE}#p-{p[0]}"}
                            for i, p in enumerate(PROJECTS)],
    }

    tpl = open(os.path.join(root, "tools", "oman_template.html"), encoding="utf-8").read()
    out = (tpl.replace("{{FILTERS}}", filters)
              .replace("{{SECTIONS}}", "".join(sections))
              .replace("{{LDJSON}}", json.dumps(ld, ensure_ascii=False))
              .replace("{{WA_GENERAL}}", e(wa_link("Hello, I'd like to discuss property in Oman from your Autumn 2026 catalog."))))
    with open(os.path.join(root, "oman", "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print("oman/index.html written,", len(PROJECTS), "projects")


if __name__ == "__main__":
    build()
