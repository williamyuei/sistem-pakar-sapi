"""
cf_engine.py — Algoritma Certainty Factor (CF)
================================================
Referensi: Shortliffe & Buchanan (1975)

Rumus:
  1. CF per gejala  : CF_gejala = CF_pakar × CF_user
                      (CF_user diberikan oleh user dari pilihan keyakinan)

  2. Kombinasi CF   : CF_combine(CF1, CF2) = CF1 + CF2 − (CF1 × CF2)
                      Diterapkan iteratif untuk setiap gejala per penyakit.
"""

from core.models import Rule


def hitung_cf(gejala_cf: dict[int, float]) -> list[dict]:
    """
    Menghitung nilai CF untuk setiap penyakit berdasarkan gejala yang dipilih.

    Args:
        gejala_cf: Dict mapping ID gejala → nilai CF_user (0.0 – 1.0).

    Returns:
        List dict hasil CF, diurutkan dari nilai tertinggi. Contoh:
        [{"penyakit": "Anthrax", "kode": "P01", "cf": 0.99, "persentase": 99.0, ...}]
    """
    if not gejala_cf:
        return []

    # Ambil semua rule yang relevan sekaligus (1 query)
    rules = Rule.objects.filter(
        gejala_id__in=gejala_cf.keys()
    ).select_related('penyakit', 'gejala')

    # Akumulasi CF per penyakit
    cf_map: dict[int, dict] = {}

    for rule in rules:
        pid = rule.penyakit.id
        cf_user = gejala_cf.get(rule.gejala_id, 0)
        cf_baru = rule.cf_pakar * cf_user

        if pid not in cf_map:
            cf_map[pid] = {
                "penyakit": rule.penyakit.nama,
                "kode": rule.penyakit.kode,
                "deskripsi": rule.penyakit.deskripsi,
                "solusi": rule.penyakit.solusi,
                "cf": cf_baru,
            }
        else:
            # Rumus kombinasi CF: CF1 + CF2 − (CF1 × CF2)
            cf_lama = cf_map[pid]["cf"]
            cf_map[pid]["cf"] = cf_lama + cf_baru - (cf_lama * cf_baru)

    # Susun hasil akhir
    hasil = [
        {
            **data,
            "cf": round(data["cf"], 4),
            "persentase": round(data["cf"] * 100, 2),
        }
        for data in cf_map.values()
    ]

    return sorted(hasil, key=lambda x: x["cf"], reverse=True)
