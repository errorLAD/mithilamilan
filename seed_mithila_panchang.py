import os
import sys
import datetime
import django

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redditClone.settings')
django.setup()

from mithila_panchang.models import (
    PanchangSource, ScannedPanchangPage, PanchangYear, PanchangMonth,
    PanchangDay, Festival, MuhuratCategory, MuhuratDate, MithilaSong
)

def seed_data():
    print("Beginning Mithila Panchang Data Seeding...")

    # 1. Panchang Source
    source, _ = PanchangSource.objects.get_or_create(
        name="मैथिली पंचांग (उर्वशी प्रकाशन)",
        defaults={
            'year_label': "२०२६ - २०२७ ई० (सन १४३४ साल)",
            'publisher': "उर्वशी प्रकाशन, पटना",
            'editor': "पं० सचिदानन्द झा (गणित, फलित)",
            'compiler': "पं० गोपीकान्त झा",
            'description': "मिथिलादेशीय मकरन्दानुसार पारम्परिक मैथिली पंचांग। सन् १४३४ साल (अंग्रेजी २०२६-२०२७ ई०)।"
        }
    )

    # 2. Scanned Pages (1 to 34)
    page_titles = {
        1: "शीर्षक पृष्ठ / आवरण",
        2: "१४३४ सालक पदाधिकारी एवं विवाह, मुंडन, उपनयन, द्विरागमन शुद्ध समय",
        3: "सिद्धयादियोग, अधपहरा एवं दिकशूल विचार",
        4: "१४३४ सालक राशिफल (मेष से कन्या)",
        5: "१४३४ सालक राशिफल (तुला से मीन)",
        6: "श्रावण कृष्णपक्ष (जुलाई-अगस्त २०२६)",
        7: "श्रावण शुक्लपक्ष (अगस्त २०२६)",
        8: "भाद्रपद शुक्लपक्ष (सितंबर २०२६)",
        9: "आश्विन कृष्णपक्ष (सितंबर-अक्टूबर २०२६)",
        10: "कार्तिक कृष्णपक्ष (अक्टूबर-नवंबर २०२६)",
        11: "कार्तिक शुक्लपक्ष (नवंबर २०२६)",
        12: "अगहन कृष्णपक्ष (नवंबर-दिसंबर २०२६)",
        13: "अगहन शुक्लपक्ष (दिसंबर २०२६)",
        14: "पौष कृष्णपक्ष (दिसंबर-जनवरी २०२६-२७)",
        15: "पौष शुक्लपक्ष (जनवरी २०२७)",
        16: "माघ कृष्णपक्ष (जनवरी-फरवरी २०२७)",
        17: "माघ शुक्लपक्ष (फरवरी २०२७)",
        18: "फाल्गुन कृष्णपक्ष (फरवरी-मार्च २०२७)",
        19: "फाल्गुन शुक्लपक्ष (मार्च २०२७)",
        20: "चैत्र कृष्णपक्ष (मार्च-अप्रैल २०२७)",
        21: "चैत्र शुक्लपक्ष (अप्रैल २०२७)",
        22: "वैशाख कृष्णपक्ष (अप्रैल-मई २०२७)",
        23: "वैशाख शुक्लपक्ष (मई २०२७)",
        24: "ज्येष्ठ कृष्णपक्ष (मई-जून २०२७)",
        25: "ज्येष्ठ शुक्लपक्ष (जून २०२७)",
        26: "आषाढ कृष्णपक्ष (जून-जुलाई २०२७)",
        27: "आषाढ शुक्लपक्ष (जुलाई २०२७)",
        28: "आवश्यक व्यावहारिक मन्त्र (रक्षाबंधन, कुशोत्पाटन, चौठचन्द्र)",
        29: "देवोत्थान, घटदान, दूर्वाक्षत मन्त्र",
        30: "वैतरणी दान एवं दाह-संस्कार",
        31: "मुहूर्त विचार (विवाह, द्विरागमन, उपनयन, मुंडन, यात्रा)",
        32: "नवग्रह रत्न एवं जप मन्त्र",
        33: "१४३४ सालक पर्व सूची (पाबनि-तिहार तालिका)",
        34: "उर्वशी प्रकाशित पुस्तक सूची"
    }

    scanned_pages_dict = {}
    for p_num in range(1, 35):
        img_name = f"panch_ocr/page-0{p_num}.jpg" if p_num < 10 else f"panch_ocr/page-{p_num}.jpg"
        sp, _ = ScannedPanchangPage.objects.get_or_create(
            page_number=p_num,
            defaults={
                'source': source,
                'title': page_titles.get(p_num, f"पृष्ठ {p_num}"),
                'image_path': img_name,
                'notes': f"प्रमाणित पृष्ठ {p_num}"
            }
        )
        scanned_pages_dict[p_num] = sp

    # 3. Panchang Year
    pyear, _ = PanchangYear.objects.get_or_create(
        gregorian_year=2026,
        defaults={
            'title_hi': "सन १४३४ साल (अंग्रेजी २०२६ - २०२७ ई०)",
            'vikram_samvat': "२०८३-८४",
            'saka_samvat': "१९४८",
            'king_planet': "शनि",
            'minister_planet': "मंगल",
            'is_active': True
        }
    )

    # 4. Panchang Months (12 Months)
    months_data = [
        ("बैशाख", "वैशाख", "Baisakh", 1, "अप्रैल – मई", "April – May"),
        ("जेठ", "ज्येष्ठ", "Jeth", 2, "मई – जून", "May – June"),
        ("असाढ़", "आषाढ", "Asadh", 3, "जून – जुलाई", "June – July"),
        ("साओन", "श्रावण", "Saon", 4, "जुलाई – अगस्त", "July – August"),
        ("भादो", "भाद्रपद", "Bhado", 5, "अगस्त – सितंबर", "August – September"),
        ("आसिन", "आश्विन", "Aasin", 6, "सितंबर – अक्टूबर", "September – October"),
        ("कार्तिक", "कार्तिक", "Kartik", 7, "अक्टूबर – नवंबर", "October – November"),
        ("अगहन", "मार्गशीर्ष", "Agahan", 8, "नवंबर – दिसंबर", "November – December"),
        ("पूस", "पौष", "Poos", 9, "दिसंबर – जनवरी", "December – January"),
        ("माघ", "माघ", "Magh", 10, "जनवरी – फरवरी", "January – February"),
        ("फागुन", "फाल्गुन", "Fagun", 11, "फरवरी – मार्च", "February – March"),
        ("चैत्र", "चैत्र", "Chaitra", 12, "मार्च – अप्रैल", "March – April"),
    ]

    months_dict = {}
    for m_hi, m_mai, m_en, m_order, gr_hi, gr_en in months_data:
        pm, _ = PanchangMonth.objects.get_or_create(
            year=pyear,
            month_order=m_order,
            defaults={
                'name_hi': m_hi,
                'name_mai': m_mai,
                'name_en': m_en,
                'gregorian_range_hi': gr_hi,
                'gregorian_range_en': gr_en,
            }
        )
        months_dict[m_hi] = pm

    # 5. Muhurat Categories
    categories_data = [
        ("विवाहक मुहूर्त", "विवाह", "Marriage Muhurat", "vivah", "fa-ring", "विवाह हेतु प्रमाणित शुद्ध शुभ तिथियाँ", 1),
        ("मुड़न मुहूर्त", "मुंडन", "Mundan Muhurat", "mundan", "fa-scissors", "चूड़ाकर्म / मुंडन संस्कार शुभ तिथियाँ", 2),
        ("उपनयन मुहूर्त", "उपनयन", "Upanayan Muhurat", "upanayan", "fa-om", "यज्ञोपवीत / जनेऊ संस्कार शुभ तिथियाँ", 3),
        ("गृहप्रवेश मुहूर्त", "गृहप्रवेश", "Grihapravesh Muhurat", "grihapravesh", "fa-house", "नूतन गृहप्रवेश शुभ मुहूर्त", 4),
        ("द्विरागमन", "द्विरागमन", "Dviragaman", "dviragaman", "fa-arrows-rotate", "पारम्परिक द्विरागमन / गौनहा तिथियाँ", 5),
        ("गृहारंभ", "गृहारंभ", "Griharambha", "griharambha", "fa-compass", "भवन निर्माण / गृहारंभ मुहूर्त", 6),
    ]

    cat_dict = {}
    for c_hi, c_mai, c_en, c_slug, c_icon, c_desc, c_order in categories_data:
        mc, _ = MuhuratCategory.objects.get_or_create(
            slug=c_slug,
            defaults={
                'name_hi': c_hi,
                'name_mai': c_mai,
                'name_en': c_en,
                'icon': c_icon,
                'description': c_desc,
                'order': c_order
            }
        )
        cat_dict[c_slug] = mc

    # 6. Seed Specific Muhurat Dates from Page 2 & Monthly Tables
    page2_ref = scanned_pages_dict.get(2)

    vivah_dates = [
        # 2026
        (datetime.date(2026, 11, 22), "अगहन", "कृष्ण", "प्रतिपदा", "रविवार", "रोहिणी", ""),
        (datetime.date(2026, 11, 25), "अगहन", "कृष्ण", "प्रतिपदा", "बुधवार", "रोहिणी", ""),
        (datetime.date(2026, 11, 26), "अगहन", "कृष्ण", "द्वितीया", "बृहस्पतिवार", "मृगशिरा", ""),
        (datetime.date(2026, 11, 30), "अगहन", "कृष्ण", "षष्ठी", "सोमवार", "पुष्य", ""),
        (datetime.date(2026, 12, 4), "अगहन", "कृष्ण", "दशमी", "शुक्रवार", "हस्त", ""),
        (datetime.date(2026, 12, 6), "अगहन", "कृष्ण", "द्वादशी", "रविवार", "स्वाती", ""),
        (datetime.date(2026, 12, 9), "अगहन", "शुक्ल", "प्रतिपदा", "बुधवार", "ज्येष्ठा", ""),
        (datetime.date(2026, 12, 10), "अगहन", "शुक्ल", "द्वितीया", "बृहस्पतिवार", "मूल", ""),
        (datetime.date(2026, 12, 11), "अगहन", "शुक्ल", "तृतीया", "शुक्रवार", "पूर्वाषाढा", ""),
        (datetime.date(2026, 12, 14), "अगहन", "शुक्ल", "षष्ठी", "सोमवार", "धनिष्ठा", ""),
        # 2027
        (datetime.date(2027, 1, 16), "पौष", "शुक्ल", "अष्टमी", "शनिवार", "अश्विनी", ""),
        (datetime.date(2027, 1, 24), "माघ", "कृष्ण", "तृतीया", "रविवार", "मघा", ""),
        (datetime.date(2027, 1, 28), "माघ", "कृष्ण", "सप्तमी", "बृहस्पतिवार", "स्वाती", ""),
        (datetime.date(2027, 1, 29), "माघ", "कृष्ण", "अष्टमी", "शुक्रवार", "स्वाती", ""),
        (datetime.date(2027, 1, 31), "माघ", "कृष्ण", "दशमी", "रविवार", "अनुराधा", ""),
        (datetime.date(2027, 2, 7), "माघ", "शुक्ल", "प्रतिपदा", "रविवार", "धनिष्ठा", ""),
        (datetime.date(2027, 2, 10), "माघ", "शुक्ल", "चतुर्थी", "बुधवार", "उत्तरभाद्रपद", ""),
        (datetime.date(2027, 2, 11), "माघ", "शुक्ल", "पंचमी", "बृहस्पतिवार", "रेवती", ""),
        (datetime.date(2027, 2, 15), "माघ", "शुक्ल", "नवमी", "सोमवार", "रोहिणी", ""),
        (datetime.date(2027, 2, 19), "माघ", "शुक्ल", "त्रयोदशी", "शुक्रवार", "पुष्य", ""),
        (datetime.date(2027, 2, 21), "माघ", "शुक्ल", "पूर्णिमा", "रविवार", "मघा", ""),
        (datetime.date(2027, 2, 22), "फाल्गुन", "कृष्ण", "प्रतिपदा", "सोमवार", "पूर्वाफाल्गुनी", ""),
        (datetime.date(2027, 2, 24), "फाल्गुन", "कृष्ण", "तृतीया", "बुधवार", "हस्त", ""),
        (datetime.date(2027, 2, 25), "फाल्गुन", "कृष्ण", "चतुर्थी", "बृहस्पतिवार", "चित्रा", ""),
        (datetime.date(2027, 2, 28), "फाल्गुन", "कृष्ण", "सप्तमी", "रविवार", "अनुराधा", ""),
    ]

    for d, m_name, pak, tithi, wk, nak, nts in vivah_dates:
        MuhuratDate.objects.get_or_create(
            category=cat_dict['vivah'],
            gregorian_date=d,
            defaults={
                'mithila_month_name': m_name,
                'paksha': pak,
                'tithi_name': tithi,
                'weekday_name': wk,
                'nakshatra_name': nak,
                'notes': nts,
                'source_page': page2_ref,
                'source_reference_text': "मैथिली पंचांग, पृष्ठ २ (विवाहक दिन)",
                'verification_status': 'VERIFIED',
                'is_published': True
            }
        )

    mundan_dates = [
        (datetime.date(2026, 11, 26), "अगहन", "कृष्ण", "द्वितीया", "बृहस्पतिवार", "मृगशिरा"),
        (datetime.date(2026, 12, 14), "अगहन", "शुक्ल", "षष्ठी", "सोमवार", "धनिष्ठा"),
        (datetime.date(2027, 1, 20), "पौष", "शुक्ल", "द्वादशी", "बुधवार", "रोहिणी"),
        (datetime.date(2027, 1, 27), "माघ", "कृष्ण", "षष्ठी", "बुधवार", "हस्त"),
        (datetime.date(2027, 2, 6), "माघ", "कृष्ण", "अमावास्या", "शनिवार", "धनिष्ठा"),
        (datetime.date(2027, 2, 11), "माघ", "शुक्ल", "पंचमी", "बृहस्पतिवार", "रेवती"),
        (datetime.date(2027, 2, 16), "माघ", "शुक्ल", "दशमी", "मंगलवार", "मृगशिरा"),
        (datetime.date(2027, 2, 19), "माघ", "शुक्ल", "त्रयोदशी", "शुक्रवार", "पुष्य"),
    ]

    for d, m_name, pak, tithi, wk, nak in mundan_dates:
        MuhuratDate.objects.get_or_create(
            category=cat_dict['mundan'],
            gregorian_date=d,
            defaults={
                'mithila_month_name': m_name,
                'paksha': pak,
                'tithi_name': tithi,
                'weekday_name': wk,
                'nakshatra_name': nak,
                'source_page': page2_ref,
                'source_reference_text': "मैथिली पंचांग, पृष्ठ २ (मुंडनक दिन)",
                'verification_status': 'VERIFIED',
                'is_published': True
            }
        )

    upanayan_dates = [
        (datetime.date(2027, 2, 7), "माघ", "शुक्ल", "प्रतिपदा", "रविवार", "धनिष्ठा", "(छ०)"),
        (datetime.date(2027, 2, 11), "माघ", "शुक्ल", "पंचमी", "बृहस्पतिवार", "रेवती", "(छ०)"),
        (datetime.date(2027, 2, 17), "माघ", "शुक्ल", "एकादशी", "बुधवार", "आद्रा", ""),
        (datetime.date(2027, 3, 17), "फाल्गुन", "शुक्ल", "नवमी", "बुधवार", "पुनर्वसु", "(क्ष०वै०)"),
        (datetime.date(2027, 3, 18), "फाल्गुन", "शुक्ल", "दशमी", "बृहस्पतिवार", "पुष्य", ""),
    ]

    for d, m_name, pak, tithi, wk, nak, nts in upanayan_dates:
        MuhuratDate.objects.get_or_create(
            category=cat_dict['upanayan'],
            gregorian_date=d,
            defaults={
                'mithila_month_name': m_name,
                'paksha': pak,
                'tithi_name': tithi,
                'weekday_name': wk,
                'nakshatra_name': nak,
                'notes': nts,
                'source_page': page2_ref,
                'source_reference_text': "मैथिली पंचांग, पृष्ठ २ (उपनयनक दिन)",
                'verification_status': 'VERIFIED',
                'is_published': True
            }
        )

    # 7. Major Festivals
    festivals_list = [
        (datetime.date(2026, 8, 15), "मधुश्रावणी पूजा समाप्त", "मधुश्रावणी", "Madhushravani", "साओन", "mithila_special", "नवविवाहिता स्त्री सभक पावन पारम्परिक पूजा।", scanned_pages_dict.get(7)),
        (datetime.date(2026, 8, 28), "रक्षाबंधन एवं श्रावणी पूर्णिमा", "रक्षाबंधन", "Raksha Bandhan", "साओन", "pabni_tihar", "श्रावणी पूर्णिमा, स्नान-दान एवं रक्षाबंधन पर्व।", scanned_pages_dict.get(7)),
        (datetime.date(2026, 9, 14), "हरितालिका (तीज) व्रत", "तीज व्रत", "Hartalika Teej", "भादो", "vrat", "सौभाग्यवती स्त्री सभक निरंजला हरितालिका तीज व्रत।", scanned_pages_dict.get(8)),
        (datetime.date(2026, 9, 17), "श्री विश्वकर्मा पूजा", "विश्वकर्मा पूजा", "Vishwakarma Puja", "भादो", "puja", "शिल्पकला व यंत्रदेव विश्वकर्मा पूजा।", scanned_pages_dict.get(8)),
        (datetime.date(2026, 10, 3), "श्री जिमूतवाहन (जितिया) व्रत", "जितिया व्रत", "Jitiya Vrat", "आसिन", "vrat", "मातृगणक संतान रक्षा लेल कठोर जितिया व्रत।", scanned_pages_dict.get(9)),
        (datetime.date(2026, 11, 15), "छठि व्रत खरना", "छठ खरना", "Chhath Kharna", "कार्तिक", "pabni_tihar", "महापर्व छठि व्रतक खरना एवं सायंकालीन तैयारी।", scanned_pages_dict.get(11)),
        (datetime.date(2026, 11, 16), "छठि व्रत सायंकालीन अर्घदान", "छठि अर्घदान", "Chhath Evening Arghya", "कार्तिक", "pabni_tihar", "भगवान भास्कर लेल सायंकालीन अर्घदान।", scanned_pages_dict.get(11)),
        (datetime.date(2026, 11, 20), "देवोत्थान ११ व्रत (देवउठान)", "देवोत्थान", "Devotthan Ekadashi", "कार्तिक", "vrat", "भगवान विष्णु निद्रा सँ उठैत छथि। गृहारंभ व शुभ कार्य आरम्भ।", scanned_pages_dict.get(11)),
        (datetime.date(2026, 11, 24), "सामा पूजारम्भ व सामा विसर्जन", "सामा चकेवा", "Sama Chakeva", "कार्तिक", "mithila_special", "भ्रातृ-भगिनीक प्रेम प्रतीक सामा चकेवा पर्व।", scanned_pages_dict.get(11)),
        (datetime.date(2026, 12, 14), "श्रीसीताराम विवाहोत्सव (विवाह पंचमी)", "विवाह पंचमी", "Vivah Panchami", "अगहन", "pabni_tihar", "जनकपुरधाममे श्रीसीताराम विवाहोत्सव।", scanned_pages_dict.get(13)),
        (datetime.date(2027, 1, 15), "तिल संक्रांति / मकर संक्रांति", "तिल संक्रांति", "Til Sankranti", "माघ", "pabni_tihar", "माघ स्नानारम्भ एवं तिल संक्रांति पर्व।", scanned_pages_dict.get(15)),
        (datetime.date(2027, 2, 11), "बसंत पंचमी / सरस्वती पूजा", "सरस्वती पूजा", "Basant Panchami", "माघ", "puja", "विद्या दायिनी माँ सरस्वती पूजन एवं बसंतोत्सव।", scanned_pages_dict.get(17)),
        (datetime.date(2027, 3, 6), "महाशिवरात्रि व्रत", "महाशिवरात्रि", "Mahashivratri", "फागुन", "vrat", "भगवान शिवक पूजा व अहोरात्र शिवरात्रि व्रत।", scanned_pages_dict.get(18)),
        (datetime.date(2027, 3, 21), "होलिकादहन", "होलिकादहन", "Holika Dahan", "फागुन", "pabni_tihar", "फाल्गुनी पूर्णिमा होलिका दहन।", scanned_pages_dict.get(19)),
        (datetime.date(2027, 3, 22), "होली (रंगोत्सव)", "होली", "Holi", "फागुन", "cultural", "रंगोत्सव एवं पातरिदान।", scanned_pages_dict.get(19)),
        (datetime.date(2027, 4, 14), "सतुआईन व जुड़शीतल", "जुड़शीतल", "Jur Sital", "वैशाख", "mithila_special", "मेष संक्रांति, सतुआईन एवं मिथिलाक नूतन वर्ष जुड़शीतल।", scanned_pages_dict.get(21)),
        (datetime.date(2027, 5, 14), "जानकी नवमी / मैथिली दिवस", "जानकी नवमी", "Sita Navami / Maithili Divas", "वैशाख", "mithila_special", "माँ सीता प्राकट्य दिवस एवं मैथिली दिवस।", scanned_pages_dict.get(23)),
    ]

    for d, t_hi, t_mai, t_en, m_name, cat, desc, sp in festivals_list:
        Festival.objects.get_or_create(
            date=d,
            title_hi=t_hi,
            defaults={
                'title_mai': t_mai,
                'title_en': t_en,
                'mithila_month_name': m_name,
                'category': cat,
                'short_description': desc,
                'source_page': sp
            }
        )

    # 8. Sample Panchang Day records (2026-08-20 & surrounding dates)
    sample_days_data = [
        (datetime.date(2026, 8, 20), "साओन", "कृष्ण", "सप्तमी", "बृहस्पतिवार", "भरणी", "05:18 AM", "06:42 PM", "07:16 PM", "06:05 AM", "सिंह", "तुला"),
        (datetime.date(2026, 8, 21), "साओन", "कृष्ण", "अष्टमी", "शुक्रवार", "कृत्तिका", "05:19 AM", "06:41 PM", "08:00 PM", "07:05 AM", "सिंह", "वृश्चिक"),
        (datetime.date(2026, 8, 22), "साओन", "कृष्ण", "नवमी", "शनिवार", "रोहिणी", "05:19 AM", "06:40 PM", "08:45 PM", "08:06 AM", "सिंह", "वृश्चिक"),
        (datetime.date(2026, 11, 25), "अगहन", "कृष्ण", "प्रतिपदा", "बुधवार", "रोहिणी", "06:30 AM", "05:15 PM", "06:10 PM", "06:00 AM", "वृश्चिक", "वृष"),
    ]

    for d, m_name, pak, tithi, wk, nak, sr, ss, mr, ms, s_rashi, m_rashi in sample_days_data:
        PanchangDay.objects.get_or_create(
            date=d,
            defaults={
                'mithila_month_name': m_name,
                'paksha': pak,
                'mithila_tithi_name': tithi,
                'weekday_name': wk,
                'nakshatra_name': nak,
                'sunrise': sr,
                'sunset': ss,
                'moonrise': mr,
                'moonset': ms,
                'sun_rashi': s_rashi,
                'moon_rashi': m_rashi
            }
        )

    # 9. Seed Mithila Songs (15 YouTube Songs)
    songs_data = [
        ("H501incNC74", "मिथिलाक पावन लोकगीत", "मैथिली सुर संगीत", "लोकगीत", 1),
        ("5Jp7tGF6hbY", "मैथिली सोहर एवं विवाह गीत", "मिथिला कला संस्कृति", "सोहर / विवाह", 2),
        ("R2l4yhQLHa4", "भगवती वंदना - मिथिला भजन", "मैथिली भक्ति माला", "भजन / वंदना", 3),
        ("JD9gsauGP4Y", "मधुश्रावणी व बटगवनी गीत", "पारम्परिक मैथिली स्वर", "पारम्परिक", 4),
        ("jNOjTQfFyi8", "समदाओन - मैथिली विदाई गीत", "लोक संगीत धारा", "समदाओन", 5),
        ("uX-p-hfZH0c", "मिथिलाक पारम्परिक लोकगीत", "मैथिली संस्कृति सुर", "लोकगीत", 6),
        ("mbEfz3gsGFU", "जनकपुर धाम मैथिली गीत", "जनकपुर भक्ति संगीता", "भजन", 7),
        ("anNyfBe9QTU", "मैथिली कजरी व झूमर", "पारम्परिक लोक उत्सव", "झूमर", 8),
        ("4pomVutNeZg", "मिथिला सांस्कृतिक लोकगीत", "मिथिला स्वर धारा", "सांस्कृतिक", 9),
        ("g8Iod6tadBg", "मैथिली सोहर मंगल गीत", "सोहर मंगल गान", "सोहर", 10),
        ("bC3a5P9ZqNU", "सीता जन्म व विवाह उत्सव", "राम सीता गान", "विवाह", 11),
        ("DCaJ-2L2ro4", "मैथिली भगवती गीत संग्रह", "दुर्गा माँ वंदना", "भगवती गीत", 12),
        ("U6P-QuXm6Nw", "मिथिला की कोकिला संगीत", "शारदा सिन्हा स्वर", "लोकगीत", 13),
        ("8fikUVMIRCQ", "मैथिली लगन व समदाओन", "विवाह मंगल गान", "विवाह", 14),
        ("FPbQmReaM2Y", "मिथिलाक मधुर पारंपरिक गीत", "मैथिली विरासत संगीत", "पारम्परिक", 15),
    ]

    for v_id, title, singer, cat, ord_num in songs_data:
        MithilaSong.objects.get_or_create(
            video_id=v_id,
            defaults={
                'title': title,
                'singer': singer,
                'category': cat,
                'order': ord_num,
                'is_featured': True,
                'is_published': True
            }
        )

    print("Mithila Panchang Data Seeding Completed Successfully!")

if __name__ == '__main__':
    seed_data()
