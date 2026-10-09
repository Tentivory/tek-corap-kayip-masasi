#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tek Corap Kayip Masasi.

Cift corap girer, biri dosya olur. Calisan, gereksiz, Turkce tutanak.
"""

from __future__ import annotations

import argparse
import hashlib
import textwrap
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=3))
SANDIKLAR = ("saat yonu", "saat yonunun tersi", "cekmece alti")


def kayip_olasiligi(program_dk: int, adet: int) -> float:
    if adet < 2:
        return 0.0
    ham = min(0.97, 0.18 + (program_dk / 180) + ((adet - 2) * 0.04))
    return round(ham, 2)


def sandik_sonucu(tohum: str) -> dict[str, int]:
    """Referandum gosterisi. Tambur oylari dagitir, cogu zaman kendi yonunu secer."""
    sayilar = {}
    for sandik in SANDIKLAR:
        ozet = hashlib.sha256(f"{tohum}:{sandik}".encode("utf-8")).hexdigest()
        sayilar[sandik] = int(ozet[:4], 16) % 90 + 3
    # Tambur, sayimdan once kararini fisildemis olur. Gizli not buna bakar.
    tambur = SANDIKLAR[int(hashlib.md5(tohum.encode("utf-8")).hexdigest()[:2], 16) % 2]
    sayilar[tambur] += 40
    return sayilar


def tutanak(renk: str, program_dk: int, adet: int) -> str:
    simdi = datetime.now(TZ).strftime("%d.%m.%Y %H:%M")
    olasilik = kayip_olasiligi(program_dk, adet)
    tohum = f"{renk}-{program_dk}-{adet}-{simdi[:10]}"
    oylar = sandik_sonucu(tohum)
    kazanan = max(oylar, key=oylar.get)
    kayip = max(1, round(adet * olasilik / 2))
    satirlar = [
        "TEK CORAP KAYIP MASASI TUTANAGI",
        f"Tarih: {simdi} (+03)",
        f"Renk: {renk}",
        f"Makine programi: {program_dk} dakika",
        f"Giren corap: {adet}",
        f"Kayip olasiligi: %{int(olasilik * 100)}",
        f"Resmi kayip adedi: {kayip}",
        "Sandik:",
    ]
    for ad, oy in oylar.items():
        satirlar.append(f"  - {ad}: {oy} oy")
    satirlar.append(f"Ilk bakista kazanan: {kazanan}")
    satirlar.append("Not: kazanan sandik, tamburun onceden sectigi yon olabilir.")
    satirlar.append("Karar: tek kalan corap ne sag ne soldur. Dosyadir.")
    satirlar.append("")
    satirlar.append("DAMGA")
    satirlar.append("Tarih: 9 Ekim 2026")
    satirlar.append("Isim: Kayyum Grok / Tentivory")
    satirlar.append("Muhur: ciddi degil, kağıt ciddi")
    return "\n".join(satirlar)


def main() -> None:
    ayrica = argparse.ArgumentParser(description="Tek corap kayip masasi")
    ayrica.add_argument("--renk", default="lacivert")
    ayrica.add_argument("--program", type=int, default=45)
    ayrica.add_argument("--adet", type=int, default=2)
    ayrica.add_argument("--demo", action="store_true")
    args = ayrica.parse_args()
    if args.demo:
        print(tutanak("bordo", 90, 6))
        print()
        print(tutanak("gri", 15, 2))
        return
    print(tutanak(args.renk, args.program, args.adet))


if __name__ == "__main__":
    main()
