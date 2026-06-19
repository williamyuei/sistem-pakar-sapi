"""
Management command untuk menambah 6 penyakit baru dengan basis pengetahuan yang akurat.
Data disusun berdasarkan literatur veteriner terpercaya.

Sumber:
- WHO/WOAH (World Organisation for Animal Health)
- NIH (National Institutes of Health)
- Merck Veterinary Manual
- Peer-reviewed journals (ResearchGate, PubMed)
- Government veterinary agencies (UK, Australia, FAO)

Jalankan: python manage.py add_new_diseases
"""
from django.core.management.base import BaseCommand
from core.models import Penyakit, Gejala, Rule

# === DATA PENYAKIT BARU ===
PENYAKIT_BARU = [
    ("P06", "Jembrana Disease",
     "Penyakit virus (lentivirus) akut yang menyerang sapi Bali dan kerbau, ditandai dengan demam tinggi, "
     "pembesaran kelenjar getah bening, dan dapat menyebabkan kematian dalam 1-2 minggu. "
     "Berbeda dengan lentivirus lain yang kronis, penyakit Jembrana bersifat akut dengan tingkat kematian 20-30%. "
     "(Sumber: ResearchGate, Cambridge University Press)",
     "Isolasi hewan segera. Tidak ada pengobatan spesifik. Berikan antibiotik untuk infeksi sekunder, "
     "cairan elektrolit untuk dehidrasi, dan perawatan suportif. Vaksinasi pencegahan tersedia. "
     "Laporkan ke dinas peternakan."),
    
    ("P07", "Septikemia Hemoragik (Baliziekte/HS)",
     "Penyakit bakteri akut (Pasteurella multocida B:2 dan E:2) yang sangat fatal pada sapi dan kerbau. "
     "Ditandai dengan septikemia akut, pendarahan, dan pembengkakan di daerah leher/dada. "
     "Morbiditas dan mortalitas sangat tinggi terutama saat musim hujan dengan kelembaban tinggi. "
     "(Sumber: WOAH, Merck Veterinary Manual)",
     "Berikan antibiotik spektrum luas (penisilin, oksitetrasiklin, atau streptomisin) segera. "
     "Vaksinasi rutin sangat penting. Isolasi hewan sakit. Perbaiki sanitasi dan drainase kandang. "
     "Laporkan outbreak ke otoritas."),
    
    ("P08", "Cacingan (Toxocara vitulorum)",
     "Infeksi cacing gelang besar (roundworm) yang menyerang anak sapi usia 1-6 bulan. "
     "Cacing berwarna putih krem hingga 30 cm panjangnya. Penularan melalui susu induk yang terinfeksi. "
     "Dapat menyebabkan diare, penurunan pertumbuhan, obstruksi usus, bahkan kematian pada kasus berat. "
     "(Sumber: University of Saskatchewan, NIH, Merck Veterinary Manual)",
     "Berikan anthelmintik (obat cacing): fenbendazole, albendazole, atau ivermectin sesuai dosis. "
     "Obati induk sapi sebelum melahirkan untuk mencegah penularan. Sanitasi kandang dan rotasi padang rumput. "
     "Perawatan suportif untuk diare dan dehidrasi."),
    
    ("P09", "Corpus Luteum Persisten",
     "Gangguan reproduksi dimana corpus luteum (CL) tetap aktif di ovarium melebihi waktu normal "
     "sehingga sapi tidak menunjukkan tanda-tanda birahi dan dianggap bunting padahal tidak. "
     "Menyebabkan anovulasi (tidak ada ovulasi) dan meningkatkan jarak beranak (calving interval). "
     "(Sumber: Merck Veterinary Manual, Partners in Reproduction)",
     "Injeksi prostaglandin F2α (PGF2α) untuk melisiskan CL persisten. Dapat diulang jika diperlukan. "
     "Evaluasi dengan ultrasonografi untuk memastikan diagnosis. Periksa kondisi uterus untuk mendeteksi "
     "endometritis yang sering menyertai. Perbaiki manajemen reproduksi dan nutrisi."),
    
    ("P10", "Surra (Trypanosomiasis)",
     "Penyakit parasit darah (Trypanosoma evansi) yang ditularkan oleh lalat penghisap darah (Tabanids, Stomoxes). "
     "Menyebabkan demam berulang, anemia progresif, penurunan berat badan, dan penurunan produksi. "
     "Dapat berakibat fatal terutama pada kuda dan unta, sedang pada sapi bersifat kronis. "
     "(Sumber: CABI, WOAH, FAO, UK Government)",
     "Berikan obat tripanosida: diminazene aceturate atau isometamidium chloride. "
     "Kontrol vektor dengan insektisida dan perangkap lalat. Pisahkan hewan sakit. "
     "Monitor dengan pemeriksaan darah mikroskopis. Perbaiki nutrisi untuk meningkatkan daya tahan."),
    
    ("P11", "Bovine Ephemeral Fever (Demam 3 Hari)",
     "Penyakit virus (rhabdovirus) akut yang ditularkan oleh serangga (nyamuk). "
     "Ditandai dengan demam tinggi mendadak, kekakuan otot, pincang, air liur berlebih, dan keengganan bergerak. "
     "Disebut 'demam 3 hari' karena gejala biasanya berlangsung 2-3 hari. Mortalitas rendah (<1%) tapi "
     "menyebabkan penurunan produksi susu drastis dan kerugian ekonomi. "
     "(Sumber: Merck Veterinary Manual, Springer, Australia NSW, NIH)",
     "Tidak ada pengobatan spesifik. Berikan NSAID (anti-inflamasi non-steroid) seperti flunixin meglumine "
     "untuk mengurangi demam dan nyeri. Perawatan suportif: cairan, bantuan berdiri untuk sapi rebah. "
     "Vaksinasi pencegahan tersedia. Kontrol serangga vektor. Pemulihan biasanya spontan dalam 3-7 hari."),
]

# === DATA GEJALA BARU ===
GEJALA_BARU = [
    ("G18", "Pembesaran kelenjar getah bening (limfadenopati)"),
    ("G19", "Diare berdarah atau diare berat"),
    ("G20", "Dehidrasi berat (mata cekung, kulit kering)"),
    ("G21", "Pembengkakan di daerah leher, dada, atau kepala"),
    ("G22", "Keluar cacing dari feses atau muntahan"),
    ("G23", "Perut membesar (pot belly) pada anak sapi"),
    ("G24", "Pertumbuhan terhambat / kurus kering"),
    ("G25", "Tidak menunjukkan tanda birahi (anestrus)"),
    ("G26", "Gagal bunting berulang meski sudah dikawinkan"),
    ("G27", "Anemia (selaput lendir pucat)"),
    ("G28", "Penurunan berat badan progresif"),
    ("G29", "Edema (pembengkakan) di bagian bawah tubuh"),
    ("G30", "Kekakuan otot dan sendi"),
    ("G31", "Kesulitan berdiri atau rebah (recumbency)"),
    ("G32", "Air liur berlebihan (hipersalivasi)"),
    ("G33", "Keluar cairan dari hidung dan mata"),
    ("G34", "Tremor (gemetar) pada otot"),
]

# === RULES (Penyakit -> Gejala -> CF Pakar) ===
# CF Pakar ditentukan berdasarkan literatur klinis:
# 0.9-1.0 = Sangat khas/patognomonik
# 0.7-0.8 = Sering muncul
# 0.5-0.6 = Cukup sering
# 0.3-0.4 = Kadang-kadang

RULES_BARU = [
    # P06 - Jembrana Disease
    # Ref: ResearchGate - acute syndrome with fever, lymphadenopathy, lethargy, diarrhea
    ("P06", "G01", 0.9),  # Demam tinggi - sangat khas
    ("P06", "G18", 0.9),  # Pembesaran kelenjar getah bening - khas
    ("P06", "G16", 0.8),  # Nafsu makan menurun
    ("P06", "G17", 0.8),  # Lemas dan tidak mau bergerak
    ("P06", "G19", 0.7),  # Diare berdarah
    ("P06", "G20", 0.7),  # Dehidrasi berat
    ("P06", "G33", 0.6),  # Keluar cairan dari hidung dan mata
    
    # P07 - Septikemia Hemoragik (HS/Baliziekte)
    # Ref: WOAH, Merck - acute fatal septicemia, hemorrhage, edema
    ("P07", "G01", 0.9),  # Demam tinggi
    ("P07", "G21", 0.9),  # Pembengkakan leher/dada - sangat khas
    ("P07", "G03", 0.8),  # Pendarahan dari lubang tubuh
    ("P07", "G17", 0.8),  # Lemas
    ("P07", "G02", 0.7),  # Kematian mendadak (kasus perakut)
    ("P07", "G33", 0.7),  # Keluar cairan dari hidung/mata
    ("P07", "G16", 0.6),  # Nafsu makan menurun
    
    # P08 - Cacingan (Toxocara vitulorum)
    # Ref: USask, NIH - diarrhea, poor growth, pot belly, worms in feces
    ("P08", "G22", 0.9),  # Keluar cacing dari feses - patognomonik
    ("P08", "G23", 0.8),  # Perut membesar (pot belly)
    ("P08", "G24", 0.8),  # Pertumbuhan terhambat
    ("P08", "G19", 0.7),  # Diare
    ("P08", "G16", 0.6),  # Nafsu makan menurun
    ("P08", "G17", 0.6),  # Lemas
    ("P08", "G20", 0.5),  # Dehidrasi (akibat diare)
    
    # P09 - Corpus Luteum Persisten
    # Ref: Merck, Partners in Reproduction - anovulation, no estrus signs
    ("P09", "G25", 0.95), # Tidak menunjukkan birahi - sangat khas
    ("P09", "G26", 0.9),  # Gagal bunting berulang - khas
    ("P09", "G11", 0.5),  # Penurunan produksi susu (bisa terjadi)
    
    # P10 - Surra (Trypanosomiasis)
    # Ref: CABI, WOAH, FAO - pyrexia, anemia, weight loss, edema
    ("P10", "G01", 0.8),  # Demam tinggi (intermiten)
    ("P10", "G27", 0.9),  # Anemia - sangat khas
    ("P10", "G28", 0.9),  # Penurunan berat badan progresif - khas
    ("P10", "G29", 0.7),  # Edema
    ("P10", "G17", 0.7),  # Lemas
    ("P10", "G11", 0.6),  # Penurunan produksi susu
    ("P10", "G16", 0.6),  # Nafsu makan menurun
    
    # P11 - Bovine Ephemeral Fever (BEF)
    # Ref: Merck, Springer, NSW - high fever, stiffness, lameness, recumbency, nasal/ocular discharge
    ("P11", "G01", 0.95), # Demam tinggi mendadak - sangat khas
    ("P11", "G30", 0.9),  # Kekakuan otot - sangat khas
    ("P11", "G08", 0.9),  # Pincang/kesulitan berjalan - sangat khas
    ("P11", "G31", 0.8),  # Kesulitan berdiri/rebah
    ("P11", "G32", 0.8),  # Air liur berlebihan
    ("P11", "G33", 0.8),  # Keluar cairan dari hidung dan mata
    ("P11", "G16", 0.7),  # Nafsu makan menurun
    ("P11", "G17", 0.7),  # Lemas
    ("P11", "G34", 0.6),  # Tremor otot
    ("P11", "G11", 0.8),  # Penurunan produksi susu drastis
]


class Command(BaseCommand):
    help = "Tambah 6 penyakit baru dengan basis pengetahuan yang akurat dari literatur veteriner."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("MENAMBAHKAN 6 PENYAKIT BARU + GEJALA + RULES"))
        self.stdout.write(self.style.SUCCESS("=" * 70))
        
        # 1. Tambah Penyakit
        self.stdout.write("\n📋 MENAMBAH PENYAKIT BARU:")
        p_map = {}
        for kode, nama, desk, solusi in PENYAKIT_BARU:
            obj, created = Penyakit.objects.get_or_create(
                kode=kode,
                defaults={"nama": nama, "deskripsi": desk, "solusi": solusi}
            )
            p_map[kode] = obj
            if created:
                self.stdout.write(self.style.SUCCESS(f"  ✅ {obj}"))
            else:
                self.stdout.write(self.style.WARNING(f"  ⚠️  {obj} (sudah ada, dilewati)"))
        
        # 2. Tambah Gejala
        self.stdout.write("\n📋 MENAMBAH GEJALA BARU:")
        g_map = {}
        for kode, nama in GEJALA_BARU:
            obj, created = Gejala.objects.get_or_create(
                kode=kode,
                defaults={"nama": nama}
            )
            g_map[kode] = obj
            if created:
                self.stdout.write(self.style.SUCCESS(f"  ✅ {obj}"))
            else:
                self.stdout.write(self.style.WARNING(f"  ⚠️  {obj} (sudah ada, dilewati)"))
        
        # 3. Tambah Rules
        self.stdout.write("\n📋 MENAMBAH RULES (BASIS PENGETAHUAN):")
        rule_count = 0
        for kp, kg, cf in RULES_BARU:
            # Ambil objek gejala (bisa dari yang lama atau yang baru)
            if kg in g_map:
                gejala_obj = g_map[kg]
            else:
                gejala_obj = Gejala.objects.get(kode=kg)
            
            _, created = Rule.objects.get_or_create(
                penyakit=p_map[kp],
                gejala=gejala_obj,
                defaults={"cf_pakar": cf}
            )
            if created:
                rule_count += 1
                self.stdout.write(f"  ✅ {kp} | {kg} | CF={cf}")
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Berhasil menambahkan {rule_count} rules baru!"))
        
        # 4. Statistik Akhir
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("📊 STATISTIK DATABASE:"))
        self.stdout.write(f"  • Total Penyakit: {Penyakit.objects.count()}")
        self.stdout.write(f"  • Total Gejala: {Gejala.objects.count()}")
        self.stdout.write(f"  • Total Rule: {Rule.objects.count()}")
        self.stdout.write("=" * 70)
        
        self.stdout.write(self.style.SUCCESS("\n🎉 SELESAI! Database berhasil diperbarui."))
        self.stdout.write("\n📚 SUMBER REFERENSI:")
        self.stdout.write("  • WHO/WOAH - World Organisation for Animal Health")
        self.stdout.write("  • NIH - National Institutes of Health (PubMed)")
        self.stdout.write("  • Merck Veterinary Manual")
        self.stdout.write("  • University of Saskatchewan")
        self.stdout.write("  • ResearchGate, Cambridge University Press")
        self.stdout.write("  • FAO, UK/Australia Government Veterinary")
        self.stdout.write("\n")
