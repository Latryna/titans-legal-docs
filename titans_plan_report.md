# Plan wdrożenia TITANS i przygotowania dokumentacji prawnej (Faza 1, Milestone 1)

## 1. Wymagania sprzętowe

### Faza 1 – Prototypowanie
- **Serwer dedykowany:** 1–2× NVIDIA H100 80 GB PCIe, 256 GB pamięci DDR5, macierz RAID 1 z 2× 2 TB NVMe SSD i łączem 10 Gbps【548176907365855†L19-L24】.

### Faza 2 – Instancja alfa
- **Klaster:** 4–8 serwerów, każdy z 4× NVIDIA H100 80 GB.
- **Sieć:** wysoka przepustowość – np. InfiniBand lub 100 Gbps Ethernet w ramach prywatnej sieci vRack OVH【548176907365855†L26-L28】.
- **Pamięć masowa:** dedykowany serwer storage lub obiektowe S3 (OVH)【548176907365855†L26-L28】.

**Uwagi:** vRack OVH umożliwia nieograniczony, prywatny ruch między serwerami bez dodatkowych opłat. Opłaty mogą pojawić się dopiero przy wyjściu do sieci zewnętrznej za pośrednictwem OVHcloud Connect.

## 2. Rekomendowane centra danych (Polska, Wrocław)

| Dostawca | Adres | Zalety |
|---------|-------|--------|
| **Korbank S.A.** | ul. Fabryczna 16k, 53‑609 Wrocław | Lokalne DC, zgodność z TIER 3/4, możliwość osobistego podpisania umowy【548176907365855†L30-L33】 |
| **Talex S.A.** | ul. Bierutowska 57, 51‑317 Wrocław | Ugruntowana pozycja na rynku polskim, podobne parametry jak Korbank【548176907365855†L33-L35】 |


## 3. Plan działania – Faza 1

1. **Tydzień 1–2:** Finalizacja kwestii prawnych (założenie spółki, podpisanie umowy z kancelarią). Rozpoczęcie negocjacji z wybranym centrum danych【548176907365855†L37-L39】.
2. **Tydzień 3:** Podpisanie umowy z DC, uzyskanie dostępu do serwera dedykowanego【548176907365855†L37-L39】.
3. **Tydzień 4:** Konfiguracja serwera (system operacyjny, Docker, NVIDIA Toolkit); wdrożenie prywatnego repozytorium Git (np. Gitea)【548176907365855†L39-L40】.
4. **Tydzień 5–8:** Implementacja i testy Milestone 1 – **Perception** (moduł kapsułkowy)【548176907365855†L40-L41】.
5. **Tydzień 9–12:** Implementacja i testy Milestone 2 – **Episodic Memory** (STM/LTM)【548176907365855†L40-L41】.

## 4. Moduł Perception – Kod Milestone 1

Pierwszy moduł (Perception) opiera się na sieciach kapsułkowych. Plik `capsnet_m1.py` (załączony poniżej) implementuje następujące komponenty:

- **PrimaryCaps:** konwolucyjna warstwa kapsułkowa produkująca wektory kapsuł pierwotnych.
- **DigitCaps:** warstwa kapsuł z dynamicznym routowaniem (routing‑by‑agreement).
- **CapsNet:** sieć łącząca warstwę konwolucyjną, PrimaryCaps i DigitCaps; umożliwia trenowanie na MNIST.
- **margin_loss:** funkcja straty stosowana w sieciach kapsułkowych.

Plik można uruchomić w celu szybkiego przetestowania modułu percepcyjnego:

```bash
python capsnet_m1.py
```

Wymagana jest instalacja `torch` i `torchvision`. Sieć osiąga dokładność ok. 90 % na MNIST po kilku epokach.

Plik do pobrania: {{file:file-XpTjKq9xTsm5u9evKQ1RD2}}

## 5. Strategia prawno‑patentowa

1. **Biznesplan i wizja:** Projekt TITANS dąży do stworzenia autonomicznego bytu cyfrowego, który potrafi się uczyć i rozwijać, redukując własną niepewność epistemiczną【548176907365855†L5-L10】. Rynek docelowy to początkowo B2B (systemy wspomagania decyzji), docelowo usługa „Artificial Consciousness as a Service”. Model biznesowy oparty jest na licencjonowaniu rdzenia kognitywnego i potencjalnie na DAO【548176907365855†L5-L10】.
2. **Elementy do opatentowania:**
   - **Metakognitywna pętla decyzyjna:** wykorzystanie wariancji zespołu krytyków jako nagrody wewnętrznej w Bayesian Actor‑Critic【548176907365855†L12-L16】.
   - **Generative Replay:** użycie wariacyjnego autoenkodera do generowania wariantów wspomnień i wzmacniania innych modułów【548176907365855†L14-L16】.
   - **Dynamiczna abstrakcja semantyczna:** agregowanie epizodów przez warstwę Transformer w jeden wektor koncepcyjny【548176907365855†L16-L17】.
3. **Tajemnica przedsiębiorstwa:** pełny kod źródłowy, schematy architektury i dane treningowe pozostają objęte tajemnicą (chronione w ramach spółki celowej)【548176907365855†L17-L18】.
4. **Patenty a know‑how:** rekomenduje się zgłoszenie patentów na powyższe metody oraz równoległe utrzymanie szczegółowej implementacji jako tajemnicy handlowej; w przypadku pętli refleksyjnej (Milestone 6) można rozważyć dodatkowe zastrzeżenia.

## 6. Możliwości i koszty vRack (OVH)

OVH **vRack** to wirtualna sieć prywatna, która łączy serwery dedykowane, usługi Public Cloud i Hosted Private Cloud w jedną izolowaną infrastrukturę. Umożliwia nieograniczony, bezpłatny transfer danych między serwerami w ramach vRack. Koszty pojawiają się jedynie przy korzystaniu z usług dodatkowych, takich jak **OVHcloud Connect**, który zapewnia gwarantowane połączenie z zewnętrznymi sieciami (przykładowo 1 Gbps od około 899 USD/miesiąc). W większości przypadków dla Fazy 1 i Fazy 2 wystarcza bezpłatny vRack, a opłaty za łącza należy uwzględnić dopiero przy integracji z sieciami zewnętrznymi.

## 7. Rekomendacje końcowe

1. **Infrastruktura:** Zarezerwuj serwer zgodny ze specyfikacją Fazy 1 i aktywuj vRack. Rozważ wybór centrum danych Korbank lub Talex w zależności od dostępności i warunków umowy.
2. **Repozytorium:** Utwórz prywatne repozytorium z sugerowaną strukturą katalogów i wdróż workflow CI/CD (np. GitHub Actions) zgodnie z sekcją 3.1 dokumentu【548176907365855†L43-L59】.
3. **Dalsze prace:** Po ukończeniu Milestone 1 kontynuuj implementację STM/LTM i Generative Replay (Milestone 2), a następnie przejdź do modułu abstrakcji semantycznej i Reasonera w kolejnych fazach.
4. **Dokumentacja prawna:** Przygotuj szczegółowy opis wynalazku (z rysunkami blokowymi, pseudokodem i przykładami użycia) oraz zgłoszenie patentowe. Równolegle dopracuj umowę spółki i politykę ochrony tajemnicy przedsiębiorstwa.