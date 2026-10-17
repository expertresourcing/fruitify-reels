import subprocess, json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F=os.path.expanduser('~/fonts/')
FONT={'hi':'NotoSansDevanagari-Bold.ttf','mr':'NotoSansDevanagari-Bold.ttf','ta':'NotoSansTamil-Bold.ttf','te':'NotoSansTelugu-Bold.ttf','bn':'NotoSansBengali-Bold.ttf','kn':'NotoSansKannada-Bold.ttf','ml':'NotoSansMalayalam-Bold.ttf','gu':'NotoSansGujarati-Bold.ttf','pa':'NotoSansGurmukhi-Bold.ttf','or':'NotoSansOriya-Bold.ttf'}
LAT='/usr/share/fonts/opentype/inter/Inter-Bold.otf'
UP='./source-clips/'
CLIP={'OPS':UP+'6865e24e-Fruitify_-_Business_Operations.mp4','ORDER':UP+'a0e1b66a-Fruitify_-_Real_Order.mp4','ADD':UP+'a89c83c9-Fruitify_-_Adding_Fruits_to_start_the_Outlet.mp4','REP':UP+'d60e4d80-Fruitify_-_Business_Reports.mp4'}
ICON='./assets/app_icon.png'
BG=(12,76,53); YEL=(255,214,64); WHITE=(255,255,255)
W,H=1080,1920

def font(lang,size): return ImageFont.truetype(F+FONT[lang],size)
import re
_lat={}
def latf(size):
    if size not in _lat: _lat[size]=ImageFont.truetype(LAT,int(size*0.92))
    return _lat[size]
def runs(t):
    return [m.group(0) for m in re.finditer(r'[\x21-\x7e\u2014\u2013]+(?: [\x21-\x7e]+)*|[^\x21-\x7e\u2014\u2013]+',t)]
def isl(r): return bool(re.match(r'[\x21-\x7e\u2014\u2013]',r))
def tlen(d,t,fnt): return sum(d.textlength(r,font=latf(fnt.size) if isl(r) else fnt) for r in runs(t))
def tdraw(d,xy,t,fnt,fill):
    x,y=xy
    for r in runs(t):
        f=latf(fnt.size) if isl(r) else fnt
        d.text((x,y+(fnt.size*0.18 if isl(r) else 0)),r,font=f,fill=fill); x+=d.textlength(r,font=f)
def wrap(d,text,fnt,maxw):
    out=[]
    for para in text.split('\n'):
        words=para.split(' '); line=''
        for w in words:
            t=(line+' '+w).strip()
            if tlen(d,t,fnt)<=maxw or not line: line=t
            else: out.append(line); line=w
        out.append(line)
    return out
def block(d,y,text,fnt,color,maxw=920,gap=1.35):
    while fnt.size>30 and any(tlen(d,w,fnt)>maxw for w in text.split()): fnt=fnt.font_variant(size=fnt.size-4)
    for ln in wrap(d,text,fnt,maxw):
        tw=tlen(d,ln,fnt); tdraw(d,((W-tw)/2,y),ln,fnt,color); y+=int(fnt.size*gap)
    return y
def base():
    im=Image.new('RGB',(W,H),BG)
    # soft vignette
    g=Image.new('L',(W,H),0); gd=ImageDraw.Draw(g); gd.ellipse((-300,-200,W+300,H+200),fill=255); g=g.filter(ImageFilter.GaussianBlur(250))
    dark=Image.new('RGB',(W,H),(4,40,28)); im=Image.composite(im,dark,g)
    ic=Image.open(ICON).convert('RGBA').resize((150,150)); im.paste(ic,((W-150)//2,170),ic)
    d=ImageDraw.Draw(im); f=ImageFont.truetype(LAT,52); t='FRUiTIFY'; d.text(((W-d.textlength(t,font=f))/2,335),t,font=f,fill=WHITE)
    return im,d
def hook_card(lang,big,small,path):
    im,d=base()
    y=block(d,640,big,font(lang,92),YEL)
    block(d,y+60,small,font(lang,58),WHITE)
    im.save(path)
def end_card(lang,L,path):
    k=1.0
    while True:
        im,d=base()
        y=block(d,int(520*k+40*(1-k)),L['end1'],font(lang,int(80*k)),YEL)
        y=block(d,y+int(30*k),L['end2'],font(lang,int(54*k)),WHITE)
        y=block(d,y+int(50*k),L['end3'],font(lang,int(54*k)),YEL)
        y=block(d,y+int(60*k),L['end4'],font(lang,int(50*k)),WHITE)
        f=ImageFont.truetype(LAT,60); t='+91 96117 01149'; d.text(((W-d.textlength(t,font=f))/2,y+10),t,font=f,fill=YEL)
        f=ImageFont.truetype(LAT,50); t='fruitifyindia.com'; d.text(((W-d.textlength(t,font=f))/2,y+120),t,font=f,fill=WHITE)
        if y+190<1800 or k<0.6: break
        k-=0.05
    im.save(path)
def caption_band(lang,text,path):
    im=Image.new('RGBA',(W,300),(0,0,0,0)); d=ImageDraw.Draw(im)
    fnt=font(lang,50); lines=wrap(d,text,fnt,940); lh=int(50*1.45)
    d.rounded_rectangle((18,22,W-18,248),30,fill=(2,30,28,255))
    y=135-len(lines)*lh//2-6
    for ln in lines:
        tw=tlen(d,ln,fnt); tdraw(d,((W-tw)/2,y),ln,fnt,WHITE); y+=lh
    im.save(path)
def build(spec,out):
    lang=spec['lang']; tmp=out+'.d'; os.makedirs(tmp,exist_ok=True)
    hook_card(lang,spec['hook'],spec['sub'],tmp+'/hook.png'); end_card(lang,spec['L'],tmp+'/end.png')
    s,e=spec['seg']; e=e-0.35; clip=CLIP[spec['clip']]; HD,ED=3,4
    inputs=['-loop','1','-t',str(HD),'-i',tmp+'/hook.png','-ss',str(s),'-t',str(e-s),'-i',clip,'-loop','1','-t',str(ED),'-i',tmp+'/end.png','-ss',str(max(0,s-HD)),'-t',str(HD+e-s+ED),'-i',clip]
    fc='[0:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[h];'
    seg='[1:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1'
    caps=spec.get('caps')
    ov=[]
    if caps:
        fc+=seg+'[sv0];'; cur='sv0'
        for i,(t0,t1,txt) in enumerate(caps):
            p=f'{tmp}/cap{i}.png'; caption_band(lang,txt,p); inputs+=['-loop','1','-t',str(e-s),'-i',p]; idx=4+i
            nxt=f'sv{i+1}'; fc+=f'[{cur}][{idx}:v]overlay=0:1600:shortest=1:enable=\'between(t,{t0-s},{t1-s})\'[{nxt}];'; cur=nxt
        fc+=f'[{cur}]null[s];'
    else: fc+=seg+'[s];'
    fc+='[2:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[e];[h][s][e]concat=n=3:v=1:a=0[v];'
    T=HD+e-s+ED
    fc+=f'[3:a]volume=0.9,afade=t=in:d=1,afade=t=out:st={T-1.5}:d=1.5[a]'
    cmd=['ffmpeg','-v','error','-y']+inputs+['-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(T),'-c:v','libx264','-preset','medium','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',out]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-2000:]); sys.exit(1)
if __name__=='__main__':
    specs=json.load(open(sys.argv[1]))
    for sp in specs:
        if len(sys.argv)>2 and sp['id'] not in sys.argv[2:]: continue
        build(sp,os.path.expanduser('~/reels/out/')+sp['id']+'.mp4'); print('built',sp['id'])

BADGE={'ORDER':{'ta':'வாடிக்கையாளர் போன்','te':'కస్టమర్ ఫోన్','bn':'ক্রেতার ফোন','mr':'ग्राहकाचा फोन','gu':'ગ્રાહકનો ફોન','pa':'ਗਾਹਕ ਦਾ ਫ਼ੋਨ','kn':'ಗ್ರಾಹಕರ ಫೋನ್','ml':'ഉപഭോക്താവിന്റെ ഫോൺ'},
 'ADD':{'ta':'கடை உரிமையாளர் போன்','te':'షాప్ ఓనర్ ఫోన్','bn':'দোকান মালিকের ফোন','mr':'दुकान मालकाचा फोन','gu':'દુકાન માલિકનો ફોન','pa':'ਦੁਕਾਨ ਮਾਲਕ ਦਾ ਫ਼ੋਨ','kn':'ಅಂಗಡಿ ಮಾಲೀಕರ ಫೋನ್','ml':'കട ഉടമയുടെ ഫോൺ'}}
def badge_png(lang,clip,path):
    im=Image.new('RGBA',(W,170),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rectangle((600,52,W,160),fill=(30,84,78,255))
    txt=BADGE[clip][lang]; fnt=font(lang,40)
    while tlen(d,txt,fnt)>380 and fnt.size>24: fnt=fnt.font_variant(size=fnt.size-2)
    tw=tlen(d,txt,fnt); x1=1040; x0=x1-tw-56
    fill,col=((241,118,18),WHITE) if clip=='ORDER' else ((240,192,80),(28,58,39))
    d.rounded_rectangle((x0,74,x1,137),32,fill=fill)
    tdraw(d,(x0+28,105-int(fnt.size*0.68)),txt,fnt,col)
    im=im.filter(ImageFilter.SMOOTH) if False else im
    im.save(path)
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
def build_voiced(spec,out,vdir):
    lang=spec['lang']; tmp=out+'.d'; os.makedirs(tmp,exist_ok=True)
    hook_card(lang,spec['hook'],spec['sub'],tmp+'/hook.png'); end_card(lang,spec['L'],tmp+'/end.png')
    s,e=spec['seg']; e=e-0.35; S=e-s; clip=CLIP[spec['clip']]
    vh,vb,ve=[f"{vdir}/{spec['id']}_{p}.mp3" for p in ('hook','body','end')]
    ha,ba,ea=dur(vh),dur(vb),dur(ve)
    HD=round(ha+0.6,2); endstart=HD+0.3+ba+0.5
    ED=round(max(4.0, endstart+ea+0.8-(HD+S)),2); T=HD+S+ED
    inputs=['-loop','1','-t',str(HD),'-i',tmp+'/hook.png','-ss',str(s),'-t',str(S),'-i',clip,'-loop','1','-t',str(ED),'-i',tmp+'/end.png','-i',vh,'-i',vb,'-i',ve]
    fc='[0:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[h];[1:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[sv0];'
    cur='sv0'
    for i,(t0,t1,txt) in enumerate(spec['caps']):
        p=f'{tmp}/cap{i}.png'; caption_band(lang,txt,p); inputs+=['-loop','1','-t',str(S),'-i',p]; idx=6+i
        a=-10 if i==0 else t0-s; b=999 if i==len(spec['caps'])-1 else t1-s
        nxt=f'sv{i+1}'; fc+=f"[{cur}][{idx}:v]overlay=0:1600:shortest=1:enable='between(t,{a},{b})'[{nxt}];"; cur=nxt
    bp=f'{tmp}/badge.png'; badge_png(lang,spec['clip'],bp); inputs+=['-loop','1','-t',str(S),'-i',bp]; bi=6+len(spec['caps'])
    fc+=f"[{cur}][{bi}:v]overlay=0:0:shortest=1[svb];"; cur='svb'
    fc+=f'[2:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[e];[h][{cur}][e]concat=n=3:v=1:a=0[v];'
    d=lambda x:int(x*1000)
    fc+=f'[3:a]adelay={d(0.25)}|{d(0.25)}[a1];[4:a]adelay={d(HD+0.3)}|{d(HD+0.3)}[a2];[5:a]adelay={d(endstart)}|{d(endstart)}[a3];[a1][a2][a3]amix=inputs=3:normalize=0,apad,atrim=0:{T},afade=t=out:st={T-0.6}:d=0.6[a]'
    cmd=['ffmpeg','-v','error','-y']+inputs+['-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(T),'-c:v','libx264','-preset','medium','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','44100','-movflags','+faststart',out]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-2000:]); sys.exit(1)
    return T
