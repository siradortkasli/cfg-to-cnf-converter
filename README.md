# CFG → CNF Dönüştürücü

Python kullanılarak geliştirilmiş, **bağlamdan bağımsız gramerleri (Context-Free Grammar, CFG)** **Chomsky Normal Form'a (CNF)** dönüştürmeye yönelik bir algoritma uygulamasıdır. Biçimsel Diller ve Otomata Teorisi kapsamında gramer dönüşüm adımlarını uygulamak ve örnekler üzerinden incelemek amacıyla hazırlanmıştır.

## Özellikler

- Boş (ε) üretimlerini kaldırma
- Birim üretimleri kaldırma
- Kullanışsız ve erişilemeyen üretimleri temizleme
- Uzun üretimlerde terminal semboller için yeni değişkenler oluşturma
- İkiden fazla sembol içeren üretimleri ikili üretimlere ayırma
- Başlangıç sembolünü gerektiğinde yeniden düzenleme
- Üç örnek grameri işleyip dönüşüm sonuçlarını konsola yazdırma

## Kullanılan teknolojiler

- **Python 3**
- Standart kütüphane: `collections.defaultdict`
- Gramer işleme ve dönüşüm algoritmaları

## Çalıştırma

Python 3 yüklüyken bu depoyu indirip terminalde çalıştırın:

```bash
python cfg_to_cnf.py
```

Harici paket kurulumu gerekmez. Program içindeki `ornek_gramerler` listesinde bulunan üç gramer sırayla dönüştürülür ve çıktılar terminalde gösterilir. Yeni örnekler için bu liste düzenlenebilir.

## Gramer gösterimi

Gramerler, her değişken için üretim alternatiflerini içeren Python sözlüğü biçiminde tanımlanır:

```python
gramer = {
    "S": [["A", "B"], ["b"]],
    "A": [["a"], ["S"]],
    "B": [["b"], ["A", "a"]],
}
```

Boş üretimler `"ε"` sembolüyle gösterilir.

## Teknik notlar ve geliştirme alanları

Bu uygulama eğitim amaçlı bir algoritma çalışmasıdır. Mevcut sürüm örnek gramerleri işleyip çıktı üretse de **tüm durumlarda biçimsel olarak geçerli CNF çıktısı garantisi verilmemektedir**. Özellikle yeni oluşturulan terminal değişkenleri sonrasında tek değişkenli üretimler kalabilir. Dönüştürme sırasının ve CNF geçerlilik kontrollerinin geliştirilmesi planlanabilir.

## Dosya

- `cfg_to_cnf.py`: Gramer dönüşüm sınıfı, yardımcı yazdırma işlevi ve üç örnek gramer.
