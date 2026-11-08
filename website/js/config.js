/**
 * Nepali Rhyme Hub — Website Configuration & Catalog (2026)
 */

const SITE_CONFIG = {
  brand: {
    nameNepali: "नेपाली राइम हब",
    nameEnglish: "Nepali Rhyme Hub",
    taglineNepali: "गाऔँ · नाचौँ · सिकौँ!",
    taglineEnglish: "Sing · Dance · Learn!",
    description: "१००% मौलिक, सुरक्षित, आधुनिक र रमाइलो नेपाली बालगीत तथा कार्टुन मञ्च।",
  },
  social: {
    youtube: "https://www.youtube.com/@NepaliRhymeHub",
    tiktok: "https://www.tiktok.com/@nepaliryhmehub",
    instagram: "https://www.instagram.com/nepalirhymehub/",
    facebook: "https://business.facebook.com/latest/home?asset_id=1416157004919997",
  },
  catalog: [
    {
      id: "bhailo_e_bhaili",
      category: "festivals",
      titleNepali: "झिलिमिली भैलो!",
      titleEnglish: "Bhailo E Bhaili (Tihar Special)",
      badge: "तिहार विशेष",
      duration: "5:15",
      bpm: 105,
      key: "D Major",
      thumbnail: "assets/thumbnails/bhailo-thumb-A.jpg",
      description: "लक्ष्मी पूजाको रात आरभ र आर्यासँग घरघरमा भैलो खेल्दै दियो, सेलरोटी र सयपत्रीको रमाइलो उत्सव!",
      lyricsSnippet: `झिलिमिली! झिलिमिली! भैलो आयो, भैलो! 🪔
दियो बल्यो घरघर, मन भयो उज्यालो!
हरियो गोबरले लिपेको आँगन,
लक्ष्मी पूजा गरेको, सुनौलो बिहानी!
च्याप्प-च्याप्प ताली बजाउँदै नाचौँ साथी सारा भाई!`
    },
    {
      id: "hamro_sahar_nepal_yatra",
      category: "urban",
      titleNepali: "हाम्रो सहर, हाम्रो देश!",
      titleEnglish: "Hamro Sahar, Hamro Desh (Modern Nepal Tour)",
      badge: "नयाँ बालगीत",
      duration: "4:48",
      bpm: 120,
      key: "D Major",
      thumbnail: "assets/thumbnails/hamro_sahar-thumb-A.jpg",
      description: "काठमाडौँको बिजुली गाडीदेखि पाटन, पोखराको फेवा ताल, जनकपुरको रेल हुँदै सगरमाथासम्मको आधुनिक बाल यात्रा!",
      lyricsSnippet: `ए है! सहर आयो, देश आयो!
घुमघुम गाडी आयो! (पिँप-पिँप!)
पूर्व, पश्चिम, हिमाल, तराई,
हाँस्दै नाचौँ साथी सारा भाई!
काठमाडौँको सहर सुन्दर, हरियो बिजुली गाडी,
धरहराको बत्ती बल्यो, धपधप बत्ती बल्यो!`
    },
    {
      id: "chhath_parva_aayo",
      category: "festivals",
      titleNepali: "छमछम छठ पर्व आयो!",
      titleEnglish: "Chhath Parva Aayo (Sun Festival of Mithila)",
      badge: "छठ विशेष",
      duration: "3:40",
      bpm: 110,
      key: "G Major",
      thumbnail: "assets/thumbnails/chhath-thumb-A.jpg",
      description: "कमल फुल्यो पोखरीमा, दियो बल्यो डिलैमा! जनकपुरको पवित्र गङ्गा सागरमा सूर्यदेवलाई अर्घ्य दिँदै ठेकुवा र सद्भावको पर्व।",
      lyricsSnippet: `छमछम छमछम छठ आयो, दियो बल्यो डिलैमा,
कमल फुल्यो पोखरीमा, सूर्य देवको पूजामा!
ठेकुवा मिठो, फलफूल राम्रो, सबलाई शुभकामना!`
    },
    {
      id: "deusi_bhan_mera_bhai",
      category: "festivals",
      titleNepali: "देउसीरे भन मेरा भाइ!",
      titleEnglish: "Deusi Bhan Mera Bhai",
      badge: "देउसी धमाका",
      duration: "4:12",
      bpm: 115,
      key: "C Major",
      thumbnail: "assets/thumbnails/deusi-thumb-A.jpg",
      description: "अघि-अघि आरभ मादल बजाउँदै, पछि-पछि साथीहरू देउसीरे भन्दै आशीष बाँड्दै गाउँ र सहरमा रमाइलो!",
      lyricsSnippet: `आहै भन मेरा भाइ हो— देउसीरे!
भन न भन राम्ररी भन— देउसीरे!
रातो माटो, चिप्लो बाटो, देउसी खेल्न आयौँ!`
    },
    {
      id: "sabun_pani_chhamchham",
      category: "habits",
      titleNepali: "साबुन पानी छमछम",
      titleEnglish: "Sabun Pani Chhamchham (Clean Habits Song)",
      badge: "असल बानी",
      duration: "2:50",
      bpm: 122,
      key: "F Major",
      thumbnail: "assets/thumbnails/hamro_sahar-thumb-B.jpg",
      description: "खाना खानु अघि र पछि बीस सेकेन्ड मिचीमिची हात धुने, स्वस्थ र बलियो बन्ने रमाइलो बानी गीत।",
      lyricsSnippet: `साबुन पानी छमछम, हात धोऔँ चट्ट!
किटाणु सबै भाग्छन्, स्वास्थ्य हुन्छ पट्ट!
नङ सफा, दाँत सेतो, बाबु कति चिटिक्क!`
    },
    {
      id: "gai_ko_bachho",
      category: "nature",
      titleNepali: "गाईको बाच्छो उफ्रिन्छ",
      titleEnglish: "Gai Ko Bachho Ufrinchha",
      badge: "जनावर बालगीत",
      duration: "3:10",
      bpm: 108,
      key: "D Major",
      thumbnail: "assets/thumbnails/bhailo-thumb-B.jpg",
      description: "हरियो घाँस चर्दै, घाँटीमा घण्टी बजाउँदै आँगनमा रमाउने सानो मायालु बाच्छोको गीत।",
      lyricsSnippet: `गाईको बाच्छो उफ्रिन्छ, टिनटिन घण्टी बज्दछ,
आमाको दूध खाएर, पुच्छर हल्लाउँदै दगुर्दछ!`
    }
  ],
  characters: [
    {
      name: "Aarav (आरभ)",
      age: "७ वर्ष",
      city: "काठमाडौँ (बानेश्वर)",
      role: "प्रविधि र सङ्गीत प्रेमी",
      emoji: "🎧",
      desc: "पहेँलो हुडी, चम्किलो स्नीकर्स र हेडफोन मन पराउने आरभ मादल र कम्प्युटर कोडिङ दुवैमा सिपालु छ।"
    },
    {
      name: "Sneha (स्नेहा)",
      age: "८ वर्ष",
      city: "ललितपुर (पाटन)",
      role: "चित्रकला र वास्तुविद्",
      emoji: "🎨",
      desc: "डेनिम ज्याकेट र डिजिटल ट्याब्लेट बोक्ने स्नेहा मन्दिरको काठको कला र सहरका रङ्गीन भित्ते चित्र कोर्न मन पराउँछिन्।"
    },
    {
      name: "Tenzing (तेन्जिङ)",
      age: "७ वर्ष",
      city: "पोखरा (लेकसाइड)",
      role: "पहाड यात्री र स्केटबोर्डर",
      emoji: "🛹",
      desc: "हल्का नीलो पफर भेस्ट र स्केटबोर्ड बोक्ने तेन्जिङ फेवा तालको किनारमा खेल्दै तुङ्नाको धुन बजाउँछ।"
    },
    {
      name: "Rhea (रिया)",
      age: "६ वर्ष",
      city: "जनकपुरधाम",
      role: "विज्ञान र तारा अनुसन्धाता",
      emoji: "🔭",
      desc: "मिथिला कलाको डङ्गरी लगाउने रिया टेलिस्कोपबाट ताराहरू हेर्न र गङ्गा सागरको साँझ रम्न मन पराउँछिन्।"
    },
    {
      name: "Bikash (बिकास)",
      age: "८ वर्ष",
      city: "चितवन र बुटवल",
      role: "प्रकृति र वन्यजन्तु रक्षक",
      emoji: "🚲",
      desc: "सुन्तले साइकल कुदाउने बिकास चितवनका एकसिङ्गे गैँडा जोगाउन र थारु लौरो नाँच नाच्न माहिर छ।"
    },
    {
      name: "Puntu (पुन्टु)",
      age: "सानो साथी",
      city: "हिमाली वन",
      role: "ब्रान्ड हिरो (रेड पाण्डा)",
      emoji: "🐾",
      desc: "सानो हरियो झोला र मिनी हेडफोन लगाउने हाम्रो प्यारो रेड पाण्डा, जसले सधैँ मादल बजाएर साथीहरूलाई हँसाउँछ।"
    }
  ]
};
