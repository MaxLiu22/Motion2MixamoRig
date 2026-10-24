# Motion2MixamoRig per Blender — Guida utente

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · Italiano · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Trasforma il video di una persona in un personaggio Mixamo animato, direttamente in Blender.
Non servono programmazione né terminale.

<!-- video: link the tutorial video here -->

> Finora testato solo su **macOS (Apple Silicon)**. Una build per Windows è in arrivo.

## Cosa ti serve

- **Blender 4.2 o successivo**
- **Una connessione a internet** per la prima configurazione
- **Circa 8 GB di spazio libero su disco** (ambiente ~1,3 GB + modelli ~5,6 GB)
- **Un account SMPL-X gratuito** e **un account Adobe gratuito** (per Mixamo); vedi i passi 4 e 5

## 1. Scarica il componente aggiuntivo

Vai all’[ultima release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
e scarica lo zip adatto al tuo computer:

| Il tuo computer | File |
| --- | --- |
| Mac con Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **In arrivo** |

Per esempio `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` è la versione del
componente aggiuntivo, `macos-arm64` la piattaforma. Se scegli quello sbagliato,
Blender si rifiuta di installarlo e indica la piattaforma che si aspettava.

**Non** decomprimerlo. Blender installa lo zip da solo.

## 2. Installalo in Blender

1. **Edit → Preferences → Get Extensions**
2. Fai clic sulla piccola **∨** in alto a destra → **Install from Disk…**
3. Scegli lo zip. **Motion2MixamoRig** compare nell’elenco, già attivo.
4. Chiudi Preferences. Nel 3D Viewport premi **N**, poi fai clic sulla scheda
   **Motion2MixamoRig** a destra.

<!-- screenshot: Install from Disk menu -->

## 3. Installa l’ambiente (una sola volta)

Nel pannello, fai clic su **Installa l’ambiente (un clic)** (Install Runtime (one click)).

Il componente aggiuntivo scarica un proprio Python e le librerie (~1,4 GB) in
`~/Motion2MixamoRig/`. Non tocca nient’altro sul tuo computer. Ci vogliono
alcuni minuti; la barra di avanzamento mostra il passaggio in corso.

<!-- screenshot: Install Runtime button and progress -->

## 4. Ottieni il modello del corpo SMPL-X

SMPL-X è un modello del corpo gratuito di cui il componente aggiuntivo ha
bisogno. La sua licenza non ci permette di distribuirlo, quindi lo scarichi tu,
una sola volta:

1. Apri [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) e fai clic su
   **Register**. Accetta la licenza e conferma l’email.
2. Accedi, apri **Download** e scarica il modello SMPL-X (la versione **NPZ**).
3. Decomprimilo e trova **`SMPLX_NEUTRAL.npz`**.
4. In Blender, fai clic su **Scegli il modello SMPL-X…** (Choose SMPL-X Model…)
   e seleziona quel file. Il pannello mostra **Modello SMPL-X: trovato**
   (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Ottieni un personaggio Mixamo

1. Apri [mixamo.com](https://www.mixamo.com/) e accedi con un account Adobe.
2. Scheda **Characters** → scegli un personaggio (per esempio **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Genera il movimento

Nel riquadro **Input**:

1. **Tipo di sorgente** (Source Type): Video (o Immagine per una sola posa)
2. **File sorgente** (Source File): la tua clip. Deve mostrare **una sola
   persona, dalla testa ai piedi nell’inquadratura per tutto il tempo**.
3. **FBX del rig Mixamo** (Mixamo Rig FBX): il personaggio del passo 5
4. **Rileva le mani** (Detect Hands) è spento. Attivalo solo se le dita devono
   muoversi. Poi fai clic su **Scegli il modello della mano MANO…** (Choose MANO
   Hand Model…) e scegli `MANO_RIGHT.pkl`. Quel file si ottiene come SMPL-X:
   registrati su [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/), scarica
   **Models & Code** e decomprimilo. Il primo passaggio delle mani scarica circa
   **2,7 GB** in più, una sola volta, e dura circa il doppio di un passaggio del solo corpo. Quando è attivo compare **Finger Smoothing (seconds)**. Ammorbidisce il movimento delle dita. Il valore predefinito è 0,08 secondi; 0 lascia ciò che è stato rilevato.
5. Fai clic su **Genera movimento** (Generate Motion)

Al termine, il personaggio animato viene importato automaticamente nella scena. Un piede appoggiato resta dove è atterrato, e la pianta è posata sul pavimento di Blender. Su quel pavimento viene aggiunto un mesh **Segni sul pavimento** (Floor Markers) (una croce ogni 0,5 m). La casella **Segni sul pavimento** (Floor Markers) sotto Avanzamento / Risultato lo mostra o lo nasconde.

### La prima esecuzione richiede più tempo — è normale

La prima volta, il componente aggiuntivo scarica circa **5,6 GB** di modelli. Il
pannello mostra la dimensione del download, la velocità e il tempo rimanente. I
modelli si scaricano una sola volta.

Dopo, il video viene elaborato sul tuo computer. Sulla CPU di un Mac, una clip
di 10 secondi richiede qualche minuto. Nel frattempo Blender resta utilizzabile,
e **Annulla** (Cancel) interrompe l’attività.

## Consigli per buoni risultati

- Una sola persona, corpo intero visibile, non tagliato ai bordi
- Camera ferma, buona luce, abiti semplici invece che larghi o svolazzanti
- Le clip brevi (5–20 secondi) sono più veloci da provare all’inizio

## Aggiornare a una nuova versione

Il componente aggiuntivo viene aggiornato spesso. Per aggiornarlo:

1. Scarica lo zip più recente dall’
   [ultima release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → rimuovi il vecchio **Motion2MixamoRig**, chiudi del tutto
   Blender (**Cmd+Q**), riaprilo e installa il nuovo zip.
3. Nel pannello, fai clic su **Aggiorna l’ambiente** (Update Runtime).

L’aggiornamento conserva i modelli già scaricati, quindi è rapido. La versione
installata è indicata accanto al componente aggiuntivo in **Get Extensions**.

## Il pannello

- **⚙ accanto al titolo** mostra o nasconde il riquadro **Configurazione** (Setup).
- **Configurazione**: lingua, ambiente, SMPL-X, **dispositivo** (Device; la CPU è
  la scelta sicura) e **Verifica ambiente** (Check Environment).
- **Input**: cosa animare, il **Modello del corpo** (Body Model, GVHMR) e **Rileva le mani** (Detect Hands).
- **Avanzamento / Risultato** (Progress / Result): avanzamento, log recente e, al
  termine di un’attività, **Importa il personaggio generato** (Import Generated
  Character), **Segni sul pavimento** (Floor Markers), **Apri la cartella di output** (Open Output Folder), **Mostra il
  log completo** (View Full Log).
- **Diagnostica** (Diagnostics): i punti in cui le parti del corpo del
  personaggio entrano l’una nell’altra (una mano dentro la testa, braccia
  incrociate). Le celle rosse della barra sono frame con un problema; fai clic
  su una per andarci. Il triangolo sotto la barra segue il frame corrente, e
  sotto compaiono le parti che si intersecano e quanto in profondità.
  **Precedente** / **Successivo** (Previous / Next) passano da un problema
  all’altro. **Apri il report HTML** (Open HTML Report) apre nel browser un
  report con il video sorgente accanto al personaggio (la prima volta la
  creazione richiede circa 15 secondi). Il video originale richiede ffmpeg sul computer (su Mac: `brew install ffmpeg`). Senza, il personaggio c’è e il video accanto resta vuoto. Il personaggio sta su croci fisse del pavimento, una ogni 0,5 m, così si vede se sta scivolando. La corsia ambra sopra le tracce rosse serve per le note che fai a occhio. Sono elencate a destra in **Notes**; un clic su una riga ci salta. **Download notes** salva queste note insieme agli istanti di intersezione. Il file prende il nome del video sorgente.

Il componente aggiuntivo parla 19 lingue. **Automatica (Blender / Sistema)**
(Auto) segue la lingua di Blender; puoi cambiarla nel riquadro Configurazione in
**Lingua dell’interfaccia** (UI Language).

## Se qualcosa va storto

| Cosa vedi | Cosa fare |
| --- | --- |
| Installazione dell’ambiente non riuscita (Runtime installation failed) | Controlla la connessione a internet e fai di nuovo clic sul pulsante. Log: `~/Motion2MixamoRig/logs/setup.log` |
| Modello SMPL-X: mancante (SMPL-X model: missing) | Ripeti il passo 4 e scegli `SMPLX_NEUTRAL.npz` |
| Modello della mano MANO: mancante (MANO hand model: missing) | Attiva **Rileva le mani**, poi **Scegli il modello della mano MANO…** e scegli `MANO_RIGHT.pkl` |
| FBX Mixamo non valido (Mixamo FBX invalid) | Scarica di nuovo il personaggio come **FBX Binary**, **T-pose** |
| L’input contiene più persone (Input contains multiple people) | Usa una clip con una sola persona |
| Nessuna persona rilevata nell’input (No person was detected) | Assicurati che il corpo intero sia visibile e ben illuminato |
| Il processo della pipeline si è chiuso in modo imprevisto (Pipeline process exited unexpectedly) | Fai clic su **Mostra il log completo** (View Full Log) |

Quando chiedi aiuto, allega il log e indica quale versione del componente
aggiuntivo usi.

## Disinstallazione

1. **Get Extensions** → rimuovi **Motion2MixamoRig**.
2. Elimina la cartella **`~/Motion2MixamoRig`** (la tua cartella Inizio →
   `Motion2MixamoRig`). Rimuovere il componente aggiuntivo **non** la elimina, e
   contiene circa 7 GB tra ambiente e modelli, più i risultati generati in
   `app/outputs/`.

## Licenza

Motion2MixamoRig è **solo per uso non commerciale**: si basa su modelli di
ricerca (come GVHMR e SMPL-X) le cui licenze non consentono l’uso commerciale.
Vedi [`NOTICE.md`](../../NOTICE.md).
