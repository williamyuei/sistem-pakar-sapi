"""
Management command untuk mengisi data Solusi Penanganan yang komprehensif.
Data disusun berdasarkan literatur veteriner terpercaya dan best practices.

Sumber Referensi:
- MSD Veterinary Manual
- WHO/WOAH (World Organisation for Animal Health)  
- NIH (National Institutes of Health) - PubMed
- FAO (Food and Agriculture Organization)
- University Extension Services (Wisconsin, Minnesota, etc)
- Government Veterinary Guidelines (UK, Australia, USA)

Jalankan: python manage.py seed_solusi
"""
from django.core.management.base import BaseCommand
from core.models import Penyakit, SolusiPenanganan


# Data solusi penanganan untuk semua penyakit
# Format: (kode_penyakit, jenis, judul, deskripsi, prioritas, referensi)
SOLUSI_DATA = [
    # ========== P01: ANTHRAX ==========
    ("P01", "pengobatan", "Antibiotik Penisilin atau Tetrasiklin",
     "Berikan procaine penicillin G (10,000-20,000 IU/kg IM) atau oxytetracycline (10-20 mg/kg IV/IM) setiap 12-24 jam selama minimal 5-7 hari. "
     "Pengobatan hanya efektif jika diberikan pada tahap sangat awal sebelum toksemia berkembang. Jangan buka bangkai atau lakukan nekropsi karena "
     "risiko sporulasi dan kontaminasi lingkungan. Gunakan APD lengkap saat menangani hewan yang dicurigai anthrax.",
     1, "MSD Veterinary Manual - Anthrax in Animals; NIH Books - Anthrax in Humans and Animals"),
    
    ("P01", "manajemen", "Isolasi dan Karantina Segera",
     "Isolasi hewan sakit dan hewan yang pernah kontak dengan minimal jarak 100 meter dari hewan sehat. Terapkan karantina ketat minimal 14-20 hari "
     "setelah vaksinasi hewan yang terpapar. Batasi pergerakan hewan antar kandang/wilayah. Jangan dipindahkan, disembelih, atau dijual. "
     "Laporkan segera ke otoritas veteriner lokal karena anthrax adalah penyakit yang wajib dilaporkan (notifiable disease).",
     2, "NIH - Contingency plan for prevention and control of anthrax; WOAH Standards"),
    
    ("P01", "sanitasi", "Pembuangan Bangkai dan Dekontaminasi",
     "JANGAN buka atau nekropsi bangkai! Bangkai harus dibakar di tempat atau dikubur dalam (>2 meter) dengan kapur hidup (quicklime). "
     "Dekontaminasi area tercemar dengan formaldehyde 5% atau sodium hypochlorite 10%. Insinerasi atau autoclave semua material terkontaminasi. "
     "Area grazing yang tercemar harus ditutup minimal 12 bulan. Spora anthrax dapat bertahan puluhan tahun di tanah.",
     3, "MSD Veterinary Manual; Queensland Australia - Anthrax Clinical Guidelines"),
    
    ("P01", "vaksinasi", "Vaksinasi Pencegahan Rutin",
     "Vaksinasi tahunan dengan anthrax spore vaccine (Sterne strain) untuk semua sapi di area endemik. Vaksinasi dilakukan 2-4 minggu sebelum musim "
     "berisiko tinggi. Untuk outbreak: vaksinasi ring vaccination pada semua hewan dalam radius 5-10 km dari kasus. Jangan vaksinasi hewan sakit "
     "atau hewan yang baru diobati antibiotik (tunggu 2-5 hari). Immunity berkembang dalam 7-10 hari pascavaksinasi.",
     4, "Utah Department of Agriculture; MSD Veterinary Manual"),
    
    # ========== P02: PMK (Penyakit Mulut dan Kuku) ==========
    ("P02", "pengobatan", "Perawatan Simptomatik dan Suportif",
     "TIDAK ADA pengobatan spesifik untuk FMD. Berikan perawatan suportif: antiseptik lokal (larutan kalium permanganat 1:1000 atau asam salisilat 2%) "
     "untuk luka di mulut dan kuku. Berikan pakan lunak/bubur dan air bersih untuk mengurangi nyeri saat makan. NSAID (flunixin meglumine 1-2 mg/kg) "
     "untuk mengurangi demam dan nyeri. Antibiotik sekunder HANYA jika ada infeksi bakterial sekunder pada luka. Pemulihan biasanya 7-14 hari.",
     1, "FAO Small-Scale Dairy Farming Manual; MSD Veterinary Manual - FMD"),
    
    ("P02", "manajemen", "Isolasi Ketat dan Stamping Out",
     "Isolasi total hewan sakit minimum 21 hari (periode infektif). Batasi pergerakan semua hewan berkuku belah dalam radius 10 km. "
     "Di negara bebas FMD: stamping out (depopulasi) semua hewan terinfeksi dan kontak adalah protokol standar. Karantina daerah outbreak minimum 30 hari "
     "setelah kasus terakhir. Kontrol ketat lalu lintas kendaraan, orang, dan peralatan. Desinfeksi wajib sebelum keluar zona terinfeksi.",
     2, "WOAH Terrestrial Code Chapter 8.8; USDA APHIS - FMD"),
    
    ("P02", "sanitasi", "Desinfeksi dan Dekontaminasi",
     "Desinfeksi kandang, peralatan, dan kendaraan dengan: sodium hydroxide 2% (caustic soda), sodium carbonate 4%, citric acid 0.2%, atau "
     "virkon (1:100). Bersihkan dulu kotoran organik sebelum desinfeksi. Bangkai harus dibakar atau dikubur dalam dengan kapur. "
     "Virus FMD dapat bertahan di lingkungan: 14 hari di slurry, 39 hari di feses, 28 hari di air. pH <6 atau >9 mematikan virus.",
     3, "WOAH Standards; NIH - FMD Experimental Evaluation"),
    
    ("P02", "vaksinasi", "Vaksinasi Emergency dan Preventif",
     "Vaksinasi emergency dalam outbreak: ring vaccination radius 5-10 km dari kasus dalam 24-48 jam pertama. Vaksin FMD harus match dengan serotype virus "
     "(A, O, C, Asia-1, SAT 1-3). Immunity berkembang 4-7 hari pascavaksinasi. Untuk endemic areas: vaksinasi rutin setiap 6 bulan. "
     "Vaksinasi emergency dapat dikombinasi dengan stamping out untuk kontrol outbreak yang lebih cepat.",
     4, "Frontiers in Veterinary Science - FMD Vaccination Australia; NIH - FMD Vaccines Review"),
    
    # ========== P03: BRUCELLOSIS ==========
    ("P03", "pengobatan", "Tidak Ada Pengobatan Efektif - Culling Rekomendasi",
     "TIDAK ADA pengobatan antibiotik yang efektif untuk brucellosis pada sapi. Antibiotik (streptomycin, oxytetracycline) dapat mengurangi bakteremia "
     "sementara tetapi TIDAK mengeliminasi infeksi kronis. Sapi yang terinfeksi akan menjadi carrier seumur hidup dan sumber penularan. "
     "Rekomendasi terbaik adalah culling (afkir) semua hewan yang test positif untuk mencegah penyebaran lebih lanjut.",
     1, "MSD Veterinary Manual - Brucellosis; WOAH Guidelines"),
    
    ("P03", "manajemen", "Test-and-Slaughter Program",
     "Implementasi program test-and-slaughter: tes serologi (Rose Bengal Test, ELISA, atau CFT) pada semua hewan secara berkala (3-6 bulan). "
     "Afkir segera semua reactor positif. Pisahkan anak dari induk segera setelah lahir dan berikan kolostrum dari sapi negatif atau kolostrum termosin. "
     "Karantina hewan baru minimum 30-60 hari dengan 2x tes negatif sebelum masuk ke herd. Beli hewan hanya dari herd tersertifikasi bebas brucellosis.",
     2, "CDC Brucellosis Programs; MSD Veterinary Manual"),
    
    ("P03", "sanitasi", "Sanitasi Kandang dan Biosecurity Ketat",
     "Dekontaminasi kandang setelah aborsi atau kelahiran dengan desinfektan: fenol 5%, formalin 2%, sodium hypochlorite 2%, atau lyso 1:400. "
     "Kuburkan atau bakar fetus abortus, plasenta, dan cairan kelahiran dengan kapur. Cuci tangan dengan sabun antiseptik setelah menangani hewan. "
     "Gunakan APD (sarung tangan, boots) saat menangani kelahiran atau aborsi. Bakteri dapat bertahan 135 hari di tanah lembab, 75 hari di feses.",
     3, "WOAH Terrestrial Manual Chapter 3.1.4; FAO Guidelines"),
    
    ("P03", "vaksinasi", "Vaksinasi Sapi Muda (Heifer)",
     "Vaksinasi dengan Brucella abortus Strain 19 atau RB51 pada heifer umur 3-8 bulan (sebelum dewasa kelamin). Vaksinasi memberikan immunity 65-75% "
     "terhadap aborsi dan infeksi. JANGAN vaksinasi sapi bunting (dapat menyebabkan aborsi) atau sapi jantan (dapat menyebabkan orchitis). "
     "Di area endemik tinggi, vaksinasi adalah strategi jangka panjang dikombinasi dengan test-and-slaughter. Sapi vaksin akan test positif secara serologi.",
     4, "USDA APHIS Brucellosis; MSD Veterinary Manual"),
    
    # CONTINUE... (akan saya lanjutkan di bagian berikutnya)

    # ========== P04: MASTITIS ==========
    ("P04", "pengobatan", "Antibiotik Intramammary dan Sistemik",
     "Untuk mastitis klinis akut: antibiotik intramammary (ceftiofur, cephapirin, atau ampicillin) setiap 12-24 jam selama 3-5 hari. "
     "Untuk kasus berat (sistemik): kombinasi intramammary + sistemik (ceftiofur 1-2 mg/kg IM/SC atau enrofloxacin 2.5-5 mg/kg). "
     "Selective dry cow therapy: antibiotik intramammary saat kering kandang untuk semua kuarter terinfeksi. Kultur susu sebelum terapi untuk "
     "identifikasi bakteri dan sensitifitas antibiotik. 25-35% kasus mastitis kultur negatif (self-limiting) - tidak perlu antibiotik.",
     1, "University of Wisconsin Dairy Extension; University of Minnesota AMRLS; MSD Veterinary Manual"),
    
    ("P04", "manajemen", "Protokol Pemerahan Higienis",
     "Terapkan National Mastitis Council 10-Point Plan: (1) Tetapkan goal SCC <200,000/ml; (2) Maintain milking equipment; "
     "(3) Pre-dip & post-dip teat dengan iodine 0.5% atau chlorhexidine; (4) Dry cow therapy; (5) Prompt treatment of clinical cases; "
     "(6) Cull chronic cases; (7) Maintain biosecurity; (8) Monitor udder health; (9) Review periodically; (10) Maintain good records. "
     "Urutan pemerahan: sapi muda → sapi sehat → mastitis kronis (terakhir). Gunakan paper towel sekali pakai untuk cleaning.",
     2, "National Mastitis Council; Wisconsin Dairy Extension"),
    
    ("P04", "sanitasi", "Sanitasi Ambing dan Lingkungan",
     "Cuci ambing dengan air hangat + desinfektan sebelum pemerahan. Pre-dip dengan iodine 0.5% atau chlorhexidine 0.5%, tunggu 30 detik, lap kering. "
     "Post-dip segera setelah pemerahan dengan teat dip antiseptik (barrier protection). Maintain clean bedding - ganti minimal 2x seminggu. "
     "Free stall bedding: sand (terbaik), sawdust kering, atau mattress. Hindari sawdust basah (pertumbuhan bakteri). Ventilasi kandang baik untuk "
     "kurangi kelembaban. Target SCC (Somatic Cell Count) <200,000 cells/ml untuk herd health yang baik.",
     3, "MSD Veterinary Manual; Boehringer Ingelheim Animal Health"),
    
    ("P04", "pencegahan", "Teat Sealant dan Dry Cow Management",
     "Aplikasi internal teat sealant (bismuth subnitrate) saat dry-off untuk physical barrier terhadap patogen selama periode kering. "
     "Dapat dikombinasi atau alternatif dari dry cow antibiotik untuk selective treatment. Periode kering ideal 45-60 hari. "
     "Transisi nutrisi bertahap antara late dry dan early lactation untuk cegah metabolic stress. Monitoring ketat 2 minggu pre-partus dan "
     "2 minggu post-partus (high-risk period). Check SCC individual cow setiap bulan untuk deteksi dini subclinical mastitis.",
     4, "Frontiers in Veterinary Science - Teat Sealant Study; UGA Cooperative Extension"),
    
    # ========== P05: BLOAT (KEMBUNG RUMEN) ==========
    ("P05", "pengobatan", "Dekompresi Rumen Emergency",
     "Untuk kasus acute bloat: (1) Pasang stomach tube (selang lambung) diameter 2-3 cm via oral untuk keluarkan gas. Posisikan sapi berdiri di tanjakan "
     "(kepala lebih tinggi). Massage rumen dari luar untuk bantu gas keluar. (2) Jika gagal atau terlalu parah: trocar and cannula (16-18 gauge) "
     "di left paralumbar fossa (fossa lapar kiri) - tusuk perkutan untuk dekompresi cepat. (3) Berikan oral: minyak nabati (peanut oil, corn oil) "
     "250-500 ml atau poloxalene 25-50g atau simethicone untuk pecah foam. Hindari mineral oil (risk aspirasi).",
     1, "MSD Veterinary Manual - Bloat; Colorado State University Veterinary Extension"),
    
    ("P05", "manajemen", "Manajemen Pakan dan Grazing",
     "Hindari sudden transition ke legume pasture (alfalfa, clover) - transisi bertahap 7-14 hari. Jangan grazing legume saat basah (pagi/embun). "
     "Berikan hay/roughage sebelum grazing legume (fill rumen dulu dengan serat). Grazing strip grazing atau rotation lebih baik dari free grazing. "
     "Campurkan legume dengan grass (ratio 1:1). Hindari pakan konsentrat tinggi yang fermentasi cepat. Sediakan ad-libitum forage/hay. "
     "Berikan bloat prevention additives: poloxalene (0.5-1g/head/day) atau monensin (ionophore) di feed.",
     2, "University Extension Services; Beef Cattle Research Council"),
    
    ("P05", "pencegahan", "Bloat Prevention Additives",
     "Tambahkan anti-foam agents dalam pakan: (1) Poloxalene (Bloat Guard) 1-2g/head/day mixed dalam grain atau mineral. Efektif untuk pasture bloat. "
     "(2) Monensin (Rumensin) ionophore 100-360mg/head/day - modifikasi fermentasi rumen, reduce gas production. (3) Vegetable oils "
     "(peanut, cottonseed oil) 100-200ml/head/day - coating action reduce foam stability. Mulai preventif 3-5 hari sebelum high-risk period. "
     "Monitor body condition score (BCS) - obesitas meningkatkan risk bloat.",
     3, "Journal of Animal Science; Veterinary Clinics: Food Animal Practice"),
    
    ("P05", "nutrisi", "Penyesuaian Rasio dan Nutrisi",
     "Maintain forage:concentrate ratio minimum 60:40 untuk adequate rumen function. Tambahkan effective fiber (>1.5cm particle size) min 19% dari DMI. "
     "Buffer tambahan: sodium bicarbonate 100-150g/head/day atau magnesium oxide 30-60g/head/day untuk stabilize rumen pH. "
     "Hindari fine-ground grain (increase rate of fermentation). Feed mixing yang homogen - hindari sorting. Feed 2-3x per hari lebih baik dari 1x "
     "(reduce fluctuation rumen fermentation). Monitor fecal score dan cudding activity sebagai indicator rumen health.",
     4, "Dairy Cattle Nutrition Extensions; NRC Nutrient Requirements"),
    
    # ========== P06: JEMBRANA DISEASE ==========
    ("P06", "pengobatan", "Terapi Suportif dan Antibiotik Sekunder",
     "Tidak ada antiviral spesifik untuk Jembrana Disease Virus. Berikan terapi suportif: (1) Cairan elektrolit IV/SC untuk rehidrasi "
     "(Ringer's Lactate atau NaCl 0.9%) 20-40 ml/kg; (2) Vitamin B complex dan multivitamin injeksi untuk support metabolisme; "
     "(3) Antibiotik broad-spectrum (oxytetracycline 10-20mg/kg atau florfenicol 20mg/kg) untuk cegah infeksi bakterial sekunder; "
     "(4) NSAID untuk demam (flunixin meglumine 1-2mg/kg). Prognosis buruk jika sudah severe - mortalitas 20-30%. Terapi paling efektif pada early stage.",
     1, "ResearchGate - Immunodiagnosis in Jembrana Disease; Cambridge - Transmission of Jembrana Disease"),
    
    ("P06", "manajemen", "Isolasi dan Kontrol Vektor",
     "Isolasi segera sapi sakit minimum 500 meter dari herd sehat. Virus ditransmit melalui darah - hindari sharing needles/equipment antar sapi. "
     "Vektor mekanis: lalat Tabanid dan Stomoxys - control dengan insektisida spray (permethrin, cypermethrin) dan fly traps. "
     "Cuci dan sterilisasi semua equipment yang kontak dengan darah (alat suntik, scalpel, ear tag applicator). Karantina hewan baru 30 hari dengan tes darah. "
     "Disease endemik di Bali - avoid transporting Bali cattle ke area naive. Report ke otoritas - disease adalah reportable di Indonesia.",
     2, "CABI Datasheet - Jembrana Disease; WOAH Listed Disease"),
    
    ("P06", "vaksinasi", "Vaksinasi Preventif (Indonesia)",
     "Vaksin Jembrana disease tersedia di Indonesia (inactivated vaccine). Vaksinasi sapi umur >3 bulan di area endemik (Bali, Nusa Tenggara). "
     "Schedule: vaksinasi awal 2 dosis dengan interval 3-4 minggu, booster setiap 6-12 bulan. Immunity berkembang 2-3 minggu pascavaksinasi kedua. "
     "Proteksi: reduce clinical severity dan mortalitas, tidak 100% prevent infection. Kombinasi vaksinasi + vector control + biosecurity untuk "
     "kontrol optimal. Vaksinasi wajib untuk sapi yang akan dipindahkan dari area endemik.",
     3, "Bali Veterinary Center; Indonesia Disease Control Program"),
    
    ("P06", "sanitasi", "Desinfeksi dan Pencegahan Transmisi Darah",
     "Virus Jembrana sensitif terhadap desinfektan standar: sodium hypochlorite 1%, iodine compounds, phenolic disinfectants. "
     "Sterilisasi alat medis dengan autoclave (121°C, 15 psi, 15 menit) atau disinfeksi kimia (glutaraldehyde 2%). "
     "Disposable needles dan syringes - JANGAN reuse. Jika harus reuse: sterilisasi proper antara penggunaan. "
     "Hindari tindakan yang involve darah (castration, dehorning, ear tagging) selama outbreak. Burn atau bury dalam bangkai dengan kapur. "
     "Virus dapat survive dalam darah pada needle sampai 24 jam.",
     4, "Veterinary Protocols Indonesia; CABI Compendium"),
    
    # CONTINUE... (P07-P11 akan dilanjutkan)

    # ========== P07: SEPTIKEMIA HEMORAGIK (BALIZIEKTE/HS) ==========
    ("P07", "pengobatan", "Antibiotik Spektrum Luas Dosis Tinggi",
     "Pengobatan HARUS diberikan sangat dini (dalam 6-12 jam onset gejala) untuk efektif. Antibiotik pilihan: (1) Oxytetracycline long-acting "
     "20mg/kg IM/IV setiap 48-72 jam, atau (2) Penicillin G procaine 20,000-40,000 IU/kg IM setiap 12 jam, atau (3) Streptomycin 10-25mg/kg IM "
     "setiap 12 jam selama 3-5 hari. Kombinasi penicillin + streptomycin sering digunakan. Terapi suportif: cairan IV, NSAID untuk shock. "
     "Prognosis buruk jika sudah terjadi septicemia dan edema luas - mortalitas >90% pada kasus akut.",
     1, "WOAH - Haemorrhagic Septicaemia; MSD Veterinary Manual; Cambridge Review"),
    
    ("P07", "manajemen", "Karantina dan Movement Control",
     "Isolasi hewan sakit segera. Outbreak control: stamping out atau mass medication semua hewan dalam affected premises. "
     "Karantina area outbreak radius 5-10km, ban movement semua ruminants selama 14-21 hari pascakasus terakhir. "
     "HS highly fatal dan contagious - transmisi via respiratory secretions dan direct contact. High risk period: musim hujan, high humidity, "
     "high temperature (monsoon season). Monitor suhu herd 2x sehari selama outbreak untuk deteksi dini. "
     "Report wajib ke otoritas - HS adalah notifiable disease di banyak negara Asia dan Afrika.",
     2, "WOAH Terrestrial Manual; UK Government - Haemorrhagic Septicaemia Guidelines"),
    
    ("P07", "vaksinasi", "Vaksinasi Rutin Tahunan",
     "Vaksinasi adalah control strategy paling efektif. Jenis vaksin: (1) Oil-adjuvanted bacterin (killed vaccine) - paling common, immunity 6-12 bulan; "
     "(2) Alum-precipitated vaccine - immunity shorter 3-6 bulan. Vaksinasi SEMUA cattle dan buffalo >3 bulan di area endemik. "
     "Schedule: vaksinasi 2-4 minggu SEBELUM musim hujan/monsoon (high-risk period). Booster tahunan. Immunity mulai 7-14 hari pascavaksinasi. "
     "Emergency vaccination dalam outbreak: ring vaccination 5km radius kasus dalam 24-48 jam. Vaksin harus match dengan serotype lokal (B:2 untuk Asia, E:2 untuk Afrika).",
     3, "Scribd - Hemorrhagic Septicemia Lecture; WOAH Standards"),
    
    ("P07", "sanitasi", "Desinfeksi dan Pencegahan Lingkungan",
     "Pasteurella multocida sensitif terhadap desinfektan common: sodium hypochlorite 1-2%, phenol 2%, quaternary ammonium compounds. "
     "Desinfeksi kandang, feeding troughs, water troughs daily selama outbreak. Improve drainage - hindari genangan air (breeding ground bakteri). "
     "Reduce stocking density - overcrowding increases transmission. Pisahkan species (cattle dari buffalo) jika mungkin. "
     "Bakteri dapat survive 1-2 minggu di feces dan soil dalam kondisi lembab. Burn atau deep bury carcasses dengan kapur. "
     "Kontrol lalat dan serangga vektor dengan sanitasi dan insektisida.",
     4, "WOAH Terrestrial Manual; FAO Animal Health Guidelines"),
    
    # ========== P08: CACINGAN (TOXOCARA VITULORUM) ==========
    ("P08", "pengobatan", "Anthelmintik Broad-Spectrum",
     "Obat cacing pilihan untuk Toxocara vitulorum: (1) Fenbendazole 10mg/kg PO single dose atau 5mg/kg PO selama 3 hari berturut-turut; "
     "(2) Albendazole 10mg/kg PO single dose (JANGAN untuk sapi bunting trimester pertama); (3) Ivermectin 0.2mg/kg SC/PO; "
     "(4) Levamisole 7.5mg/kg SC/PO; (5) Pyrantel pamoate 10mg/kg PO. Ulangi treatment setelah 2-3 minggu untuk kill larva yang baru mature. "
     "Terapi suportif untuk anak sapi severe: cairan SC/IV untuk dehidrasi, vitamin B complex, probiotik untuk restore gut flora. "
     "Monitor feses 7-14 hari post-treatment untuk assess efficacy (fecal egg count).",
     1, "University of Saskatchewan - Toxocara vitulorum; NIH PMC Case Study; MSD Veterinary Manual"),
    
    ("P08", "pencegahan", "Deworm Induk Pra-Partus",
     "Strategi pencegahan utama: deworm sapi induk bunting 2-4 minggu SEBELUM expected calving date. Ini mengurangi transmisi transmammary larvae ke calf. "
     "Anthelmintic untuk sapi bunting: fenbendazole (safe), ivermectin (safe trimester 2-3), levamisole (avoid trimester 1). "
     "Deworm calves pada umur 2-3 minggu (sebelum patent period - prepatent deworming), ulangi umur 6-8 minggu dan 12-16 minggu. "
     "High-risk calves: dari induk dengan riwayat infeksi berat atau area endemik tinggi. Rotational deworming schedule berbasis fecal egg count monitoring.",
     2, "The Beef Site - Toxocara Vitulorum Report; Wormboss Australia"),
    
    ("P08", "manajemen", "Sanitasi Kandang dan Rotasi Padang",
     "Hygiene management: (1) Clean bedding daily untuk remove fecal contamination; (2) Separate young calves dari adult cattle; "
     "(3) Colostrum management: pasteurisasi kolostrum (60°C selama 60 menit) untuk kill larvae; (4) Rotational grazing: pindahkan calves ke clean pasture "
     "setiap 2-4 minggu (larva tidak survive >2 minggu di pasture kering). Hindari overcrowding - increase parasite load. "
     "Fecal egg count monitoring: sample pooled feces setiap 3-6 bulan untuk assess parasite burden dan efficacy deworming program.",
     3, "ResearchGate - Toxocara vitulorum in cattle; Parasitology Extensions"),
    
    ("P08", "nutrisi", "Nutrisi Optimal untuk Resistance",
     "Nutritional support untuk meningkatkan resistance: (1) Protein adequat (CP 14-16% untuk growing calves) - mendukung immune function; "
     "(2) Trace minerals: zinc (40-60ppm), copper (10-15ppm), selenium (0.3ppm) - esensial untuk immunity dan tissue repair; "
     "(3) Vitamin A (2000-4000 IU/kg diet) untuk intestinal mucosa health; (4) Energy adequat (avoid underfeeding) - malnutrisi meningkatkan susceptibility. "
     "Free-choice mineral supplement dengan trace minerals. Monitor body condition score - target BCS 5-6 (skala 1-9) untuk optimal resistance terhadap parasit.",
     4, "NRC Nutrient Requirements; Journal of Veterinary Parasitology"),
    
    # ========== P09: CORPUS LUTEUM PERSISTEN ==========
    ("P09", "pengobatan", "Injeksi Prostaglandin F2α (PGF2α)",
     "Treatment pilihan: Prostaglandin F2α (PGF2α) injeksi untuk luteolysis (hancurkan CL persisten). Dosis: dinoprost tromethamine 25mg IM atau "
     "cloprostenol 500µg IM. CL akan regress dalam 2-5 hari, diikuti estrus dalam 2-5 hari pascainjeksi. Jika tidak estrus setelah 7-10 hari: "
     "ulangi PGF2α (kemungkinan ada CL baru atau cyst). Jangan berikan PGF2α pada sapi bunting (menyebabkan aborsi). "
     "Kombinasi terapi: GnRH (day 0) + PGF2α (day 7) + GnRH (day 9) untuk Ovsynch protocol jika perlu breeding scheduled.",
     1, "MSD Veterinary Manual - Luteal Cystic Ovary; NIH - Effects of GnRH or PGF2α"),
    
    ("P09", "manajemen", "Pemeriksaan Ultrasonografi dan Monitoring",
     "Diagnosis akurat dengan transrectal ultrasonography (TRUS): visualisasi CL persisten (corpus luteum >20mm yang bertahan >18 hari tanpa estrus). "
     "Differensiasi dari pregnancy (presence of embryo/fetus) dan cystic structures. Monitoring herd: check all cows tidak kawin setelah 60 hari postpartum. "
     "Body condition score monitoring: BCS <2.5 atau >3.5 meningkatkan risk persistent CL. Target BCS 3.0-3.25 at calving, 2.5-3.0 early lactation. "
     "Breeding records accurate: heat detection aids (tail paint, pedometers, activity monitors) untuk identify anestrus cows.",
     2, "Partners in Reproduction - Corpus Luteum Persistent; NADIS UK"),
    
    ("P09", "pencegahan", "Pencegahan Endometritis dan Infeksi Uterus",
     "Persistent CL sering berkaitan dengan endometritis (uterine infection). Pencegahan: (1) Clean calving environment; "
     "(2) Proper obstetric hygiene - desinfeksi alat dan tangan; (3) Avoid unnecessary uterine manipulation; (4) Early treatment metritis/endometritis "
     "(PGF2α atau intrauterine antibiotics); (5) Adequate nutrition peripartum untuk cegah immune suppression; (6) Vitamin E (1000 IU/day) dan "
     "selenium (0.3ppm diet) untuk uterine health. Postpartum check 30-40 hari untuk detect endometritis dan reproductive abnormalities dini.",
     3, "MSD Animal Health Ireland - Uterine Infection; Reproduction Extensions"),
    
    ("P09", "nutrisi", "Manajemen Nutrisi dan Body Condition",
     "Nutritional management untuk optimal reproduction: (1) Energy balance positive atau minimal 0 pada breeding period; "
     "(2) Avoid excessive body condition loss postpartum (target <1 BCS loss); (3) Transition cow management: DCAD diet 21 hari prepartum "
     "(prevent milk fever), adequate calcium dan phosphorus; (4) Protein 16-18% CP early lactation; (5) Beta-carotene supplementation "
     "(300-600mg/day) untuk corpus luteum function dan fertility. Monitor milk production, body condition, dan metabolic indicators (BHB, NEFA) "
     "untuk assess energy balance. Consult nutritionist untuk optimize reproduction-focused feeding program.",
     4, "Dairy Cattle Fertility Management; NRC Nutrient Requirements of Dairy Cattle"),
    
    # CONTINUE... (P10-P11)

    # ========== P10: SURRA (TRYPANOSOMIASIS) ==========
    ("P10", "pengobatan", "Obat Tripanosida Spesifik",
     "Trypanocidal drugs pilihan: (1) Diminazene aceturate (Berenil) 3.5-7mg/kg IM deep injection single dose - drug of choice untuk Trypanosoma evansi. "
     "Efektif untuk infection akut dan kronis. Side effects minimal jika dosis tepat; (2) Isometamidium chloride (Trypamidium) 0.5-1mg/kg IM - "
     "efek terapeutik DAN profilaktik (proteksi 2-4 bulan). Gunakan untuk treatment dan prevention di endemic areas; "
     "(3) Suramin 10mg/kg IV (slow) - jarang digunakan karena toxicity lebih tinggi. Treatment harus diulang jika relapse (recurrence parasitemia). "
     "Monitor blood smear 7, 14, 21 hari post-treatment untuk assess cure. Terapi suportif: iron supplementation untuk anemia, vitamin B complex.",
     1, "CABI - Trypanosoma evansi; WOAH Chapter 8.23; FAO Field Guide"),
    
    ("P10", "manajemen", "Kontrol Vektor Lalat Penghisap Darah",
     "Vector control strategies: (1) Insekticide treatment: pour-on pyrethroid (deltamethrin, cypermethrin) setiap 2-4 minggu atau ear tags insecticide; "
     "(2) Fly traps: sticky traps, odor-baited traps untuk Tabanid flies dan Stomoxys; (3) Residual spraying: kandang walls dan resting areas dengan "
     "residual insecticide; (4) Environmental management: drain standing water (breeding site Tabanus), remove manure regularly, vegetation control "
     "around farm. Timing: vector control intensif during high fly season (panas/lembab). Integrated pest management lebih efektif dari single approach.",
     2, "UK Government - Surra Disease; ResearchGate - Trypanosomosis in Livestock"),
    
    ("P10", "pencegahan", "Chemoprophylaxis dan Screening",
     "Preventive chemotherapy di endemic areas: Isometamidium chloride 0.5mg/kg IM memberikan proteksi 2-6 bulan (tergantung challenge). "
     "Strategic prophylaxis: inject sebelum high-risk period (musim fly peak, transhumance, mixing herds). Quarantine dan test hewan baru: "
     "blood smear examination (Giemsa stain), serologi (CATT, ELISA) sebelum masuk herd. Isolasi 30-60 hari dengan monitoring clinical signs. "
     "Avoid sharing needles/instruments (mechanical transmission). Sterilisasi equipment bedah proper. Di Latin America: vampire bat control juga penting.",
     3, "WOAH Standards; CABI Compendium; FAO Guidelines"),
    
    ("P10", "nutrisi", "Nutritional Support untuk Recovery",
     "Nutritional support untuk sapi terinfeksi: (1) High-quality protein 14-16% CP untuk restore muscle mass yang loss dari cachexia; "
     "(2) Iron supplementation: iron dextran injection 10-20mg/kg IM atau oral ferrous sulfate untuk combat anemia (Hb <8g/dl); "
     "(3) Vitamin B12 (cyanocobalamin) 1000-5000µg IM weekly untuk support erythropoiesis; (4) Folic acid 5-10mg/day untuk blood cell production; "
     "(5) Energy adequat: high-quality forage + grain supplement untuk weight recovery. Monitor PCV (packed cell volume) weekly - target >25% untuk recovery. "
     "Avoid stress selama recovery period. Good nutrition meningkatkan treatment response dan reduce relapse rate.",
     4, "Journal of Tropical Animal Health; Veterinary Parasitology Reviews"),
    
    # ========== P11: BOVINE EPHEMERAL FEVER (DEMAM 3 HARI) ==========
    ("P11", "pengobatan", "NSAID dan Terapi Suportif",
     "Tidak ada antiviral spesifik - treatment adalah symptomatic dan supportive. (1) NSAID untuk demam dan nyeri: Flunixin meglumine 1-2.2mg/kg IV/IM "
     "setiap 12-24 jam atau Ketoprofen 3mg/kg IV/IM atau Meloxicam 0.5mg/kg SC - reduce fever, inflammation, muscle stiffness; "
     "(2) Cairan therapy: Ringer's Lactate atau NaCl 0.9% 20-40ml/kg IV untuk dehydration dan support circulation; "
     "(3) Calcium borogluconate IV jika ada hypocalcemia signs (muscle tremors, recumbency); (4) Vitamin B complex injection untuk support metabolism. "
     "Nursing care: soft bedding untuk recumbent cows, flip/reposition setiap 3-4 jam (prevent pressure sores), sling support jika perlu. "
     "Recovery spontan 3-7 hari pada majority cases. Mortalitas <1% kecuali komplikasi (pneumonia, mastitis sekunder).",
     1, "MSD Veterinary Manual - BEF; Springer - Epidemiology BEF; Australia NSW Department"),
    
    ("P11", "manajemen", "Supportive Care untuk Sapi Rebah",
     "Management recumbent cows (down cows): (1) Thick bedding (straw, sand, mattress) untuk prevent pressure necrosis; "
     "(2) Reposition cow setiap 3-4 jam untuk prevent muscle dan nerve damage; (3) Hip lifters atau slings untuk assist standing; "
     "(4) Massage muscles untuk prevent atrophy dan improve circulation; (5) Encourage standing attempts 4-6x per hari dengan assistance; "
     "(6) Hand-fed high-quality feed dan water jika tidak mau eat/drink; (7) Milk out secara manual atau machine untuk prevent mastitis. "
     "Monitor for complications: pneumonia (dari recumbency), pressure sores, nerve paralysis, mastitis. "
     "Hindari force standing terlalu awal - bisa cause secondary injuries. Patience - majority recover dalam 5-7 hari dengan good nursing care.",
     2, "CSIRO Microbiology Australia; NIH - BEF in Asia; ResearchGate - BEF Australia"),
    
    ("P11", "vaksinasi", "Vaksinasi Preventif Tahunan",
     "Inactivated BEF vaccine available di endemic countries (Australia, Asia). Vaksinasi sapi >6 bulan umur. Schedule: (1) Primary course: 2 doses "
     "dengan interval 4-6 minggu; (2) Booster: annual booster 2-4 minggu SEBELUM expected BEF season (vector activity peak - panas/musim hujan). "
     "Immunity berkembang 2-3 minggu pascavaksinasi kedua. Duration of immunity: 12 bulan. Vaksinasi tidak prevent infection 100% tetapi significantly "
     "reduce clinical severity, duration of disease, dan milk production loss. High-value animals (dairy high producers, bulls) prioritas vaksinasi. "
     "Vaksinasi tidak efektif jika diberikan SAAT outbreak sudah terjadi (perlu waktu immunity development).",
     3, "Queensland Australia - BEF; Journal Vaccine - BEF Vaccines; Veterinary Record"),
    
    ("P11", "sanitasi", "Kontrol Vektor Nyamuk dan Culicoides",
     "Vector control untuk prevent BEF transmission: (1) Insecticide application: pour-on pyrethroid atau spray premises dengan residual insecticide "
     "(permethrin, deltamethrin) terutama evening/night (vector activity peak); (2) Repellents: insect repellent pada cattle selama high-risk periods; "
     "(3) Environmental management: eliminate standing water (breeding sites nyamuk), drain ditches, remove vegetation near housing; "
     "(4) Housing management: screen housing jika feasible, fans untuk air circulation (reduce vector contact); (5) Timing: intensify vector control "
     "2-4 minggu before expected disease season. BEF is vector-borne (mosquitoes, Culicoides) - tidak direct cattle-to-cattle transmission. "
     "Control vectors = control disease spread. Integrated approach: vaksinasi + vector control untuk optimal protection.",
     4, "Elsevier - Textbook Diseases of Cattle; Veterinary Entomology Reviews"),
]


class Command(BaseCommand):
    help = "Isi data Solusi Penanganan komprehensif untuk semua penyakit dari sumber terpercaya."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("=" * 80))
        self.stdout.write(self.style.SUCCESS("MENGISI DATA SOLUSI PENANGANAN KOMPREHENSIF"))
        self.stdout.write(self.style.SUCCESS("=" * 80))
        
        # Mapping kode penyakit ke objek
        penyakit_map = {}
        for penyakit in Penyakit.objects.all():
            penyakit_map[penyakit.kode] = penyakit
        
        created_count = 0
        updated_count = 0
        
        for kode_penyakit, jenis, judul, deskripsi, prioritas, referensi in SOLUSI_DATA:
            if kode_penyakit not in penyakit_map:
                self.stdout.write(self.style.WARNING(f"  ⚠️  Penyakit {kode_penyakit} tidak ditemukan, skip."))
                continue
            
            penyakit_obj = penyakit_map[kode_penyakit]
            
            # Cek apakah solusi sudah ada (berdasarkan penyakit + jenis + judul)
            obj, created = SolusiPenanganan.objects.get_or_create(
                penyakit=penyakit_obj,
                jenis=jenis,
                judul=judul,
                defaults={
                    'deskripsi': deskripsi,
                    'prioritas': prioritas,
                    'referensi': referensi,
                    'aktif': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  ✅ {penyakit_obj.kode} - {jenis}: {judul[:50]}..."))
            else:
                # Update jika sudah ada
                obj.deskripsi = deskripsi
                obj.prioritas = prioritas
                obj.referensi = referensi
                obj.save()
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"  🔄 {penyakit_obj.kode} - {jenis}: {judul[:50]}... (updated)"))
        
        # Statistik
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("📊 STATISTIK:"))
        self.stdout.write(f"  • Solusi baru dibuat: {created_count}")
        self.stdout.write(f"  • Solusi diupdate: {updated_count}")
        self.stdout.write(f"  • Total solusi di database: {SolusiPenanganan.objects.count()}")
        self.stdout.write("=" * 80)
        
        # Summary per penyakit
        self.stdout.write("\n📋 RINGKASAN PER PENYAKIT:")
        for penyakit in Penyakit.objects.all().order_by('kode'):
            jumlah = penyakit.solusi_penanganan.filter(aktif=True).count()
            self.stdout.write(f"  {penyakit.kode} - {penyakit.nama}: {jumlah} solusi aktif")
        
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("🎉 SELESAI! Data solusi penanganan berhasil diisi."))
        self.stdout.write("\n📚 SUMBER REFERENSI:")
        self.stdout.write("  • MSD Veterinary Manual")
        self.stdout.write("  • WHO/WOAH - World Organisation for Animal Health")
        self.stdout.write("  • NIH/PubMed - National Institutes of Health")
        self.stdout.write("  • University Extensions (Wisconsin, Minnesota, etc)")
        self.stdout.write("  • FAO - Food and Agriculture Organization")
        self.stdout.write("  • Government Veterinary Services (UK, Australia, USA)")
        self.stdout.write("  • Peer-reviewed Veterinary Journals")
        self.stdout.write("\n")
