#1306220033 Emine Ersöz
import os

# Koordinatları satır ve sütun indekslerine dönüştürme
def koordinati_indekse_cevir(koordinat):
    if not koordinat_dogrula(koordinat):
        return None, None
    satir_harf = koordinat[0]
    sutun_str = koordinat[1:]
    satir_indeks = ord(satir_harf) - ord('A')
    sutun_indeks = int(sutun_str) - 1
    return satir_indeks, sutun_indeks

# İndeksleri koordinatlara dönüştürme
def indeksi_koordinata_cevir(satir_indeks, sutun_indeks):
    if not (0 <= satir_indeks <= 9 and 0 <= sutun_indeks <= 9):
        return None
    satir_harf = chr(ord('A') + satir_indeks)
    sutun_str = str(sutun_indeks + 1)
    return satir_harf + sutun_str

# Oyun tahtasını başlatma
def tahta_olustur():
    # '.' boş hücreyi, 'S' gemi parçasını, 'X' vurulan gemi parçasını, 'O' ıska atışını temsil eder.
    return [['.' for _ in range(10)] for _ in range(10)]

# Tahtayı ekrana yazdırma
def tahtayi_goster(tahta, tahta_adi="Tahta"):
    print(f"\n--- {tahta_adi} ---")
    print("   1  2  3  4  5  6  7  8  9 10")
    print("  ------------------------------")
    for i, satir in enumerate(tahta):
        print(f"{chr(ord('A') + i)} | {'  '.join(satir)}")
    print("  ------------------------------")

# Gemi yerleşimini doğrulama; koordinatlar tahta üzerinde mi çakışma vs var mı vb.
def gemi_yerlesimi_dogrula(koordinatlar, tahta):
    if not koordinatlar:
        return False, "Gemi koordinatları boş olamaz."

    indeks_koordinatlari = []
    for k in koordinatlar:
        r, c = koordinati_indekse_cevir(k)
        if r is None or c is None or not (0 <= r <= 9 and 0 <= c <= 9):
            return False, f"'{k}' koordinatı tahta sınırları dışında veya geçersiz."
        indeks_koordinatlari.append((r, c))

    # Çakışma kontrolü (Tahtada 'S' olan bir yere yerleştirme)
    for r, c in indeks_koordinatlari:
        if tahta[r][c] == 'S':
            return False, f"'{indeksi_koordinata_cevir(r, c)}' koordinatı zaten dolu. Çakışma var."
            
    # Yatay veya dikey hizalama kontrolü
    ilk_satir, ilk_sutun = indeks_koordinatlari[0]
    yatay_hizali = True
    dikey_hizali = True

    for i in range(1, len(indeks_koordinatlari)):
        satir, sutun = indeks_koordinatlari[i]
        if satir != ilk_satir:
            yatay_hizali = False
        if sutun != ilk_sutun:
            dikey_hizali = False

    if not (yatay_hizali or dikey_hizali):
        return False, "Gemi koordinatları yatay veya dikey hizalı değil."

    # Koordinatların ardışık olup olmadığını kontrol et (boşluk olmamalı)
    if yatay_hizali:
        sutunlar = sorted([c for r, c in indeks_koordinatlari])
        if not all(sutunlar[i] == sutunlar[i-1] + 1 for i in range(1, len(sutunlar))):
            return False, "Yatay gemi koordinatları ardışık değil."
    elif dikey_hizali:
        satirlar = sorted([r for r, c in indeks_koordinatlari])
        if not all(satirlar[i] == satirlar[i-1] + 1 for i in range(1, len(satirlar))):
            return False, "Dikey gemi koordinatları ardışık değil."

    # Gemiler arası boşluk kontrolü (çapraz ve bitişik)
    for r, c in indeks_koordinatlari:
        for i in range(-1, 2): # -1, 0, 1
            for j in range(-1, 2): # -1, 0, 1
                if i == 0 and j == 0: # Kendisini kontrol etme
                    continue
                komsu_r, komsu_c = r + i, c + j
                if 0 <= komsu_r <= 9 and 0 <= komsu_c <= 9:
                    # Komşu hücrede başka bir gemi parçası ('S') var mı kontrol et
                    if tahta[komsu_r][komsu_c] == 'S':
                        # Eğer bu komşu hücre, yerleştirilmek istenen geminin bir parçası değilse hata ver
                        if (komsu_r, komsu_c) not in indeks_koordinatlari:
                            return False, "Gemiler arasında yeterli boşluk yok (bitişik veya çapraz)."
    return True, "Geçerli yerleşim."

# Gemi koordinatlarını al ve doğrula
def gemi_koordinatlarini_al(gemi_uzunlugu, gemi_adi, mevcut_tahta):
    while True:
        koordinatlar = []
        print(f"{gemi_uzunlugu} uzunluğundaki '{gemi_adi}' gemisi için koordinatları girin (örn. A5 B5 C5):")
        girdi = input("   Tüm koordinatları boşlukla ayırarak girin: ").upper().split()

        if len(girdi) != gemi_uzunlugu:
            print(f"   Hata: Bu gemi için {gemi_uzunlugu} adet koordinat girmelisiniz. {len(girdi)} adet girdiniz.")
            continue

        gecerli_girdi = True
        for k in girdi:
            if not koordinat_dogrula(k):
                print(f"   Hata: '{k}' geçersiz bir koordinat biçimi.")
                gecerli_girdi = False
                break
            koordinatlar.append(k)

        if not gecerli_girdi:
            continue

        # Yerleşimi doğrula
        gecerli, mesaj = gemi_yerlesimi_dogrula(koordinatlar, mevcut_tahta)
        if gecerli:
            # Gemiyi tahtaya yerleştir
            for k in koordinatlar:
                r, c = koordinati_indekse_cevir(k)
                mevcut_tahta[r][c] = 'S'
            tahtayi_goster(mevcut_tahta, "Kendi Gemileriniz")  
            return koordinatlar
        else:
            print(f"   Yerleşim hatası: {mesaj} Lütfen tekrar deneyin.")

# Koordinat formatını doğrulama fonksiyonu
def koordinat_dogrula(koordinat):
    if len(koordinat) < 2 or len(koordinat) > 3:
        return False
    satir = koordinat[0]
    sutun = koordinat[1:]
    if 'A' <= satir <= 'J' and sutun.isdigit() and 1 <= int(sutun) <= 10:
        return True
    return False

# Gemi koordinatlarını dosyaya yazma
def gemileri_dosyaya_yaz(dosya_adi="1stships.txt", gemi_verisi=[]):
    try:
        with open(dosya_adi, 'w') as f:
            for gemi in gemi_verisi:
                f.write(",".join(gemi) + "\n")
        return True
    except Exception as e:
        print(f"Dosyaya yazma hatası: {e}")
        return False

# Gemi dosyasını oluşturma
def gemi_dosyasi_olustur(dosya_adi="1stships.txt"):
    try:
        if not os.path.exists(dosya_adi):
            with open(dosya_adi, 'w') as f:
                pass
        return True
    except Exception as e:
        print(f"Dosya oluşturma hatası: {e}")
        return False

# Hedef dosyasını oluşturma
def hedef_dosyasi_olustur(dosya_adi="2ndaim.txt"):
    try:
        if not os.path.exists(dosya_adi):
            with open(dosya_adi, 'w') as f:
                pass
        return True
    except Exception as e:
        print(f"Dosya oluşturma hatası: {e}")
        return False

# Hedef koordinatlarını alma ve doğrulama
def hedef_koordinati_al(vurulan_hedef_koordinatlari):
    while True:
        koordinat = input("Hedef koordinatı girin (örn. A5): ").upper()
        if not koordinat_dogrula(koordinat):
            print("Geçersiz koordinat. Lütfen tekrar deneyin.")
            continue
        if koordinat in vurulan_hedef_koordinatlari:
            print("Bu koordinata zaten ateş ettiniz. Lütfen farklı bir koordinat girin.")
            continue
        return koordinat

# İsabet mi iska mı kontrol etme
def isabet_mi_iska_mi(hedef_koordinati, tum_gemi_bilgisi):
    r, c = koordinati_indekse_cevir(hedef_koordinati)
    if r is None or c is None:
        return "Iska", hedef_koordinati, [] 

    # Koordinatın bir gemiye ait olup olmadığını kontrol et
    for gemi_adi, gemi_detaylari in tum_gemi_bilgisi.items():
        if hedef_koordinati in gemi_detaylari['koordinatlar']:
            # Vurulan parça sayısını güncelle
            gemi_detaylari['vurulan_parcalar'] += 1

            etraf_koordinatlari_batinca = []
            # Gemi batırıldığında etrafını işaretle
            if gemi_detaylari['vurulan_parcalar'] == len(gemi_detaylari['koordinatlar']):
                print(f"Tebrikler! '{gemi_adi}' gemisini batırdınız!")
                for gemi_kord in gemi_detaylari['koordinatlar']:
                    gr, gc = koordinati_indekse_cevir(gemi_kord)
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if 0 <= gr + i <= 9 and 0 <= gc + j <= 9:
                                etraf_koordinatlari_batinca.append(indeksi_koordinata_cevir(gr + i, gc + j))
                return "Vurdu", hedef_koordinati, etraf_koordinatlari_batinca
            else:
                return "Vurdu", hedef_koordinati, []
    
    return "Iska", hedef_koordinati, []

# Hedef dosyasını güncelleme
def hedef_dosyasini_guncelle(dosya_adi="2ndaim.txt", hedef_koordinati="", sonuc=""):
    try:
        with open(dosya_adi, 'a') as f:
            f.write(f"{hedef_koordinati},{sonuc}\n")
        return True
    except Exception as e:
        print(f"Dosyaya yazma hatası: {e}")
        return False

# Tüm gemilerin batırılıp batırılmadığını kontrol etme
def oyun_bitti_mi(tum_gemi_bilgisi):
    for gemi_adi, gemi_detaylari in tum_gemi_bilgisi.items():
        # Eğer bir geminin vurulan parça sayısı, toplam boyutundan az ise
        if gemi_detaylari['vurulan_parcalar'] < len(gemi_detaylari['koordinatlar']):
            return False 
    return True  # Tüm gemiler batırıldı

if __name__ == "__main__":
    print("Amiral Battı Oyununa Hoşgeldiniz!")
    # 1. Gemi Yerleşimi
    gemi_dosyasi_olustur()
    oyuncu_gemileri_tahtasi = tahta_olustur() # Oyuncunun kendi gemilerini yerleştirdiği tahta
    oyuncu_atis_tahtasi = tahta_olustur()     # Oyuncunun atışlarını takip ettiği tahta (rakip tahtası)

    yerlestirilecek_gemiler = [
        ("5-uzunluk", 5),
        ("4-uzunluk", 4),
        ("3-uzunluk-1", 3),
        ("3-uzunluk-2", 3),
        ("2-uzunluk-1", 2),
        ("2-uzunluk-2", 2),
        ("1-uzunluk-1", 1),
        ("1-uzunluk-2", 1),
        ("1-uzunluk-3", 1)
    ]
    
    # Her gemi için koordinatları ve vurulan parça sayısını tutar
    tum_gemi_bilgisi = {} 

    print("    Gemi Yerleşimi  ")
    tahtayi_goster(oyuncu_gemileri_tahtasi, "Kendi Gemileriniz")

    for gemi_adi, gemi_uzunlugu in yerlestirilecek_gemiler:
        gemi_koordinatlari = gemi_koordinatlarini_al(gemi_uzunlugu, gemi_adi, oyuncu_gemileri_tahtasi)
        
        # Gemi bilgilerini tum_gemi_bilgisi sözlüğüne ekle
        tum_gemi_bilgisi[gemi_adi] = {
            'koordinatlar': gemi_koordinatlari,
            'vurulan_parcalar': 0 # Başlangıçta hiç vurulmamış
        }

        print(f"\n'{gemi_adi}' gemisi yerleştirildi. Güncel tahta:")
        tahtayi_goster(oyuncu_gemileri_tahtasi, "Kendi Gemileriniz")

    # Tüm gemi koordinatlarını dosyaya yazma
    dosyaya_yazilacak_gemi_koordinatlari = [detay['koordinatlar'] for detay in tum_gemi_bilgisi.values()]
    gemileri_dosyaya_yaz(dosya_adi="1stships.txt", gemi_verisi=dosyaya_yazilacak_gemi_koordinatlari)

    # 2. Hedef Alma (İkinci Oyuncu)
    hedef_dosyasi_olustur()
    print("\n    Hedef Alma (İkinci Oyuncu)    ")
    print("Bu tahta rakibin gemi yerleşimini tahmin etmek için yaptığınız atışları gösterir.")
    tahtayi_goster(oyuncu_atis_tahtasi, "Rakip Tahtası (Atışlarınız)")

    vurulan_hedef_koordinatlari = set()  # Vurulan koordinatları saklamak için bir liste
    atis_sayisi = 1

    while not oyun_bitti_mi(tum_gemi_bilgisi):
        print(f"\n{atis_sayisi}. Atış:")
        hedef = hedef_koordinati_al(vurulan_hedef_koordinatlari)
        vurulan_hedef_koordinatlari.add(hedef)  # Vurulan koordinatı listeye ekle
        
        # İsabet mi ıska mı kontrol et
        isabet, vurulan_koordinat, etraf_koordinatlari_batinca = isabet_mi_iska_mi(hedef, tum_gemi_bilgisi)
        
        hedef_dosyasini_guncelle(dosya_adi="2ndaim.txt", hedef_koordinati=hedef, sonuc=isabet)
        print(f"{hedef}'e atış: {isabet}")

        r, c = koordinati_indekse_cevir(hedef)  # Hedef koordinatını indekslere çevir

        if isabet == "Vurdu":
            oyuncu_atis_tahtasi[r][c] = 'X'  # Rakip tahtasında vurulan gemi parçasını işaretle
            
            # Gemi batırıldıysa etrafını işaretle
            if etraf_koordinatlari_batinca: 
                for etraf_koord in etraf_koordinatlari_batinca:
                    etraf_r, etraf_c = koordinati_indekse_cevir(etraf_koord)
                    if etraf_r is not None and etraf_c is not None and \
                       oyuncu_atis_tahtasi[etraf_r][etraf_c] == '.': # Sadece boş yerleri işaretle
                        oyuncu_atis_tahtasi[etraf_r][etraf_c] = 'O'  # Etrafındaki boş yerleri ıska olarak işaretle
            else: # Gemi vuruldu ama batmadıysa, vurulan noktanın etrafını işaretle
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        komsu_r, komsu_c = r + i, c + j
                        ''' Sadece geçerli sınırlar içindeki, henüz atış yapılmamış ('.') olan ve 
                         kendi gemi tahtamızda 'S' olmayan yerleri işaretle'''
                        if 0 <= komsu_r <= 9 and 0 <= komsu_c <= 9 and \
                           oyuncu_atis_tahtasi[komsu_r][komsu_c] == '.' and \
                           oyuncu_gemileri_tahtasi[komsu_r][komsu_c] != 'S': 
                            oyuncu_atis_tahtasi[komsu_r][komsu_c] = 'O'

        else:
            oyuncu_atis_tahtasi[r][c] = 'O'  # Rakip tahtasında ıska atışını işaretle

        tahtayi_goster(oyuncu_atis_tahtasi, "Rakip Tahtası (Atışlarınız)") # Atış tahtasını göster
        atis_sayisi += 1

        # Her atıştan sonra oyunun bitip bitmediğini kontrol et
        if oyun_bitti_mi(tum_gemi_bilgisi):
            print("\n    Oyun Sona Erdi!    ")
            print("Tüm gemiler batırıldı. İkinci oyuncu oyunu kazandı!")
            break 

    print("\nOyun sona erdi. Gemi ve koordinat dosyalarınızı kontrol edin.")