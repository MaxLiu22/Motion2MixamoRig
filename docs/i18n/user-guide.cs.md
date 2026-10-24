# Motion2MixamoRig pro Blender — Uživatelská příručka

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · Čeština · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Proměňte video jednoho člověka v animovanou postavu Mixamo, přímo v Blenderu.
Programování ani terminál nepotřebujete.

<!-- video: link the tutorial video here -->

> Zatím vyzkoušeno jen na **macOS (Apple Silicon)**. Verze pro Windows brzy přijde.

## Co budete potřebovat

- **Blender 4.2 nebo novější**
- **Připojení k internetu** pro první nastavení
- **Asi 8 GB volného místa na disku** (prostředí ~1,3 GB + modely ~5,6 GB)
- **Účet SMPL-X zdarma** a **účet Adobe zdarma** (pro Mixamo); viz kroky 4 a 5

## 1. Stáhněte doplněk

Jděte na [nejnovější vydání](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
a stáhněte zip pro svůj počítač:

| Váš počítač | Soubor |
| --- | --- |
| Mac s Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Již brzy** |

Třeba `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` je verze doplňku,
`macos-arm64` platforma. Když vyberete špatný, Blender instalaci odmítne
a napíše, jakou platformu čekal.

**Nerozbalujte** ho. Blender zip nainstaluje sám.

## 2. Nainstalujte ho do Blenderu

1. **Edit → Preferences → Get Extensions**
2. Klikněte na malé **∨** vpravo nahoře → **Install from Disk…**
3. Vyberte zip. **Motion2MixamoRig** se objeví v seznamu, už zapnutý.
4. Zavřete Preferences. V 3D Viewportu stiskněte **N** a klikněte na kartu
   **Motion2MixamoRig** vpravo.

<!-- screenshot: Install from Disk menu -->

## 3. Nainstalujte prostředí (jednou)

Na panelu klikněte na **Nainstalovat prostředí (jedním kliknutím)** (Install Runtime (one click)).

Doplněk stáhne vlastní Python a knihovny (~1,4 GB) do
`~/Motion2MixamoRig/`. Ničeho jiného na počítači se nedotkne. Trvá to několik
minut; ukazatel průběhu ukazuje aktuální krok.

<!-- screenshot: Install Runtime button and progress -->

## 4. Získejte model těla SMPL-X

SMPL-X je bezplatný model těla, který doplněk potřebuje. Licence nám nedovoluje
ho šířit, takže si ho stáhnete sami, jednou:

1. Otevřete [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) a klikněte na
   **Register**. Přijměte licenci a potvrďte e-mail.
2. Přihlaste se, otevřete **Download** a stáhněte model SMPL-X (verzi **NPZ**).
3. Rozbalte ho a najděte **`SMPLX_NEUTRAL.npz`**.
4. V Blenderu klikněte na **Vybrat model SMPL-X…** (Choose SMPL-X Model…)
   a vyberte ten soubor. Panel pak ukáže **Model SMPL-X: nalezen**
   (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Získejte postavu Mixamo

1. Otevřete [mixamo.com](https://www.mixamo.com/) a přihlaste se účtem Adobe.
2. Karta **Characters** → vyberte postavu (třeba **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Vygenerujte pohyb

V poli **Input**:

1. **Typ zdroje** (Source Type): Video (nebo Image pro jednu pózu)
2. **Zdrojový soubor** (Source File): váš klip. Musí ukazovat **přesně jednu
   osobu, od hlavy k patě v záběru po celou dobu**.
3. **FBX rigu Mixamo** (Mixamo Rig FBX): postava z kroku 5
4. **Detekovat ruce** (Detect Hands) je vypnuté. Zapněte to, jen když se mají
   hýbat prsty. Pak klikněte na **Vybrat model ruky MANO…** (Choose MANO Hand
   Model…) a vyberte `MANO_RIGHT.pkl`. Ten soubor získáte stejně jako SMPL-X:
   zaregistrujte se na [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/),
   stáhněte **Models & Code** a rozbalte. První průchod rukou stáhne asi
   **2,7 GB** navíc, jednou, a trvá asi dvakrát déle než průchod jen těla.
   Když jsou ruce zapnuté, objeví se **Vyhlazení prstů (sekundy)** (Finger
   Smoothing (seconds)). Změkčí pohyb prstů. Výchozí hodnota je 0,08 sekundy;
   0 nechá to, co se detekovalo.
5. Klikněte na **Vygenerovat pohyb** (Generate Motion)

Až to skončí, animovaná postava se do scény naimportuje sama. Došlápnutá noha
zůstane tam, kam dopadla, a chodidlo se položí na podlahu Blenderu. Na tu
podlahu se přidá síť **Značky na podlaze** (Floor Markers) (kříž každých
0,5 m). Zaškrtávací pole **Značky na podlaze** (Floor Markers) pod Průběh /
Výsledek ji ukáže nebo skryje.

### První spuštění trvá déle — to je normální

Poprvé doplněk stáhne asi **5,6 GB** modelů. Panel ukazuje velikost stahování,
rychlost a zbývající čas. Modely se stáhnou jen jednou.

Potom se video zpracuje na vašem počítači. Na CPU Macu trvá 10sekundový klip
několik minut. Blender zůstane použitelný, než to doběhne, a **Zrušit**
(Cancel) úlohu zastaví.

## Tipy pro dobrý výsledek

- Jen jedna osoba, viditelné celé tělo, neoříznuté na okrajích
- Klidná kamera, dobré světlo, jednoduché oblečení místo volného nebo vlajícího
- Krátké klipy (5–20 sekund) se na první zkoušku zpracují rychleji

## Aktualizace na novou verzi

Doplněk se aktualizuje často. Postup:

1. Stáhněte nejnovější zip z
   [nejnovějšího vydání](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → odeberte starý **Motion2MixamoRig**, Blender úplně
   ukončete (**Cmd+Q**), otevřete znovu a nainstalujte nový zip.
3. Na panelu klikněte na **Aktualizovat prostředí** (Update Runtime).

Aktualizace si nechá stažené modely, takže je rychlá. Nainstalovaná verze je
vedle doplňku v **Get Extensions**.

## Panel

- **⚙ vedle nadpisu** ukáže nebo skryje pole **Nastavení** (Setup).
- **Nastavení**: jazyk, prostředí, SMPL-X, zařízení (CPU je bezpečná volba)
  a **Zkontrolovat prostředí** (Check Environment).
- **Input**: co animovat, **Model těla** (Body Model, GVHMR) a
  **Detekovat ruce** (Detect Hands).
- **Průběh / Výsledek** (Progress / Result): průběh, nedávný protokol a po
  úloze **Importovat vygenerovanou postavu** (Import Generated Character),
  zaškrtávací pole **Značky na podlaze** (Floor Markers), **Otevřít výstupní
  složku** (Open Output Folder), **Zobrazit celý protokol** (View Full Log).
- **Diagnostika** (Diagnostics): kde části těla postavy vnikají do sebe (ruka
  uvnitř hlavy, zkřížené paže). Červené buňky na liště jsou snímky s
  problémem; kliknutím na jednu tam přejdete. Trojúhelník pod lištou sleduje
  aktuální snímek a pod ním jsou části, které se protínají, a hloubka.
  **Předchozí** / **Další** (Previous / Next) přeskakují mezi problémy.
  **Otevřít HTML report** (Open HTML Report) otevře v prohlížeči report se
  zdrojovým videem vedle postavy (poprvé sestavení trvá asi 15 sekund). To
  video potřebuje na počítači ffmpeg (na Macu `brew install ffmpeg`); bez něj
  zůstane panel prázdný. Postava stojí na pevných křížích podlahy, jeden
  každých 0,5 m, abyste viděli, jestli klouže. Jantarový pruh nad červenými
  stopami je na poznámky od oka. Jsou vypsané vpravo pod **Notes**; kliknutím
  na jednu na ni skočíte. **Download notes** uloží tyto poznámky spolu s časy
  průniků. Soubor se jmenuje podle zdrojového videa.

Panel doplňku je v 19 jazycích. **Automaticky** (Auto) sleduje jazyk Blenderu,
když je ten jazyk jedním z nich; jinak panel zůstane anglicky. Změňte to v poli
Nastavení pod **Jazyk rozhraní** (UI Language). Tahle příručka je česky; tahle
volba na panelu ještě není a anglické názvy v závorkách jsou text tlačítek.

## Když se něco pokazí

| Co vidíte | Co udělat |
| --- | --- |
| Instalace prostředí selhala (Runtime installation failed) | Zkontrolujte internet a klikněte na tlačítko znovu. Protokol: `~/Motion2MixamoRig/logs/setup.log` |
| Model SMPL-X: chybí (SMPL-X model: missing) | Zopakujte krok 4 a vyberte `SMPLX_NEUTRAL.npz` |
| Model ruky MANO: chybí (MANO hand model: missing) | Zapněte **Detekovat ruce**, pak **Vybrat model ruky MANO…** a vyberte `MANO_RIGHT.pkl` |
| FBX Mixamo je neplatný (Mixamo FBX invalid) | Stáhněte postavu znovu jako **FBX Binary**, **T-pose** |
| Vstup obsahuje víc osob (Input contains multiple people) | Použijte klip jen s jednou osobou |
| Nebyla detekována žádná osoba (No person was detected) | Ujistěte se, že je vidět celé tělo a že je dobře osvětlené |
| Proces pipeline neočekávaně skončil (Pipeline process exited unexpectedly) | Klikněte na **Zobrazit celý protokol** (View Full Log) |

Když žádáte o pomoc, přiložte protokol a napište, kterou verzi doplňku používáte.

## Odinstalace

1. **Get Extensions** → odeberte **Motion2MixamoRig**.
2. Smažte složku **`~/Motion2MixamoRig`** (vaše domovská složka →
   `Motion2MixamoRig`). Odebrání doplňku ji **nesmaže** a drží asi 7 GB
   prostředí a modelů plus vygenerované výsledky v `app/outputs/`.

## Licence

Motion2MixamoRig je **jen pro nekomerční použití**: spoléhá na výzkumné modely
(třeba GVHMR a SMPL-X), jejichž licence komerční použití nedovolují.
Viz [`NOTICE.md`](../../NOTICE.md).
