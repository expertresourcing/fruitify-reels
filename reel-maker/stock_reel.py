# New-style reel: real footage first second, big question over the clip, end card. 1080x1920.
import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(__file__)); os.chdir(os.path.join(os.path.dirname(__file__), '..'))
from make import font, block, base, W, H, YEL, WHITE, LAT
from PIL import Image, ImageDraw, ImageFont
def overlay(lang, big, small, path, top=True):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # dark gradient band for readability
    band = Image.new('RGBA', (W, 760), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    for y in range(760): bd.line([(0, y), (W, y)], fill=(0, 0, 0, int(190 * (1 - y / 760) if top else 190 * y / 760)))
    im.alpha_composite(band, (0, 0 if top else H - 760)); d = ImageDraw.Draw(im)
    y0 = 230 if top else H - 620
    y = block(d, y0, big, font(lang, 96), YEL) if big else y0
    if small:
        from make import wrap, tlen
        fnt = font(lang, 62); lines = wrap(d, small, fnt, 900); lh = int(62 * 1.45)
        bh = len(lines) * lh + 70; top_y = H - 420 - bh
        d.rounded_rectangle((50, top_y, W - 50, top_y + bh), 36, fill=(2, 40, 30, 235))
        block(d, top_y + 30, small, fnt, WHITE, maxw=900)
    im.save(path)
def endcard(lang, l1, l2, l3, path):
    im, d = base()
    y = block(d, 640, l1, font(lang, 96), YEL)
    y = block(d, y + 50, l2, font(lang, 64), WHITE)
    f = ImageFont.truetype(LAT, 66); t = l3; d.text(((W - d.textlength(t, font=f)) / 2, y + 90), t, font=f, fill=YEL)
    f = ImageFont.truetype(LAT, 52); t = 'WhatsApp +91 96117 01149'; d.text(((W - d.textlength(t, font=f)) / 2, y + 200), t, font=f, fill=WHITE)
    im.save(path)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
def build(s):
    out = s['out']; tmp = out + '.d'; os.makedirs(tmp, exist_ok=True)
    overlay(s['lang'], s['hook'], '', tmp + '/o1.png', top=True)
    overlay(s['lang'], '', s['body'], tmp + '/o2.png', top=False)
    endcard(s['lang'], s['end1'], s['end2'], 'fruitifyindia.com/grow', tmp + '/end.png')
    vo = s['voice']; vd = dur(vo)
    a, b = s['clipA'], s['clipB']; ta, tb = s['tA'], s['tB']
    te = max(3.0, vd + 0.8 - ta - tb)
    fc = (f"[0:v]trim=start={s['sA']}:duration={ta},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30[va];"
          f"[1:v]trim=start={s['sB']}:duration={tb},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30[vb];"
          f"[va][2:v]overlay=0:0[va2];[vb][3:v]overlay=0:0[vb2];"
          f"[4:v]scale=1080:1920,fps=30,trim=duration={te},setpts=PTS-STARTPTS[ve];"
          f"[va2][vb2][ve]concat=n=3:v=1:a=0,format=yuv420p[v];"
          f"[5:a]adelay=250|250,apad,atrim=duration={ta+tb+te}[a]")
    cmd = ['ffmpeg','-v','error','-y','-i',a,'-i',b,'-i',tmp+'/o1.png','-i',tmp+'/o2.png','-loop','1','-t',str(te),'-i',tmp+'/end.png','-i',vo,
           '-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-preset','medium','-crf','22','-c:a','aac','-b:a','128k','-movflags','+faststart',out]
    subprocess.check_call(cmd); return out, ta+tb+te
if __name__ == '__main__':
    for s in json.load(open(sys.argv[1])): print(build(s))
