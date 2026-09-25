from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets'/'editorial'
OUT.mkdir(parents=True,exist_ok=True)
BG='#0B0B0A'; FG='#F1EEE7'; MUTED='#9B9993'; LINE='#343432'; ACC='#F04A2A'
FONT="Arial, Helvetica, sans-serif"

def svg_start(title,h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{h}" viewBox="0 0 1200 {h}">',f'<title>{escape(title)}</title>',f'<rect width="1200" height="{h}" fill="{BG}"/>']

def text(x,y,s,size,fill=FG,weight=700,anchor='start',spacing=0,opacity=1):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{spacing}" opacity="{opacity}">{escape(s)}</text>'

def line(x1,y1,x2,y2,stroke=LINE,w=1,opacity=1):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{w}" opacity="{opacity}"/>'

def write(name,parts):
    parts.append('</svg>')
    (OUT/name).write_text('\n'.join(parts))

def cover():
    p=svg_start('Ahmad — editorial profile cover',430)
    p += [
      '<!-- modular-ahmad -->','<g transform="translate(72 88)">',
      f'<polygon points="0,250 34,250 92,0 58,0" fill="{FG}"/>',
      f'<polygon points="110,250 144,250 86,0 52,0" fill="{FG}"/>',
      f'<rect x="31" y="142" width="83" height="26" fill="{ACC}"/>',
      f'<rect x="176" y="0" width="34" height="250" fill="{FG}"/>',
      f'<rect x="292" y="0" width="34" height="250" fill="{FG}"/>',
      f'<rect x="210" y="110" width="82" height="28" fill="{FG}"/>',
      f'<rect x="360" y="0" width="34" height="250" fill="{FG}"/>',
      f'<rect x="506" y="0" width="34" height="250" fill="{FG}"/>',
      f'<polygon points="394,0 423,0 467,154 438,154" fill="{FG}"/>',
      f'<polygon points="477,0 506,0 462,154 433,154" fill="{FG}"/>',
      f'<polygon points="574,250 608,250 666,0 632,0" fill="{FG}"/>',
      f'<polygon points="684,250 718,250 660,0 626,0" fill="{FG}"/>',
      f'<rect x="605" y="142" width="83" height="26" fill="{FG}"/>',
      f'<rect x="752" y="0" width="34" height="250" fill="{FG}"/>',
      f'<path d="M786 17 H842 C927 17 966 58 966 125 C966 192 927 233 842 233 H786" fill="none" stroke="{FG}" stroke-width="34"/>',
      '</g>',line(72,365,1128,365),
      text(72,400,'MUHAMMAD AHMAD',18,FG,700,spacing=1.5),
      text(1128,400,'COMPUTER SCIENCE · FAST-NUCES',15,MUTED,600,'end',1.2),
    ]
    write('00-cover.svg',p)

def automotive():
    p=svg_start('3D AUTOMOTIVE EXPERIENCE — selected work',520)
    p += ['<!-- composition-diagonal -->',
         f'<polygon points="780,0 1200,0 1200,520 1020,520" fill="{FG}"/>',
         f'<polygon points="1030,0 1200,0 1200,140 1102,140" fill="{ACC}"/>',
         text(74,120,'3D',102,FG,800),text(74,218,'AUTOMOTIVE',88,FG,800),text(74,296,'EXPERIENCE',88,FG,800),
         text(78,367,'CINEMATIC REAL-TIME WEBGL · CAMERA · LIGHT · MATERIAL · MOTION',18,MUTED,600,spacing=.8),
         line(78,404,672,404),
         text(78,448,'NEXT.JS  ·  THREE.JS  ·  R3F  ·  WEBGL',20,FG,700,spacing=1),
         text(1050,430,'01',110,BG,800,'middle')]
    write('01-automotive.svg',p)

def orchestration():
    p=svg_start('Multimodel Orchestration — selected work',560)
    p += ['<!-- composition-route -->',
         text(72,118,'MULTIMODEL',82,FG,800),text(72,202,'ORCHESTRATION',82,FG,800),
         text(74,252,'AI CODING WORKERS · SHARED STATE · ROUTING · RECOVERY · VERIFICATION',17,MUTED,600,spacing=.7),
         line(74,294,1126,294),
         text(88,352,'REQUEST',18,MUTED,700,spacing=1.5),text(286,352,'PLAN JOB',18,FG,700,spacing=1.5),
         text(492,352,'ROUTE',18,FG,700,spacing=1.5),text(666,352,'EXECUTE',18,FG,700,spacing=1.5),
         text(884,352,'VERIFY',18,ACC,800,spacing=1.5),
         line(158,345,260,345,FG,2),line(372,345,470,345,FG,2),line(550,345,644,345,FG,2),line(760,345,860,345,FG,2),
         f'<rect x="72" y="402" width="468" height="88" fill="none" stroke="{LINE}"/>',
         text(92,438,'PYTHON 3.12+',16,MUTED,600),text(92,470,'LANGGRAPH · SQLITE · TYPER · PYDANTIC',18,FG,700),
         f'<rect x="568" y="402" width="558" height="88" fill="{FG}"/>',
         text(590,438,'LOCAL-FIRST / VENDOR-NEUTRAL',16,BG,700),
         text(590,470,'COORDINATION LAYER, NOT ANOTHER CHAT WRAPPER',18,BG,800)]
    write('02-orchestration.svg',p)

def digit():
    p=svg_start('AI Digit Recognizer — selected work',530)
    p += ['<!-- composition-crop -->',f'<rect x="0" y="0" width="438" height="530" fill="{FG}"/>',
         text(220,408,'7',430,BG,800,'middle'),f'<rect x="384" y="0" width="54" height="530" fill="{ACC}"/>',
         text(512,112,'AI DIGIT',86,FG,800),text(512,198,'RECOGNIZER',86,FG,800),
         text(516,262,'DRAW → 28×28 MNIST IMAGE → PREDICT → CONFIDENCE',18,MUTED,600,spacing=.7),
         line(516,302,1126,302),text(516,352,'PYTHON · PYTORCH · PYGAME',20,FG,700,spacing=1),
         text(516,410,'HANDWRITTEN INPUT',16,MUTED,600,spacing=1.2),
         text(516,442,'PREDICTION CONFIDENCE',16,MUTED,600,spacing=1.2),
         text(516,474,'OPTIONAL NETWORK VISUALIZATION',16,MUTED,600,spacing=1.2)]
    write('03-digit.svg',p)

def secondary():
    p=svg_start('Secondary work — Sixty-Four, WEBERAISE, Scout Email',560)
    p += [text(70,92,'MORE WORK',26,MUTED,700,spacing=2),line(70,122,1130,122)]
    rows=[('SIXTY-FOUR','C++17 · SFML · STOCKFISH','CUSTOMIZABLE CHESS SYSTEM'),
          ('WEBERAISE','NEXT.JS · MOTION · WEBGL','MOTION-LED WEB WORK'),
          ('SCOUT EMAIL','PYTHON · AUTOMATION · LLM WORKFLOWS','PROSPECT DISCOVERY + OUTREACH')]
    ys=[210,330,450]
    for (name,stack,desc),y in zip(rows,ys):
        p += [text(72,y,name,48,FG,800),text(1128,y-18,stack,15,MUTED,650,'end',.7),
              text(1128,y+18,desc,15,FG,650,'end',.7),line(72,y+48,1128,y+48)]
    p += [f'<rect x="70" y="506" width="210" height="10" fill="{ACC}"/>']
    write('04-secondary.svg',p)

def stack():
    p=svg_start('Tools and stack',490)
    p += [text(72,88,'TOOLS / STACK',24,MUTED,700,spacing=2),
          text(70,176,'PYTHON  C++  TYPESCRIPT',56,FG,800),
          text(70,252,'THREE.JS  WEBGL  REACT',56,FG,800),
          text(70,328,'NEXT.JS  PYTORCH  OPENCV',56,FG,800),
          text(70,404,'LANGGRAPH  SQLITE  LINUX',56,FG,800),
          f'<rect x="1042" y="132" width="88" height="272" fill="{ACC}"/>',
          text(1086,454,'05',34,MUTED,800,'middle')]
    write('05-stack.svg',p)

def ending():
    p=svg_start('Muhammad Ahmad — end mark',300)
    p += [line(72,70,1128,70),text(72,154,'MUHAMMAD AHMAD',64,FG,800),
          text(72,198,'PORTFOLIO · LINKEDIN · EMAIL · GITHUB',18,MUTED,650,spacing=1.4),
          f'<rect x="1004" y="116" width="124" height="124" fill="{ACC}"/>']
    write('06-end.svg',p)

for fn in [cover,automotive,orchestration,digit,secondary,stack,ending]: fn()
