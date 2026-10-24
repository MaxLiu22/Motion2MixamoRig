# Motion2MixamoRig para o Blender — Guia do usuário

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · Português (Brasil) · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Transforme o vídeo de uma pessoa num personagem Mixamo animado, dentro do Blender.
Não precisa de programação nem de terminal.

<!-- video: link the tutorial video here -->

> Até agora testado só no **macOS (Apple Silicon)**. A versão para Windows está a caminho.

## O que você precisa

- **Blender 4.2 ou mais novo**
- **Uma conexão com a internet** na primeira configuração
- **Cerca de 8 GB de espaço livre em disco** (ambiente ~1,3 GB + modelos ~5,6 GB)
- **Uma conta SMPL-X gratuita** e **uma conta Adobe gratuita** (para o Mixamo); veja os passos 4 e 5

## 1. Baixe a extensão

Vá à [última release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
e baixe o zip do seu computador:

| Seu computador | Arquivo |
| --- | --- |
| Mac com Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Em breve** |

Por exemplo `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` é a versão da
extensão, `macos-arm64` a plataforma. Se escolher o errado, o Blender recusa
a instalação e diz qual plataforma esperava.

**Não** descompacte. O Blender instala o zip sozinho.

## 2. Instale no Blender

1. **Edit → Preferences → Get Extensions**
2. Clique no **∨** pequeno no canto superior direito → **Install from Disk…**
3. Escolha o zip. **Motion2MixamoRig** aparece na lista, já ativado.
4. Feche Preferences. Na 3D Viewport pressione **N** e clique na aba
   **Motion2MixamoRig** à direita.

<!-- screenshot: Install from Disk menu -->

## 3. Instale o ambiente (uma vez)

No painel, clique em **Instalar o ambiente (um clique)** (Install Runtime (one click)).

A extensão baixa o próprio Python e as bibliotecas (~1,4 GB) em
`~/Motion2MixamoRig/`. Não mexe em mais nada no computador. Leva alguns
minutos; a barra de progresso mostra o passo atual.

<!-- screenshot: Install Runtime button and progress -->

## 4. Obtenha o modelo de corpo SMPL-X

SMPL-X é um modelo de corpo gratuito de que a extensão precisa. A licença não
permite que a gente o distribua, então você baixa, uma vez:

1. Abra [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) e clique em
   **Register**. Aceite a licença e confirme o e-mail.
2. Entre, abra **Download** e baixe o modelo SMPL-X (a versão **NPZ**).
3. Descompacte e ache **`SMPLX_NEUTRAL.npz`**.
4. No Blender, clique em **Escolher o modelo SMPL-X…** (Choose SMPL-X Model…)
   e selecione esse arquivo. O painel mostra **Modelo SMPL-X: encontrado**
   (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Obtenha um personagem Mixamo

1. Abra [mixamo.com](https://www.mixamo.com/) e entre com uma conta Adobe.
2. Aba **Characters** → escolha um personagem (por exemplo **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Gere o movimento

Na caixa **Input**:

1. **Tipo de origem** (Source Type): Video (ou Image para uma só pose)
2. **Arquivo de origem** (Source File): o seu clipe. Tem de mostrar **exatamente
   uma pessoa, da cabeça aos pés no quadro o tempo todo**.
3. **FBX do rig Mixamo** (Mixamo Rig FBX): o personagem do passo 5
4. **Detectar as mãos** (Detect Hands) está desligado. Ligue só quando quiser
   que os dedos se movam. Depois clique em **Escolher o modelo de mão MANO…**
   (Choose MANO Hand Model…) e escolha `MANO_RIGHT.pkl`. Esse arquivo se obtém
   como o SMPL-X: cadastre-se em [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/),
   baixe **Models & Code** e descompacte. A primeira passagem das mãos baixa
   cerca de **2,7 GB** a mais, uma vez, e leva cerca do dobro de uma passagem
   só do corpo. Com as mãos ligadas, aparece **Suavização dos dedos (segundos)**
   (Finger Smoothing (seconds)). Ela suaviza o movimento dos dedos. O padrão é
   0,08 segundo; 0 mantém o que foi detectado.
5. Clique em **Gerar movimento** (Generate Motion)

Quando termina, o personagem animado é importado na cena automaticamente. Um
pé plantado fica onde pousou, e a sola é assentada no chão do Blender. Uma
malha **Marcas no chão** (Floor Markers) é adicionada nesse chão (uma cruz a
cada 0,5 m). A caixa **Marcas no chão** (Floor Markers) em Progresso / Resultado
mostra ou oculta essa malha.

### A primeira execução demora mais — isso é normal

Na primeira vez, a extensão baixa cerca de **5,6 GB** de modelos. O painel
mostra o tamanho do download, a velocidade e o tempo restante. Os modelos são
baixados uma vez só.

Depois disso, o vídeo é processado no seu computador. Na CPU de um Mac, um
clipe de 10 segundos leva alguns minutos. O Blender continua usável enquanto
roda, e **Cancelar** (Cancel) interrompe o trabalho.

## Dicas para um bom resultado

- Uma só pessoa, corpo inteiro visível, sem corte nas bordas
- Câmera firme, boa luz, roupa simples em vez de larga ou esvoaçante
- Clipes curtos (5–20 segundos) são mais rápidos para o primeiro teste

## Atualizar para uma versão nova

A extensão é atualizada com frequência. Para atualizar:

1. Baixe o zip mais recente na
   [última release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → remova o **Motion2MixamoRig** antigo, feche o Blender
   por completo (**Cmd+Q**), abra de novo e instale o zip novo.
3. No painel, clique em **Atualizar o ambiente** (Update Runtime).

A atualização conserva os modelos já baixados, então é rápida. A versão
instalada aparece ao lado da extensão em **Get Extensions**.

## O painel

- **⚙ ao lado do título** mostra ou oculta a caixa **Configuração** (Setup).
- **Configuração**: idioma, ambiente, SMPL-X, dispositivo (CPU é a escolha
  segura) e **Verificar o ambiente** (Check Environment).
- **Input**: o que animar, **Modelo do corpo** (Body Model, GVHMR) e
  **Detectar as mãos** (Detect Hands).
- **Progresso / Resultado** (Progress / Result): progresso, log recente e,
  depois de um trabalho, **Importar o personagem gerado** (Import Generated
  Character), a caixa **Marcas no chão** (Floor Markers), **Abrir a pasta de
  saída** (Open Output Folder), **Ver o log completo** (View Full Log).
- **Diagnóstico** (Diagnostics): onde as partes do corpo do personagem entram
  uma na outra (uma mão dentro da cabeça, braços cruzados). As células
  vermelhas da barra são frames com problema; clique numa para ir até lá. O
  triângulo sob a barra segue o frame atual, e abaixo estão as partes que se
  cruzam e a profundidade. **Anterior** / **Próximo** (Previous / Next) saltam
  entre os problemas. **Abrir o relatório HTML** (Open HTML Report) abre no
  navegador um relatório com o vídeo de origem ao lado do personagem (a
  primeira vez leva cerca de 15 segundos para montar). Esse vídeo precisa do
  ffmpeg instalado no computador (num Mac, `brew install ffmpeg`); sem ele o
  quadro fica em branco. O personagem fica sobre cruzes fixas no chão, uma a
  cada 0,5 m, para ver se está deslizando. A faixa âmbar acima das trilhas
  vermelhas é para notas feitas a olho. Essas notas aparecem em **Notes** à
  direita; clique numa para saltar até ela. **Download notes** salva essas
  notas junto com os instantes de interseção. O arquivo recebe o nome do
  vídeo de origem.

O painel da extensão está em 19 idiomas. **Automático** (Auto) segue o idioma
do Blender quando esse idioma é um deles; nos outros casos o painel fica em
inglês. Mude na caixa Configuração, em **Idioma da interface** (UI Language).
Este guia está em português do Brasil; essa opção ainda não está no painel, e
os nomes em inglês entre parênteses são o texto dos botões.

## Se algo der errado

| O que você vê | O que fazer |
| --- | --- |
| A instalação do ambiente falhou (Runtime installation failed) | Confira a internet e clique no botão de novo. Log: `~/Motion2MixamoRig/logs/setup.log` |
| Modelo SMPL-X: ausente (SMPL-X model: missing) | Repita o passo 4 e escolha `SMPLX_NEUTRAL.npz` |
| Modelo de mão MANO: ausente (MANO hand model: missing) | Ligue **Detectar as mãos**, depois **Escolher o modelo de mão MANO…** e escolha `MANO_RIGHT.pkl` |
| FBX do Mixamo inválido (Mixamo FBX invalid) | Baixe o personagem de novo como **FBX Binary**, **T-pose** |
| A entrada contém várias pessoas (Input contains multiple people) | Use um clipe com uma só pessoa |
| Nenhuma pessoa foi detectada (No person was detected) | Confira se o corpo inteiro está visível e bem iluminado |
| O processo do pipeline encerrou de forma inesperada (Pipeline process exited unexpectedly) | Clique em **Ver o log completo** (View Full Log) |

Quando pedir ajuda, anexe o log e diga qual versão da extensão você usa.

## Desinstalar

1. **Get Extensions** → remova **Motion2MixamoRig**.
2. Apague a pasta **`~/Motion2MixamoRig`** (sua pasta de início →
   `Motion2MixamoRig`). Remover a extensão **não** apaga essa pasta, e ela
   guarda cerca de 7 GB de ambiente e modelos, mais os resultados gerados em
   `app/outputs/`.

## Licença

O Motion2MixamoRig é **somente para uso não comercial**: depende de modelos de
pesquisa (como GVHMR e SMPL-X) cujas licenças não permitem uso comercial.
Veja [`NOTICE.md`](../../NOTICE.md).
