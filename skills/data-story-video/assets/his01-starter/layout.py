import json,os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
def find_font():
 explicit=os.environ.get('VIDEO_FONT_FILE')
 if explicit:
  if not Path(explicit).is_file():raise FileNotFoundError(f'VIDEO_FONT_FILE not found: {explicit}')
  return explicit,int(os.environ.get('VIDEO_FONT_INDEX','0')),int(os.environ.get('VIDEO_BOLD_FONT_INDEX',os.environ.get('VIDEO_FONT_INDEX','0')))
 candidates=[('/System/Library/Fonts/AppleSDGothicNeo.ttc',2,4),('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',1,1),('C:/Windows/Fonts/malgun.ttf',0,0)]
 for path,regular,bold in candidates:
  if Path(path).is_file():return path,regular,bold
 raise FileNotFoundError('Install a Korean font (e.g. fonts-noto-cjk), or set VIDEO_FONT_FILE to a Korean TTF/OTF/TTC file.')
FONT,REGULAR_INDEX,BOLD_INDEX=find_font()
BG='#10181c';FG='#f4f1e8';MUTED='#97a6a9';HOT='#fb744c'
CAT=json.loads((HERE/'chart-catalog.json').read_text())
font=lambda n,b=False:ImageFont.truetype(FONT,n,index=BOLD_INDEX if b else REGULAR_INDEX)
def wrap(s,f,maxw):
 lines=[]
 for raw in s.split('\n'):
  line=''
  for word in raw.split(' '):
   candidate=(line+' '+word) if line else word
   if f.getlength(candidate)>maxw and line:lines.append(line);line=word
   else:line=candidate
  lines.append(line)
 return '\n'.join(lines)
def txt(draw,xy,s,n=34,fill=FG,bold=False,maxw=928):
 draw.multiline_text(xy,wrap(s,font(n,bold),maxw),font=font(n,bold),fill=fill,spacing=9)
def overlay(e,ch,which):
 im=Image.new('RGBA',(1080,1350),(0,0,0,0));d=ImageDraw.Draw(im)
 d.rectangle((0,0,1080,105),fill=BG);txt(d,(76,33),e['track']+' / '+e['id'],27,bold=True);txt(d,(850,38),f"{e['chapters'].index(ch)+1} / {len(e['chapters'])}",23,MUTED)
 d.line((76,90,1004,90),fill='#334248',width=2)
 d.rectangle((0,1143,1080,1350),fill=BG);d.line((76,1144,1004,1144),fill='#334248',width=2)
 text=wrap(ch['captions'][which],font(34),928);assert len(text.splitlines())<=2,(e['id'],ch,text)
 txt(d,(76,1163),text,34)
 files=' · '.join(CAT[ch['chart']].get('sourceFiles',[]));txt(d,(76,1290),'출처: '+files,19,MUTED,maxw=800);txt(d,(922,1290),ch['chart'],19,MUTED)
 return im
def card(e,is_end):
 im=Image.new('RGB',(1080,1350),BG);d=ImageDraw.Draw(im)
 txt(d,(76,45),e['track']+' / '+e['id'],27,MUTED,True);d.line((76,103,1004,103),fill='#334248',width=2)
 txt(d,(76,172),'기록에서 남긴 기준' if is_end else e.get('openingLabel','실제 기록의 변화를 이어서'),27,HOT,True)
 title=e['ending'] if is_end else e['title'];txt(d,(76,285),title,64,bold=True,maxw=900)
 txt(d,(76,600),e['conclusion'] if is_end else e['question'],35,MUTED)
 if not is_end:
  for i,c in enumerate(e['chapters']):txt(d,(76,815+i*70),f"{i+1}   "+CAT[c['chart']]['title'],29,FG)
 elif e.get('related'):txt(d,(76,880),'함께 볼 내용: '+', '.join(e['related']),29,HOT)
 txt(d,(76,1228),e.get('footer','기록 기반 · 무음 · 날짜와 관찰 단위 유지'),25,MUTED)
 return im
def example_card(e,ch):
 im=Image.new('RGB',(1080,1350),BG);d=ImageDraw.Draw(im);x=ch['example']
 txt(d,(76,45),e['track']+' / '+e['id'],27,MUTED,True);d.line((76,103,1004,103),fill='#334248',width=2)
 txt(d,(76,172),'이해를 돕는 예시 · 실제 사건과 구분',27,HOT,True)
 txt(d,(76,285),x['title'],60,bold=True)
 txt(d,(76,620),x['term'],34,MUTED)
 txt(d,(76,900),e.get('chartLead','이어서 실제 기록의 차트를 봅니다.'),31,HOT)
 d.line((76,1145,1004,1145),fill='#334248',width=2);txt(d,(76,1163),x['caption'],34)
 txt(d,(76,1290),'생활 예시 → 용어 뜻 → 실제 데이터 → 해석 범위',23,MUTED)
 return im
