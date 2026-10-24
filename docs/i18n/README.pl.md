# Motion2MixamoRig

<p align="center">
  <a href="#wymagania"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.pl.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · Polski · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Przenieś ruch osoby z nagrania wideo — albo pozę ze zdjęcia — na postać 3D zriggowaną w Adobe Mixamo.

Dla twórców gier: podaj nagranie akcji z **jedną osobą** (albo zdjęcie) i postać z Mixamo; narzędzie wygeneruje filmy podglądowe oraz plik postaci ze skinningiem (`.glb`), który możesz od razu wczytać do Blendera lub Unity.

> Motion2MixamoRig jest na razie eksperymentalny. Wersja 0.1.8 to pipeline wiersza poleceń. To repozytorium zawiera też rozszerzenie Blender 4.2+ Extension, które uruchamia ten sam pipeline w zewnętrznym środowisku Pythona. Budowanie dodatku ze źródeł: [`blender_extension/README.md`](../../blender_extension/README.md).

## Dwa sposoby użycia

### 🎨 W Blenderze — bez programowania

1. Pobierz zip dla swojej platformy, np. `motion2mixamorig-<version>-macos-arm64.zip`, ze strony [najnowszego wydania](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. W Blenderze: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, wybierz plik zip.
3. 3D Viewport → naciśnij **N** → karta **Motion2MixamoRig** → **Zainstaluj środowisko (jednym kliknięciem)** (Install Runtime (one click)).
4. **Wybierz model SMPL-X…** (Choose SMPL-X Model…) (darmowe pobranie) i wskaż plik FBX postaci z Mixamo.
5. Wybierz nagranie z jedną osobą → **Generuj ruch** (Generate Motion).

Instrukcje krok po kroku, wskazówki i aktualizacja: **[Przewodnik użytkownika](user-guide.pl.md)**. Przetestowano na macOS (Apple Silicon).

### 💻 Wiersz poleceń — dla programistów

Sklonuj repozytorium i uruchom pipeline samodzielnie: zacznij od sekcji [Wymagania](#wymagania).

Agenci powinni zacząć od [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Otwórz <a href="../assets/demo.mp4">demo.mp4</a> w tym repozytorium.</sub>
</p>

Kolejne demo:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Raport diagnostyczny (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Wymagania

Python 3.11+. Po sklonowaniu utwórz virtualenv i zainstaluj zależności; potem polecenie `m2mr` będzie dostępne:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Zainstaluj zależności i ten projekt. chumpy (stary pakiet w łańcuchu zależności)
# importuje pip w swoim skrypcie setup, więc w domyślnym izolowanym buildzie pip
# kończy się błędem "No module named 'pip'". Najpierw zainstaluj go z wyłączoną
# izolacją, a dopiero potem ten projekt.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Wagi modeli (GVHMR itd.) nie są pobierane na tym etapie. Pierwsze `m2mr run` pobierze je do `weights/` (~5 GB, tylko raz). Pierwsze `m2mr run --detect-hands` pobiera też wagi dłoni HaMeR do `weights/hamer/` (~2,7 GB, tylko raz).

Zalecane jest zainstalowanie ffmpeg (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
Pipeline działa bez niego, ale wynikowe filmy będą **bez dźwięku** i nie odtworzą się w przeglądarce.

## Zanim uruchomisz: umieść te pliki w `assets/`

To repozytorium nie zawiera tych plików; musisz je pobrać samodzielnie. Nazwa pliku SMPL-X musi dokładnie odpowiadać tabeli; nazwy plików FBX, wideo i zdjęć są dowolne. Każde uruchomienie wymaga SMPL-X, postaci z Mixamo oraz **albo** wideo, **albo** zdjęcia. Postacie Mixamo ponownie wyeksportowane z Cinema 4D też działają; zobacz [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Co | Gdzie | Skąd |
|---|---|---|
| Model ciała SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Zarejestruj się na stronie [SMPL-X](https://smpl-x.is.tue.mpg.de/) i pobierz plik |
| FBX postaci z Mixamo | `assets/mixamo/Y_Bot.fbx` | Za pomocą konta Adobe pobierz Y Bot (lub dowolną inną postać zriggowaną w Mixamo) z [Mixamo](https://www.mixamo.com) |
| Nagranie akcji | `assets/video/<your_clip>.mp4` | Klip z **dokładnie jedną** wyraźnie widoczną osobą, **od stóp do głów przez cały czas w kadrze** (możesz trzymać kilka plików; każde uruchomienie używa ostatnio dodanego) |
| Zdjęcie pozy (opcjonalnie) | `assets/image/<your_photo>.jpg` | Zdjęcie z **dokładnie jedną** wyraźnie widoczną osobą, **od stóp do głów w kadrze**. Używane z `--image` |
| Prawa dłoń MANO (tylko dla `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Zarejestruj się na [MANO](https://mano.is.tue.mpg.de/) i pobierz **Models & Code**. Przebieg samego ciała nie potrzebuje tego pliku |

Uwaga: plik pobrany z Mixamo nazywa się `Y Bot.fbx` (**ze spacją**), czyli różni się jednym znakiem od `Y_Bot.fbx` (**z podkreślnikiem**) w tabeli.
Zmień nazwę na wersję z podkreślnikiem, a stanie się domyślnym rigiem (`m2mr run` bez `--rig`). Pozostawienie spacji też działa — jeśli brakuje `Y_Bot.fbx`, użyty zostanie pierwszy plik `.fbx` z `assets/mixamo/`.

`assets/video/` może zawierać kilka filmów. Bez `--video` ani `--image` uruchomienie używa pliku **ostatnio dodanego** do `assets/video/`; jeśli ten folder jest pusty, używane jest najnowsze zdjęcie z `assets/image/`.
Każdy klip lub zdjęcie może pokazywać tylko jedną osobę, **od stóp do głów w kadrze** — nic nie może być ucięte na krawędziach. `m2mr doctor` / `m2mr run` zatrzymają się przed ekstrakcją, jeśli w kadrze są dwie osoby.

## Szybki start

Wyniki trafiają do `outputs/<run-time>_<source>/`. Uruchomienia z wideo zapisują `videos/`; uruchomienia ze zdjęcia zapisują `images/`.

### 1. Sprawdź zasoby i środowisko

Wszystko, czego brakuje, zostanie wypisane razem z informacją, skąd to pobrać i gdzie umieścić.

```bash
m2mr doctor
```

`m2mr doctor` sprawdza przebieg ciała. Nie wymaga modelu dłoni MANO. Żeby sprawdzić też dodatkowy plik i pakiety Pythona używane do wykrywania palców:

```bash
m2mr doctor --detect-hands
```

### 2. Pierwsze uruchomienie: zobacz wynik na ekranie

Bez żadnych opcji polecenie używa **najnowszego pliku z `assets/video/`** oraz `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

To najwolniejszy krok. Pierwsze uruchomienie pobiera ~5 GB wag modeli (tylko raz), a potem wyodrębnia ruch człowieka z nagrania.
Na CPU ekstrakcja klipu o długości ~30 sekund trwa około 8–15 minut; kolejne uruchomienia o podobnej długości, gdy wagi są już pobrane, trwają około 3–5 minut.
Retargeting i renderowanie zajmują zwykle minutę lub dwie. Ponowne użycie szkieletu przez `--skeleton` w następnej sekcji całkowicie pomija ekstrakcję i kończy się w kilkadziesiąt sekund.

Postawiona stopa jest domyślnie przypinana: śródstopie, gdy śródstopie jest na dole, pięta tylko gdy palce są uniesione. Jeśli wyprostowana noga nie sięga tego punktu, biodra się przesuwają. Potem podeszwa jest stawiana na podłodze (y = 0). `--no-foot-lock` zostawia surowy retarget, więc stopy mogą się ślizgać; podeszwa i tak ląduje na podłodze.

### 3. Ten sam ruch, inna postać

Pobierz inną postać z Mixamo do `assets/mixamo/`. **Nie uruchamiaj ponownie tylko z `--rig`** — to powtórzy wolną ekstrakcję.
Podaj `--skeleton`, aby ponownie użyć szkieletu z poprzedniego uruchomienia; minuty zamieniają się w kilkadziesiąt sekund:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Inne nagranie

`--video` wybiera klip. Można go dowolnie łączyć z `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Zdjęcie (poza statyczna)

`--image` odtwarza **statyczną pozę 3D** ze zdjęcia jednej osoby, a następnie przenosi ją na postać z Mixamo tak samo jak w przypadku wideo. Podgląd to cztery obrazy w `images/` (te same widoki co przy wideo) oraz klip z obrotem w lewo/prawo `before_after_360_compare.mp4`. Nie podawaj jednocześnie `--video`.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` bez ścieżki używa pliku ostatnio dodanego do `assets/image/`.

### 6. Sprawdzanie samoprzenikania

Każde uruchomienie sprawdza też gotową postać pod kątem **samoprzenikania** — gdy jedna część ciała wchodzi w inną, np. dłoń w głowę — i zapisuje `diagnostics.json`. Terminal wypisuje jedną linię, np. `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Podłoga nie jest sprawdzana.

Aby ponownie sprawdzić uruchomienie albo zobaczyć problemy:

```bash
m2mr diagnose outputs/<run>                  # zapisz ponownie diagnostics.json
m2mr diagnose outputs/<run> --visualize      # także diagnostics.html: wideo źródłowe obok postaci, oś czasu, klikalna lista problemów
m2mr diagnose outputs/<run> --threshold-cm 2 # zgłaszaj tylko przenikania głębsze niż 2 cm (domyślnie 1)
```

Każdy problem w `diagnostics.json` to para części ciała z zakresami klatek, w których się przenikają, najgorszą klatką i jej głębokością. Numery klatek liczone są od 0, tak jak na osi czasu Blendera po imporcie glTF. Części połączone stawem (ramię i przedramię, tułów i udo, …) nie są porównywane: ich skóra nachodzi na siebie przy stawie w każdej pozie. `diagnostics.html` osadza wideo źródłowe (wymaga `ffmpeg`) i wczytuje three.js z CDN, więc widok 3D wymaga połączenia z internetem. Ten widok rysuje stałe znaczniki podłogi na y = 0: krzyż co 0,5 m, większy co metr i zielony krzyż w początku układu, żeby dało się ocenić, czy postać się rusza. Bursztynowy pas nad ścieżkami przenikania służy do uwag zauważonych na oko (przeciągnij zakres albo **In** / **Out**). Lista **Notes** po prawej je pokazuje; kliknięcie wiersza przenosi do niego. **Download notes** zapisuje te uwagi razem z listą przenikań. Plik nazywa się jak wideo źródłowe i zawiera jego ścieżkę.

### 7. Palce (`--detect-hands`)

Zwykłe `m2mr run` rusza ciałem i zostawia kości palców Mixamo w spoczynku. `--detect-hands` włącza model dłoni, który jedzie z ekstraktorem ciała. Przy domyślnym ekstraktorze, GVHMR, tym modelem jest [HaMeR](https://github.com/geopavlakos/hamer). HaMeR wycina nadgarstki z osoby i klatek, które GVHMR już wybrał. Nie szuka drugiej osoby w klipie.

**Czas rośnie mniej więcej dwukrotnie.** Klip, który bez flagi kończy się w kilka minut, z `--detect-hands` trwa około dwa razy dłużej, bo przejście dłoni idzie na wierzch ekstrakcji ciała. Przy długim wideo uwzględnij ten czas, zanim zaczniesz.

Umieść `MANO_RIGHT.pkl` jak w tabeli powyżej, a potem:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

Pierwsze uruchomienie z `--detect-hands` pobiera wagi HaMeR do `weights/hamer/` (~2,7 GB, raz). Obroty palców trafiają do `skeleton_motion.npz` i napędzają 30 kości palców Mixamo na postaci ze skinningiem. Nadgarstek, którego przejście ciała nie widziało wyraźnie, zostaje w spoczynku dla tej dłoni.

`--hand-smooth` mówi, ile sekund wygładzania nałożyć na te obroty. Domyślnie `0.08`. `0` zostawia surową estymację. Wygładzanie działa, gdy plik szkieletu już zawiera ruch dłoni, także przy późniejszym uruchomieniu, które tylko używa tego pliku ponownie.

Ponowne użycie wcześniejszego szkieletu:

- Plik już zawiera ruch dłoni: `--skeleton` sam napędza palce. `--detect-hands` nie jest już potrzebne.
- Nie zawiera, ale cache ciała tego przebiegu wciąż leży obok (`cache/<clip>/0_input_video.mp4` oraz `preprocess/vitpose.pt` i `preprocess/bbx.pt`): `--skeleton ... --detect-hands` dokłada palce bez ponownej ekstrakcji ciała.
- Tego cache już nie ma: uruchom wideo albo zdjęcie jeszcze raz z `--detect-hands`.

## Wyniki

Każde `m2mr run` tworzy katalog nazwany według **czasu uruchomienia polecenia**. Pliki w katalogu głównym są takie same dla wideo i zdjęcia; zmienia się tylko folder z podglądem.

```
outputs/20260829_193205_dance/          # lub …_pose/ dla zdjęcia
├── run.json                            # czas startu, dane wejściowe, pełne polecenie
├── skeleton_motion.npz                 # szkielet 3D człowieka (do ponownego użycia z --skeleton)
├── mixamo_rotations.npz                # rotacje Mixamo dla każdej kości
├── mixamo_character.glb                # postać ze skinningiem, do importu w Blenderze / Unity
├── diagnostics.json                    # raport samoprzenikania (zob. Szybki start, krok 6)
├── diagnostics.html                    # tylko po `m2mr diagnose <run> --visualize`
└── videos/   lub   images/             # podglądy — zależnie od wejścia
```

**Wejście wideo** zapisuje `videos/` (te same proporcje obrazu co klip):

```
videos/
├── human_skeleton.mp4                  # odtworzony szkielet 3D człowieka
├── mixamo_skeleton.mp4                 # szkielet riga Mixamo
├── mixamo_character.mp4                # postać Mixamo ze skinningiem
└── compare.mp4                         # 2×2: oryginał (lewy górny) / szkielet Mixamo (prawy górny)
                                        #      szkielet człowieka (lewy dolny) / postać (prawy dolny)
```

**Wejście ze zdjęcia** zapisuje zamiast tego `images/` (te same cztery widoki plus pełny obrót):

```
images/
├── human_skeleton.png                  # odtworzony szkielet 3D człowieka
├── mixamo_skeleton.png                 # szkielet riga Mixamo
├── mixamo_character.png                # postać Mixamo ze skinningiem
├── compare.png                         # 2×2: oryginał (lewy górny) / szkielet Mixamo (prawy górny)
│                                       #      szkielet człowieka (lewy dolny) / postać (prawy dolny)
└── before_after_360_compare.mp4        # lewo: oryginalne zdjęcie
                                        # prawo: obrót wokół riga co 10° (pełny obrót)
```

Z `--detect-hands` plik `skeleton_motion.npz` przechowuje też obroty palców, a `mixamo_rotations.npz` i `mixamo_character.glb` zawierają 30 kości palców. Bez tej flagi i bez ruchu dłoni już zapisanego w ponownie używanym szkielecie te kości zostają w spoczynku.

Otwórz `mixamo_character.glb` w Blenderze: File → Import → glTF 2.0 (.glb/.gltf). Jeśli kamera patrzy w pustą przestrzeń, zaznacz mesh postaci i użyj View → Frame Selected. Skupisko kul na głowie i dłoniach to wyświetlanie kości, a nie mesh: w Outlinerze ukryj **Icosphere** i **armature**; pozostaw widoczny mesh ze skinningiem. Ustaw FPS sceny zgodnie z `run.json` (`fps`), a oś czasu na klatki od 0 do `n_frames` − 1, aby odtwarzanie odpowiadało źródłu, a numery klatek — plikowi `diagnostics.json`. Porównaj uruchomienie z wideo z `videos/mixamo_character.mp4`, a uruchomienie ze zdjęcia z `images/mixamo_character.png` lub klipem z obrotem.

## Licencja

Kod tego repozytorium jest objęty licencją Apache-2.0. Zasoby, które pobierasz samodzielnie, mają własne warunki i nie mogą być rozpowszechniane razem z tym repozytorium:

- **SMPL-X**: dostęp kontrolowany przez MPI; domyślnie niekomercyjne badania / edukacja / sztuka; użycie komercyjne wymaga osobnej umowy
- **MANO** (tylko przy `--detect-hands`): dostęp kontrolowany przez MPI, ten sam rodzaj pobrania co SMPL-X; trzymaj `MANO_RIGHT.pkl` lokalnie i nie rozpowszechniaj go
- **Mixamo FBX**: można używać w wydanym produkcie; nie rozpowszechniaj surowego FBX jako paczki zasobów
- **GVHMR i inne wagi modeli**: pobierane automatycznie do `weights/` przy pierwszym `m2mr run`, na licencjach poszczególnych projektów źródłowych
- **HaMeR**: kod inferencji w tym repozytorium jest na licencji MIT; wagi trafiają do `weights/hamer/` przy pierwszym `m2mr run --detect-hands`, na warunkach publikacji projektu źródłowego

## Kontakt

Jeśli napotkasz problem, potrzebujesz pomocy w lokalnej instalacji albo chcesz porozmawiać o współpracy, napisz na adres:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
