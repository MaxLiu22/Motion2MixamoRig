# Motion2MixamoRig dla Blendera — Przewodnik użytkownika

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · Polski · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Zamień nagranie wideo z jedną osobą w animowaną postać z Mixamo — prosto w Blenderze.
Nie musisz programować ani korzystać z terminala.

<!-- video: link the tutorial video here -->

> Na razie przetestowano tylko na **macOS (Apple Silicon)**. Wersja dla Windows jest już w drodze.

## Czego potrzebujesz

- **Blender 4.2 lub nowszy**
- **Połączenie z internetem** przy pierwszej konfiguracji
- **Około 8 GB wolnego miejsca na dysku** (środowisko ~1,3 GB + modele ~5,6 GB)
- **Darmowe konto SMPL-X** i **darmowe konto Adobe** (do Mixamo); zobacz kroki 4 i 5

## 1. Pobierz dodatek

Wejdź na stronę [najnowszego wydania](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
i pobierz zip dla swojego komputera:

| Twój komputer | Plik |
| --- | --- |
| Mac z Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Wkrótce** |

Na przykład w `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` to wersja
dodatku, a `macos-arm64` to platforma. Jeśli wybierzesz zły plik, Blender
odmówi instalacji i poda, jakiej platformy oczekiwał.

**Nie** rozpakowuj go. Blender sam instaluje plik zip.

## 2. Zainstaluj go w Blenderze

1. **Edit → Preferences → Get Extensions**
2. Kliknij małe **∨** w prawym górnym rogu → **Install from Disk…**
3. Wybierz plik zip. **Motion2MixamoRig** pojawi się na liście, już włączony.
4. Zamknij Preferences. W 3D Viewport naciśnij **N**, a potem kliknij kartę
   **Motion2MixamoRig** po prawej stronie.

<!-- screenshot: Install from Disk menu -->

## 3. Zainstaluj środowisko (jednorazowo)

W panelu kliknij **Zainstaluj środowisko (jednym kliknięciem)** (Install Runtime (one click)).

Dodatek pobiera własnego Pythona i biblioteki (~1,4 GB) do
`~/Motion2MixamoRig/`. Nie zmienia niczego innego na twoim komputerze. Trwa to
kilka minut; pasek postępu pokazuje bieżący krok.

<!-- screenshot: Install Runtime button and progress -->

## 4. Pobierz model ciała SMPL-X

SMPL-X to darmowy model ciała, którego potrzebuje dodatek. Jego licencja nie
pozwala nam go dołączać, więc pobierasz go sam, jednorazowo:

1. Otwórz [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) i kliknij **Register**.
   Zaakceptuj licencję i potwierdź adres e-mail.
2. Zaloguj się, otwórz **Download** i pobierz model SMPL-X (wersję **NPZ**).
3. Rozpakuj go i znajdź **`SMPLX_NEUTRAL.npz`**.
4. W Blenderze kliknij **Wybierz model SMPL-X…** (Choose SMPL-X Model…) i wskaż
   ten plik. Panel pokaże wtedy **Model SMPL-X: znaleziono** (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Pobierz postać z Mixamo

1. Otwórz [mixamo.com](https://www.mixamo.com/) i zaloguj się kontem Adobe.
2. Karta **Characters** → wybierz postać (na przykład **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Wygeneruj ruch

W sekcji **Dane wejściowe** (Input):

1. **Typ źródła** (Source Type): **Wideo** (Video) (albo **Obraz** (Image) dla pojedynczej pozy)
2. **Plik źródłowy** (Source File): twój klip. Musi pokazywać **dokładnie jedną
   osobę, od stóp do głów w kadrze przez cały czas**.
3. **Postać Mixamo FBX** (Mixamo Rig FBX): postać z kroku 5
4. **Wykrywaj dłonie** (Detect Hands) jest wyłączone. Włącz je tylko wtedy, gdy
   palce mają się ruszać. Potem kliknij **Wybierz model dłoni MANO…** (Choose MANO
   Hand Model…) i wskaż `MANO_RIGHT.pkl`. Plik bierzesz tak jak SMPL-X: zarejestruj
   się na [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/), pobierz **Models & Code**
   i rozpakuj. Pierwsze przejście dłoni dociąga jednorazowo około **2,7 GB** i trwa
   mniej więcej dwa razy dłużej niż przebieg samego ciała. Po włączeniu pojawia się **Finger Smoothing (seconds)**. Wygładza ruch palców. Domyślnie 0,08 sekundy; 0 zostawia to, co wykryto.
5. Kliknij **Generuj ruch** (Generate Motion)

Po zakończeniu animowana postać zostanie automatycznie zaimportowana do
twojej sceny. Postawiona stopa zostaje tam, gdzie stanęła, a podeszwa leży na podłodze Blendera. Na tej podłodze dochodzi mesh **Znaczniki podłogi** (Floor Markers) (krzyż co 0,5 m). Pole **Znaczniki podłogi** (Floor Markers) w sekcji Postęp / wynik pokazuje je albo ukrywa.

### Pierwsze uruchomienie trwa dłużej — to normalne

Za pierwszym razem dodatek pobiera około **5,6 GB** modeli. Panel pokazuje
rozmiar pobierania, prędkość i pozostały czas. Modele pobierają się tylko raz.

Potem wideo jest przetwarzane na twoim komputerze. Na procesorze Maca
10-sekundowy klip zajmuje kilka minut. W tym czasie możesz dalej korzystać
z Blendera, a **Anuluj** (Cancel) przerywa zadanie.

## Wskazówki dla dobrych wyników

- Tylko jedna osoba, widoczna cała sylwetka, nieucięta przy krawędziach kadru
- Stabilna kamera, dobre światło, proste ubranie zamiast luźnego lub powiewnego
- Krótkie klipy (5–20 sekund) szybciej sprawdzisz na początek

## Aktualizacja do nowej wersji

Dodatek jest często aktualizowany. Aby go zaktualizować:

1. Pobierz najnowszy zip ze strony
   [najnowszego wydania](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → usuń stary **Motion2MixamoRig**, całkowicie zamknij
   Blendera (**Cmd+Q**), uruchom go ponownie i zainstaluj nowy zip.
3. W panelu kliknij **Zaktualizuj środowisko** (Update Runtime).

Aktualizacja zachowuje pobrane modele, więc trwa krótko. Zainstalowana wersja
jest widoczna obok dodatku w **Get Extensions**.

## Panel

- **⚙ obok tytułu** pokazuje lub ukrywa sekcję **Konfiguracja** (Setup).
- **Konfiguracja**: język, środowisko, SMPL-X, urządzenie (**Urządzenie** (Device);
  CPU to bezpieczny wybór) oraz **Sprawdź środowisko** (Check Environment).
- **Dane wejściowe**: co ma zostać animowane, **Model ciała** (Body Model, GVHMR) i **Wykrywaj dłonie** (Detect Hands).
- **Postęp / wynik** (Progress / Result): postęp, ostatnie wpisy logu, a po
  zakończeniu zadania **Importuj wygenerowaną postać** (Import Generated Character), **Znaczniki podłogi** (Floor Markers),
  **Otwórz folder wyjściowy** (Open Output Folder) i **Pokaż pełny log** (View Full Log).
- **Diagnostyka** (Diagnostics): miejsca, w których części ciała postaci
  wchodzą w siebie (dłoń w głowie, skrzyżowane ręce). Czerwone komórki na
  pasku to klatki z problemem; kliknij jedną, aby tam przejść. Trójkąt pod
  paskiem podąża za bieżącą klatką, a pod nim widać, które części się
  przenikają i jak głęboko. **Poprzedni** / **Następny** (Previous / Next)
  przechodzą między problemami. **Otwórz raport HTML** (Open HTML Report)
  otwiera w przeglądarce raport z wideo źródłowym obok postaci (za pierwszym
  razem tworzenie trwa około 15 sekund). Oryginalne wideo wymaga ffmpeg na komputerze (na Macu: `brew install ffmpeg`). Bez niego postać jest, a wideo obok pozostaje puste. Postać stoi na stałych krzyżach podłogi, co 0,5 m, żeby było widać, czy się ślizga. Bursztynowy pas nad czerwonymi ścieżkami służy do uwag, które zauważysz na oko. Są na liście **Notes** po prawej; kliknięcie wiersza przenosi do niego. **Download notes** zapisuje te uwagi razem z czasami przenikania. Plik nazywa się jak wideo źródłowe.

Dodatek mówi w 19 językach. **Automatycznie (Blender / system)**
(Auto (Blender / System)) podąża za językiem Blendera; zmienisz to w sekcji
Konfiguracja w polu **Język interfejsu** (UI Language).

## Gdy coś pójdzie nie tak

| Co widzisz | Co zrobić |
| --- | --- |
| **Instalacja środowiska nie powiodła się** (Runtime installation failed) | Sprawdź połączenie z internetem i kliknij przycisk jeszcze raz. Log: `~/Motion2MixamoRig/logs/setup.log` |
| **Model SMPL-X: brak** (SMPL-X model: missing) | Powtórz krok 4 i wskaż `SMPLX_NEUTRAL.npz` |
| **Model dłoni MANO: brak** (MANO hand model: missing) | Włącz **Wykrywaj dłonie**, potem **Wybierz model dłoni MANO…** i wskaż `MANO_RIGHT.pkl` |
| **Nieprawidłowy plik Mixamo FBX** (Mixamo FBX invalid) | Pobierz postać ponownie jako **FBX Binary**, **T-pose** |
| **Na nagraniu jest więcej niż jedna osoba** (Input contains multiple people) | Użyj klipu z tylko jedną osobą |
| **Nie wykryto żadnej osoby** (No person was detected in the input) | Upewnij się, że widać całe ciało i jest dobrze oświetlone |
| **Proces pipeline'u nieoczekiwanie się zakończył** (Pipeline process exited unexpectedly) | Kliknij **Pokaż pełny log** |

Gdy prosisz o pomoc, dołącz log i napisz, której wersji dodatku używasz.

## Odinstalowanie

1. **Get Extensions** → usuń **Motion2MixamoRig**.
2. Usuń folder **`~/Motion2MixamoRig`** (twój folder domowy →
   `Motion2MixamoRig`). Usunięcie dodatku **nie** usuwa tego folderu, a zajmuje
   on około 7 GB (środowisko i modele) oraz zawiera twoje wygenerowane wyniki
   w `app/outputs/`.

## Licencja

Motion2MixamoRig jest przeznaczony **wyłącznie do użytku niekomercyjnego**:
korzysta z modeli badawczych (takich jak GVHMR i SMPL-X), których licencje nie
pozwalają na użycie komercyjne. Zobacz [`NOTICE.md`](../../NOTICE.md).
