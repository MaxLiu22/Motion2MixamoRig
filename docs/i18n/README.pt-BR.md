# Motion2MixamoRig

<p align="center">
  <a href="#pré-requisitos"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.pt-BR.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · Português (Brasil) · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Transfira o movimento de uma pessoa em um vídeo — ou a pose em uma foto — para um personagem 3D com rig da Adobe Mixamo.

Para quem desenvolve jogos: passe um vídeo de ação com **uma só pessoa** (ou uma foto) e um personagem Mixamo; o programa gera vídeos de prévia e um arquivo de personagem com skinning (`.glb`) para arrastar no Blender ou no Unity.

> O Motion2MixamoRig ainda é experimental. A versão 0.1.8 é o pipeline de linha de comando. Este repositório também inclui uma extensão para o Blender 4.2+ que executa o mesmo pipeline em um ambiente Python externo. Compilar o complemento a partir do código: [`blender_extension/README.md`](../../blender_extension/README.md).

## Duas formas de usar

### 🎨 No Blender — sem programar

1. Baixe o zip da sua plataforma, por exemplo `motion2mixamorig-<version>-macos-arm64.zip`, na [última release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. No Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, escolha o zip.
3. 3D Viewport → pressione **N** → aba **Motion2MixamoRig** → **Instalar o ambiente (um clique)** (Install Runtime (one click)).
4. **Escolher o modelo SMPL-X…** (Choose SMPL-X Model…) (download gratuito) e escolha um FBX de personagem Mixamo.
5. Escolha um vídeo com uma só pessoa → **Gerar movimento** (Generate Motion).

Instruções passo a passo, dicas e atualização: **[Guia do usuário](user-guide.pt-BR.md)**. Testado no macOS (Apple Silicon).

### 💻 Linha de comando — para quem desenvolve

Clone o repositório e execute o pipeline você mesmo: comece em [Pré-requisitos](#pré-requisitos).

Agentes devem começar por [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Abra <a href="../assets/demo.mp4">demo.mp4</a> neste repositório.</sub>
</p>

Outra demonstração:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Relatório de diagnóstico (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Pré-requisitos

Python 3.11+. Depois do clone, crie um virtualenv e instale as dependências; o comando `m2mr` fica disponível:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Instala as dependências e este projeto. O chumpy (um pacote antigo na
# cadeia de dependências) importa o pip no script de setup, o que falha com
# "No module named 'pip'" no build isolado padrão do pip. Instale-o
# antes, com o isolamento desligado, e depois instale este projeto.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Os pesos de inferência não são baixados aqui. O primeiro `m2mr run` baixa os pesos do GVHMR em `weights/` (~5 GB, uma vez só). O primeiro `m2mr run --detect-hands` também baixa os pesos da mão HaMeR em `weights/hamer/` (~2,7 GB, uma vez só).

O ffmpeg é recomendado (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
O pipeline funciona sem ele, mas os vídeos de saída ficam **sem áudio** e não tocam no navegador.

## Antes de executar: coloque estes arquivos em `assets/`

Este repositório não inclui estes arquivos; você precisa obtê-los. O nome do arquivo SMPL-X tem de coincidir exatamente com a tabela; os nomes de FBX, vídeo e imagem podem ser quaisquer. Uma execução precisa de SMPL-X, um personagem Mixamo e **um vídeo ou** uma foto. Personagens Mixamo reexportados do Cinema 4D também funcionam; veja [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| O que | Onde | Onde conseguir |
|---|---|---|
| Modelo de corpo SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Cadastre-se em [SMPL-X](https://smpl-x.is.tue.mpg.de/) e baixe |
| FBX do personagem Mixamo | `assets/mixamo/Y_Bot.fbx` | Com uma conta Adobe, baixe o Y Bot (ou outro personagem com rig Mixamo) em [Mixamo](https://www.mixamo.com) |
| Vídeo de ação | `assets/video/<your_clip>.mp4` | Um clipe com **exatamente uma** pessoa bem visível, **da cabeça aos pés no quadro o tempo todo** (pode guardar vários arquivos; cada execução usa o adicionado por último) |
| Foto da pose (opcional) | `assets/image/<your_photo>.jpg` | Uma foto com **exatamente uma** pessoa bem visível, **da cabeça aos pés no quadro**. Use com `--image` |
| Mão direita MANO (só para `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Cadastre-se em [MANO](https://mano.is.tue.mpg.de/) e baixe **Models & Code**. Uma execução só do corpo não precisa deste arquivo |

Nota: o arquivo baixado do Mixamo se chama `Y Bot.fbx` (**espaço**), um caractere diferente de `Y_Bot.fbx` (**sublinhado**) na tabela.
Renomeie para o sublinhado e ele vira o rig padrão (`m2mr run` sem `--rig`). Deixar o espaço também serve: se `Y_Bot.fbx` não existir, usa-se o primeiro `.fbx` em `assets/mixamo/`.

`assets/video/` pode ter vários vídeos. Sem `--video` nem `--image`, a execução usa o arquivo **adicionado por último** em `assets/video/`; se a pasta estiver vazia, cai na foto mais recente em `assets/image/`.
Cada clipe ou foto deve mostrar uma só pessoa, **da cabeça aos pés no quadro**, sem nada cortado nas bordas. `m2mr doctor` / `m2mr run` param antes da extração se houver duas pessoas na imagem.

## Início rápido

Os resultados vão para `outputs/<run-time>_<source>/`. Execuções com vídeo escrevem `videos/`; as com foto escrevem `images/`.

### 1. Confira os assets e o ambiente

O que faltar é impresso com o lugar de onde baixar e onde colocar.

```bash
m2mr doctor
```

`m2mr doctor` confere a execução do corpo. Não exige o modelo de mão MANO. Para conferir também o arquivo extra e os pacotes Python usados pela detecção dos dedos:

```bash
m2mr doctor --detect-hands
```

### 2. Primeira execução: ver algo na tela

Sem opções, usa o **arquivo mais recente em `assets/video/`** e `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Este é o passo lento. A primeira execução baixa ~5 GB de pesos de inferência (uma vez só) e depois extrai o movimento humano do vídeo.
Na CPU, um clipe de ~30 segundos leva cerca de 8–15 minutos para extrair; execuções seguintes de duração parecida, com os pesos já presentes, levam cerca de 3–5 minutos.
O retarget e a renderização costumam levar um ou dois minutos. Reutilizar um esqueleto com `--skeleton` na seção seguinte pula a extração por completo e termina em algumas dezenas de segundos.

Um pé plantado é fixado por padrão: a ponta do pé quando a ponta está no chão, o calcanhar só quando os dedos estão levantados. Se uma perna esticada não alcança esse ponto, o quadril se move. Depois a sola é assentada no chão (y = 0). `--no-foot-lock` mantém o retarget bruto, então os pés podem deslizar; a sola ainda é assentada no chão.

### 3. O mesmo movimento, outro personagem

Baixe outro personagem do Mixamo para `assets/mixamo/`. **Não execute de novo mudando só `--rig`**: isso repete a extração lenta.
Passe `--skeleton` para reutilizar o esqueleto de uma execução anterior; minutos viram dezenas de segundos:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Outro vídeo

`--video` escolhe o clipe. Combina livremente com `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Uma foto (pose estática)

`--image` reconstrói uma **pose 3D estática** a partir da foto de uma pessoa e a transfere para o personagem Mixamo como numa execução com vídeo. As prévias são quatro imagens em `images/` (as mesmas vistas da execução com vídeo), mais um clipe de órbita esquerda/direita `before_after_360_compare.mp4`. Não passe `--video` ao mesmo tempo.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` sem caminho usa o arquivo adicionado por último em `assets/image/`.

### 6. Procure autointerseções

Cada execução também confere o personagem pronto em busca de **autointerseção** — uma parte do corpo entrando em outra, como uma mão dentro da cabeça — e escreve `diagnostics.json`. O terminal imprime uma linha, por exemplo `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. O chão não é conferido.

Para conferir de novo uma execução, ou para ver os problemas:

```bash
m2mr diagnose outputs/<run>                  # reescreve diagnostics.json
m2mr diagnose outputs/<run> --visualize      # também diagnostics.html: vídeo de origem ao lado do personagem, linha do tempo, lista de problemas clicável
m2mr diagnose outputs/<run> --threshold-cm 2 # só reporta penetrações mais fundas que 2 cm (padrão 1)
```

Cada problema em `diagnostics.json` é um par de partes do corpo, com os intervalos de frames em que se cruzam, o pior frame e a profundidade. Os números de frame começam em 0, como a linha do tempo do Blender depois de importar um glTF. Partes unidas por uma articulação (braço e antebraço, tronco e coxa, …) não são comparadas: a pele se sobrepõe em volta da articulação em qualquer pose. `diagnostics.html` incorpora o vídeo de origem (precisa de `ffmpeg`) e carrega o three.js de uma CDN, então a vista 3D precisa de internet. Essa vista mantém marcas fixas no chão em y = 0 — uma cruz a cada 0,5 m, uma maior a cada metro e uma cruz verde na origem — para julgar se o personagem está se movendo. A faixa âmbar acima das trilhas de interseção é para notas feitas a olho (arraste um intervalo, ou In / Out). A lista **Notes** à direita as mostra; um clique numa linha salta até ela. **Download notes** salva essas notas junto com a lista de interseções. O arquivo recebe o nome do vídeo de origem e registra o caminho desse vídeo.

### 7. Dedos (`--detect-hands`)

Um `m2mr run` simples move o corpo e deixa os ossos dos dedos Mixamo em repouso. `--detect-hands` liga o modelo de mão que acompanha o extrator do corpo. Com o extrator padrão, GVHMR, esse modelo é o [HaMeR](https://github.com/geopavlakos/hamer). O HaMeR recorta os pulsos da pessoa e dos frames que o GVHMR já escolheu. Ele não procura uma segunda pessoa no clipe.

**O tempo aproximadamente dobra.** Um clipe que sem a opção termina em alguns minutos leva cerca do dobro com `--detect-hands`, porque a passagem das mãos se soma à extração do corpo. Num vídeo longo, conte esse tempo extra antes de começar.

Coloque `MANO_RIGHT.pkl` como na tabela acima e depois:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

A primeira execução com `--detect-hands` baixa os pesos do HaMeR em `weights/hamer/` (~2,7 GB, uma vez). As rotações dos dedos são gravadas em `skeleton_motion.npz` e movem os 30 ossos dos dedos Mixamo no personagem com skin. Um pulso que a passagem do corpo não viu com clareza fica em repouso naquela mão.

`--hand-smooth` é quantos segundos de suavização aplicar a essas rotações. O padrão é `0.08`. `0` mantém a estimativa bruta. A suavização roda sempre que o arquivo do esqueleto já contém movimento das mãos, inclusive numa execução posterior que só reutiliza esse arquivo.

Ao reutilizar um esqueleto anterior:

- O arquivo já contém movimento das mãos: `--skeleton` move os dedos sozinho. `--detect-hands` não é necessário de novo.
- Não contém, mas o cache do corpo daquela execução ainda está ao lado (`cache/<clip>/0_input_video.mp4`, mais `preprocess/vitpose.pt` e `preprocess/bbx.pt`): `--skeleton ... --detect-hands` acrescenta os dedos sem extrair o corpo de novo.
- Esse cache sumiu: execute o vídeo ou a foto de novo com `--detect-hands`.

## Saídas

Cada `m2mr run` cria uma pasta com o nome da **hora em que o comando começou**. Os arquivos na raiz são os mesmos para vídeo e foto; só muda a pasta das prévias.

```
outputs/20260829_193205_dance/          # ou …_pose/ para uma foto
├── run.json                            # hora de início, entradas, comando completo
├── skeleton_motion.npz                 # esqueleto humano 3D (reutilize com --skeleton)
├── mixamo_rotations.npz                # rotações Mixamo por osso
├── mixamo_character.glb                # personagem com skin, importe no Blender / Unity
├── diagnostics.json                    # relatório de autointerseção (veja o passo 6 do Início rápido)
├── diagnostics.html                    # só depois de `m2mr diagnose <run> --visualize`
└── videos/   ou   images/              # prévias — depende da entrada
```

**Entrada de vídeo** escreve `videos/` (a mesma proporção do clipe):

```
videos/
├── human_skeleton.mp4                  # esqueleto humano 3D reconstruído
├── mixamo_skeleton.mp4                 # esqueleto do rig Mixamo
├── mixamo_character.mp4                # personagem Mixamo com skin
└── compare.mp4                         # 2×2: original (sup. esq.) / esqueleto Mixamo (sup. dir.)
                                        #      esqueleto humano (inf. esq.) / personagem (inf. dir.)
```

**Entrada de foto** escreve `images/` (as mesmas quatro vistas, mais um giro):

```
images/
├── human_skeleton.png                  # esqueleto humano 3D reconstruído
├── mixamo_skeleton.png                 # esqueleto do rig Mixamo
├── mixamo_character.png                # personagem Mixamo com skin
├── compare.png                         # 2×2: original (sup. esq.) / esqueleto Mixamo (sup. dir.)
│                                       #      esqueleto humano (inf. esq.) / personagem (inf. dir.)
└── before_after_360_compare.mp4        # esquerda: foto original
                                        # direita: órbita do rig a 10° (uma volta completa)
```

Com `--detect-hands`, `skeleton_motion.npz` também guarda as rotações dos dedos, e `mixamo_rotations.npz` / `mixamo_character.glb` incluem os 30 ossos dos dedos. Sem essa opção, e sem movimento das mãos já gravado num esqueleto reutilizado, esses ossos ficam em repouso.

Abra `mixamo_character.glb` no Blender: File → Import → glTF 2.0 (.glb/.gltf). Se a câmera enquadrar um espaço vazio, selecione a malha do personagem e use View → Frame Selected. O grupo de esferas na cabeça e nas mãos é a exibição dos ossos, não a malha: no Outliner, oculte **Icosphere** e o **armature**; deixe a malha com skin visível. Defina o FPS da cena a partir de `run.json` (`fps`) e a linha do tempo nos frames de 0 a `n_frames` − 1, para a reprodução coincidir com a fonte e os números de frame coincidirem com `diagnostics.json`. Compare uma execução de vídeo com `videos/mixamo_character.mp4`, e uma de foto com `images/mixamo_character.png` ou com o clipe de órbita.

## Licença

O código deste repositório é Apache-2.0. Os assets que você baixa têm termos próprios e não devem ser redistribuídos com este repositório:

- **SMPL-X**: acesso controlado pelo MPI; por padrão, só pesquisa / ensino / arte não comerciais; uso comercial exige um acordo à parte
- **MANO** (só se usar `--detect-hands`): acesso controlado pelo MPI, o mesmo tipo de download do SMPL-X; coloque `MANO_RIGHT.pkl` localmente e não o redistribua
- **FBX do Mixamo**: pode ir num produto distribuído; não redistribua o FBX original como pacote de assets
- **Pesos do GVHMR**: baixados automaticamente em `weights/` no primeiro `m2mr run`, sob a licença de origem
- **HaMeR**: o código de inferência neste repositório é MIT; os pesos são baixados em `weights/hamer/` no primeiro `m2mr run --detect-hands`, sob a licença de origem

## Contato

Se encontrar um problema, precisar de ajuda para terminar uma instalação local ou quiser falar de uma colaboração, escreva para:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
