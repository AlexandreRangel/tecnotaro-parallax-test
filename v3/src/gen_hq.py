# Tecno Tarot Parallax 3, HQ 4 layer generator. Runs on Blackwell next to ComfyUI.
# python gen_hq.py A B [layers] ; layers: bg,mid,figure,energy (4 moving layers + static frame)
import json,sys,os,time,io,random,subprocess,urllib.request,urllib.parse
import numpy as np
from PIL import Image,ImageFilter,ImageDraw
API='http://127.0.0.1:8188'
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=r'C:\Dropbox\tarot-app\midia\decks\tecnotaro-parallax-3\raw_hq'
W,H=2120,3460            # final layer size (window x 1.12 @2x)
BW,BH=1024,1664          # base txt2img
HW,HH=1600,2600          # hires pass
CK=r'_SDXL_1_0\Juggernaut_XL\juggernautXL_ragnarokBy.safetensors'
STYLE=("Tecnotaro tarot art by Alexandre Rangel, playful energetic fluid mood, transhumanist cyberpunk steampunk world, polished brass and copper, glowing neon magenta, cyan and amber, "
 "very bright luminous high-key lighting, vivid saturated colors, painterly digital illustration, crisp fine details, sharp focus, masterpiece")
NEG=("text, letters, words, caption, watermark, signature, logo, border, frame, card frame, margin, young, teenager, child, kid, childlike, youthful face, east asian, asian, "
 "war, military, soldier, army, armor, armour, helmet, bandana, gun, rifle, weapon, combat, fighting pose, violence, blood, gore, muscular, bodybuilder, bulky, "
 "deformed, distorted face, bad anatomy, extra limbs, extra legs, extra arms, extra fingers, missing fingers, fused fingers, mutated hands, "
 "photo, photorealistic, blurry, soft focus, lowres, jpeg artifacts, dark, murky, underexposed, muddy, grainy, cropped head")
NOFIG="pedestrians, signage, neon text, shop signs, person, people, human, man, woman, figure, character, face, animal, creature, silhouette, crowd"
LOGF=os.path.join(HERE,'hq_run.log')
def log(*a):
    s=time.strftime('%H:%M:%S ')+' '.join(str(x) for x in a); print(s,flush=True); open(LOGF,'a').write(s+'\n')
class TooHot(Exception): pass
def gpu():
    o=subprocess.run(['nvidia-smi','--query-gpu=temperature.gpu,power.draw','--format=csv,noheader,nounits'],capture_output=True,text=True).stdout.strip().split(',')
    return int(o[0]),float(o[1])
TEMPS=[]
def guard():
    t,p=gpu()
    if t>85: raise TooHot(f'GPU {t} C')
    while t>80: log('cooling, gpu',t); time.sleep(20); t,p=gpu()
def post(path,data):
    r=urllib.request.Request(API+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json'});return json.loads(urllib.request.urlopen(r).read())
def get(path): return urllib.request.urlopen(API+path).read()
LOG=[];LAYER=['']
def run_graph(g):
    time.sleep(3); guard()   # one job at a time, 3 s pause; guard lengthens it above 80 C
    LOG.append({'layer':LAYER[0],'workflow':json.loads(json.dumps(g))})
    t0=time.time(); pid=post('/prompt',{"prompt":g,"client_id":"tecnov3hq"})['prompt_id']; peak=0
    while True:
        h=json.loads(get('/history/'+pid))
        if pid in h:
            st=h[pid].get('status',{})
            if st.get('status_str')=='error': raise RuntimeError(str(st)[:800])
            for o in h[pid]['outputs'].values():
                for im in o.get('images',[]):
                    q=urllib.parse.urlencode({'filename':im['filename'],'subfolder':im['subfolder'],'type':im['type']})
                    TEMPS.append(peak); log(f'  render {LAYER[0]} {time.time()-t0:.0f}s peak {peak}C')
                    return Image.open(io.BytesIO(get('/view?'+q))).convert('RGB')
        t,_=gpu(); peak=max(peak,t)
        if t>85:
            post('/interrupt',{}); raise TooHot(f'GPU {t} C during render')
        time.sleep(1)
def base(pos,neg):
    return {"1":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":CK}},
     "2":{"class_type":"CLIPTextEncode","inputs":{"text":pos,"clip":["1",1]}},
     "3":{"class_type":"CLIPTextEncode","inputs":{"text":neg,"clip":["1",1]}}}
def wf(pos,neg,seed,w=BW,h=BH):
    g=base(pos,neg); g.update({
    "4":{"class_type":"EmptyLatentImage","inputs":{"width":w,"height":h,"batch_size":1}},
    "5":{"class_type":"KSampler","inputs":{"model":["1",0],"positive":["2",0],"negative":["3",0],"latent_image":["4",0],"seed":seed,"steps":40,"cfg":4.5,"sampler_name":"dpmpp_2m_sde","scheduler":"karras","denoise":1.0}},
    "6":{"class_type":"VAEDecode","inputs":{"samples":["5",0],"vae":["1",2]}},
    "7":{"class_type":"UpscaleModelLoader","inputs":{"model_name":"4xNomos8k_atd_jpg.safetensors"}},
    "8":{"class_type":"ImageUpscaleWithModel","inputs":{"upscale_model":["7",0],"image":["6",0]}},
    "9":{"class_type":"ImageScale","inputs":{"image":["8",0],"upscale_method":"lanczos","width":HW,"height":HH,"crop":"disabled"}},
    "10":{"class_type":"VAEEncode","inputs":{"pixels":["9",0],"vae":["1",2]}},
    "11":{"class_type":"KSampler","inputs":{"model":["1",0],"positive":["2",0],"negative":["3",0],"latent_image":["10",0],"seed":seed+1,"steps":28,"cfg":4.5,"sampler_name":"dpmpp_2m_sde","scheduler":"karras","denoise":0.34}},
    "12":{"class_type":"VAEDecode","inputs":{"samples":["11",0],"vae":["1",2]}},
    "99":{"class_type":"SaveImage","inputs":{"images":["12",0],"filename_prefix":"tv3hq"}}}); return g
def upload(img,name):
    import requests
    b=io.BytesIO();img.save(b,'PNG');b.seek(0)
    return requests.post(API+'/upload/image',files={'image':(name,b,'image/png')},data={'overwrite':'true'}).json()['name']
def i2i(img,pos,neg,seed,den,steps=32):
    g=base(pos,neg); g.update({"4":{"class_type":"LoadImage","inputs":{"image":upload(img,'tv3hq_crop.png')}},
    "5":{"class_type":"VAEEncode","inputs":{"pixels":["4",0],"vae":["1",2]}},
    "6":{"class_type":"KSampler","inputs":{"model":["1",0],"positive":["2",0],"negative":["3",0],"latent_image":["5",0],"seed":seed,"steps":steps,"cfg":4.5,"sampler_name":"dpmpp_2m_sde","scheduler":"karras","denoise":den}},
    "7":{"class_type":"VAEDecode","inputs":{"samples":["6",0],"vae":["1",2]}},
    "99":{"class_type":"SaveImage","inputs":{"images":["7",0],"filename_prefix":"tv3hqfix"}}}); return run_graph(g)
_Y={}
def detect(img,model,conf):
    from ultralytics import YOLO
    if model not in _Y: _Y[model]=YOLO(os.path.join(r'C:\models\ultralytics\bbox',model))
    r=_Y[model](np.asarray(img)[...,::-1].copy(),conf=conf,device='cpu',verbose=False)[0]
    return [b for b in r.boxes.xyxy.tolist() if max(b[2]-b[0],b[3]-b[1])>=24]
def detail(img,model,txt,seed,den,conf=0.4,scale=2.0):
    # face / hand detailer: crop, re-render at 1024 px, paste back with a soft ellipse
    boxes=detect(img,model,conf); img=img.copy(); iw,ih=img.size
    for (x1,y1,x2,y2) in boxes:
        cx,cy=(x1+x2)/2,(y1+y2)/2; s=max(x2-x1,y2-y1)*scale
        X1,Y1=int(max(0,cx-s/2)),int(max(0,cy-s/2)); X2,Y2=int(min(iw,cx+s/2)),int(min(ih,cy+s/2))
        cr=img.crop((X1,Y1,X2,Y2)); cw,ch=cr.size; k=1024/max(cw,ch)
        out=i2i(cr.resize((int(cw*k)//8*8,int(ch*k)//8*8),Image.LANCZOS),txt,NEG,seed,den).resize((cw,ch),Image.LANCZOS)
        m=Image.new('L',(cw,ch),0); ImageDraw.Draw(m).ellipse((cw*.1,ch*.1,cw*.9,ch*.9),fill=255); m=m.filter(ImageFilter.GaussianBlur(cw*.06))
        img.paste(out,(X1,Y1),m); log('  detailed',model,int(x2-x1))
    return img
def render(pos,neg,seed,face=False,hand=False):
    for t in range(3):
        im=run_graph(wf(pos,neg,seed+t*7919))
        if np.asarray(im).std()>3: break
        log('blank render, retry')
    else: raise RuntimeError('blank renders')
    if face: im=detail(im,'face_yolov8m.pt',"detailed mature adult face with fine skin texture and expressive clear eyes, natural proportions, "+STYLE,seed+2,0.36)
    if hand: im=detail(im,'hand_yolov8s.pt',"detailed anatomically correct hand with five fingers, "+STYLE,seed+3,0.32,0.5,2.2)
    return im
def sharpen(im,r=1.6,p=70): return im.filter(ImageFilter.UnsharpMask(r,p,2))
def fit(im,size): # cover
    w,h=im.size; s=max(size[0]/w,size[1]/h); im=im.resize((round(w*s),round(h*s)),Image.LANCZOS)
    x,y=(im.width-size[0])//2,(im.height-size[1])//2; return im.crop((x,y,x+size[0],y+size[1]))
_S=None
def cut(img):
    """strict key: BiRefNet mask, hard threshold, 1 px choke, colour decontamination against the grey studio bg (no white fringe)"""
    global _S
    from rembg import remove,new_session
    if _S is None: _S=new_session('birefnet-general',providers=['CPUExecutionProvider'])
    a=np.asarray(remove(img,session=_S,only_mask=True)).astype(np.float32)/255
    a=np.clip((a-0.30)/0.45,0,1)
    a=np.asarray(Image.fromarray((a*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32)/255
    c=np.asarray(img).astype(np.float32)/255
    e=np.concatenate([c[:8].reshape(-1,3),c[-8:].reshape(-1,3),c[:,:8].reshape(-1,3),c[:,-8:].reshape(-1,3)]); bg=np.median(e,0)
    aa=np.maximum(a,0.05)[...,None]; f=np.clip((c-(1-aa)*bg)/aa,0,1); f=np.where(a[...,None]>0.97,c,f)
    # defringe: edge pixels take the colour of the solid interior instead of light halo
    edge=(a>0.02)&(a<0.9)
    if edge.any():
        inner=np.asarray(Image.fromarray((f*255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))).astype(np.float32)/255
        lum=f.mean(2); f[edge]=np.where((lum[edge]>inner[edge].mean(1)+0.15)[:,None],inner[edge],f[edge])
    return Image.fromarray((np.dstack([f,a])*255).astype(np.uint8),'RGBA')
def lumakey(img,gain=1.3,gamma=0.95):
    c=np.clip((np.asarray(img).astype(np.float32)/255-0.05)/0.95,0,1)
    a=np.clip(c.max(2)*gain,0,1)**gamma; f=np.clip(c/np.maximum(a,1e-3)[...,None],0,1)
    return Image.fromarray((np.dstack([f,a])*255).astype(np.uint8),'RGBA')
def mult_alpha(im,m):
    a=np.asarray(im).copy(); a[...,3]=(a[...,3]*m).astype(np.uint8); return Image.fromarray(a,'RGBA')
def place(pc,x,y):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); lay.paste(pc,(x,y),pc); return lay
def arrange(obj,suit,n,rng):  # Marseille arrangement, exact count
    canvas=Image.new('RGBA',(W,H),(0,0,0,0));ob=obj.crop(obj.getbbox())
    if suit in('swords','wands'):
        hh=int(H*(0.78 if suit=='swords' else 0.86));o=ob.resize((int(ob.width*hh/ob.height),hh),Image.LANCZOS)
        for i in range(n):
            t=(i-(n-1)/2)/max(1,(n-1)/2) if n>1 else 0
            ang=-t*min(28,6+3*n) if suit=='swords' else (22 if i%2==0 else -22)+rng.uniform(-3,3)
            oi=o.rotate(ang,expand=True,resample=Image.BICUBIC)
            if suit=='swords' and i%2: oi=oi.transpose(Image.FLIP_LEFT_RIGHT)
            canvas.alpha_composite(place(oi,int(W/2+t*W*(0.34 if suit=='swords' else 0.28)-oi.width/2),int(H*0.53-oi.height/2)))
        return canvas
    L={2:[(.5,.3),(.5,.72)],3:[(.3,.3),(.7,.3),(.5,.7)],4:[(.3,.3),(.7,.3),(.3,.7),(.7,.7)],5:[(.27,.25),(.73,.25),(.5,.5),(.27,.75),(.73,.75)],
     6:[(.3,.22),(.7,.22),(.3,.5),(.7,.5),(.3,.78),(.7,.78)],7:[(.3,.2),(.7,.2),(.5,.38),(.3,.56),(.7,.56),(.3,.8),(.7,.8)],
     8:[(.3,.17),(.7,.17),(.3,.39),(.7,.39),(.3,.61),(.7,.61),(.3,.83),(.7,.83)],9:[(.25,.17),(.75,.17),(.25,.39),(.75,.39),(.5,.5),(.25,.61),(.75,.61),(.25,.83),(.75,.83)],
     10:[(.27,.14),(.73,.14),(.5,.26),(.27,.38),(.73,.38),(.27,.62),(.73,.62),(.5,.74),(.27,.86),(.73,.86)]}[n]
    sw=int(W*{2:.52,3:.44,4:.44,5:.40,6:.38,7:.34,8:.31,9:.30,10:.28}[n]*(1.0 if suit=='coins' else 0.85))
    for (px,py) in L:
        s=sw*rng.uniform(0.95,1.05); o=ob.resize((int(s),int(ob.height*s/ob.width)),Image.LANCZOS).rotate(rng.uniform(-4,4),expand=True,resample=Image.BICUBIC)
        canvas.alpha_composite(place(o,int(px*W-o.width/2),int(py*H-o.height/2)))
    return canvas
GREY="isolated on a plain flat solid medium grey studio background"
def do_card(c,only=None):
    LOG.clear(); d=os.path.join(OUT,c['slug']); os.makedirs(d,exist_ok=True)
    n=c['n']; seed=5000+n*100; rng=random.Random(seed); E=c['energy']; info={}
    want=lambda k: only is None or k in only
    S=lambda k,im: im.save(os.path.join(d,k+'.png'))
    if want('bg'):
        LAYER[0]='sky'
        im=render(f"far distant background only, nobody, luminous sky and far horizon of {c['bg']}, huge glowing nebula clouds of {E} light, distant hazy floating islands and airships, soft atmospheric depth, {STYLE}",NEG+", "+NOFIG+", buildings in foreground",seed)
        S('_sky',sharpen(fit(im,(W,H)),1.2,50))
    if want('bg'):
        LAYER[0]='city'
        im=render(f"wide panoramic distant skyline silhouette of {c['mid']} and towers with glowing windows, seen from far away, horizontal band of architecture, {GREY}, {STYLE}",NEG+", "+NOFIG+", sky, clouds",seed+11)
        pc=cut(im); pc=pc.crop(pc.getbbox()); k=W*1.05/pc.width; pc=pc.resize((int(pc.width*k),int(pc.height*k)),Image.LANCZOS)
        if pc.height>H*0.45: k=H*0.45/pc.height; pc=pc.resize((int(pc.width*k),int(pc.height*k)),Image.LANCZOS)
        # light atmospheric haze so it reads far
        a=np.asarray(pc).astype(np.float32); a[...,:3]=a[...,:3]*0.8+np.array([200,170,235])*0.2; pc=Image.fromarray(a.astype(np.uint8),'RGBA')
        S('_city',place(pc,(W-pc.width)//2,int(H*0.66)-pc.height))
    if want('mid'):
        LAYER[0]='mid'; lay=Image.new('RGBA',(W,H),(0,0,0,0))
        for side in (0,1):
            im=render(f"one tall isolated {c['mid']}, single architectural set piece, full height from base to top, side view, {GREY}, {STYLE}",NEG+", "+NOFIG+", sky, clouds, scenery background",seed+21+side*5)
            pc=cut(im); pc=pc.crop(pc.getbbox()); k=min(H*rng.uniform(0.6,0.78)/pc.height,W*0.36/pc.width); pc=pc.resize((int(pc.width*k),int(pc.height*k)),Image.LANCZOS)
            x=-int(pc.width*rng.uniform(0.1,0.25)) if side==0 else W-int(pc.width*rng.uniform(0.75,0.9))
            lay.alpha_composite(place(pc,x,int(H*0.80)-pc.height))
        S('mid',lay)
    if want('figure'):
        LAYER[0]='ground'
        im=render(f"empty ground surface only, {c['ground']}, wide low angle view of the floor receding to the horizon, detailed textures, nobody, {STYLE}",NEG+", "+NOFIG+", sky, buildings",seed+31)
        g=fit(im,(W,int(H*0.42))); lay=Image.new('RGBA',(W,H),(0,0,0,0)); lay.paste(g,(0,H-g.height))
        y=np.arange(H)[:,None]/H; m=np.clip((y-0.60)/0.07,0,1)*np.ones((1,W))
        S('_ground',sharpen(mult_alpha(lay,m),1.2,50))
    if want('figure'):
        LAYER[0]='figure'
        if c['kind']=='pip':
            sg={'wands':'one single','cups':'one single','swords':'one single vertical','coins':'one single front view flat'}[c['suit']]
            im=render(f"{sg} {c['obj']}, full object centered, product shot, {GREY}, {STYLE}",NEG+", "+NOFIG+", multiple objects, two, pair",seed+41)
            fig=arrange(cut(sharpen(im)),c['suit'],c['count'],rng); info['faces']=[]
        else:
            person=c['kind'] in('major','court') and not c['n'] in (10,16,18)
            shot=("full body from head to feet, the character fills the entire frame height, large and close, feet at the bottom edge, realistic adult proportions, normal head size, slim body"
                  if person else "full composition, centered, large in frame, filling the image")
            im=render(f"{c['fig']}, {shot}, {GREY}, {STYLE}",NEG+", scenery, buildings, city, sky, small head, tiny figure, distant, floor shadow",seed+41,face=person or c['kind']=='ace',hand=person or c['kind']=='ace')
            im=sharpen(im); im.save(os.path.join(d,'_raw_figure.png')); fc=cut(im); fc=fc.crop(fc.getbbox())
            # large figure that reaches the card base: bottom anchored past the window bottom edge
            k=min(H*0.95/fc.height,W*0.96/fc.width); fc2=fc.resize((int(fc.width*k),int(fc.height*k)),Image.LANCZOS)
            ox,oy=(W-fc2.width)//2,H-fc2.height; fig=place(fc2,ox,oy)
            faces=detect(im,'face_yolov8m.pt',0.35); sx=fc2.width/fc.width
            bb0=Image.open(os.path.join(d,'_raw_figure.png')).size
            # faces in final coords (cut cropped at getbbox of cut alpha)
            cb=cut_bbox=None
            info['faces']=faces; info['xf']=[ox,oy,k]
        S('_fig',fig)
        if c['kind']!='pip':
            # map faces: recompute via detection on the placed figure composited on grey
            g=Image.new('RGB',(W,H),(128,128,128)); g.paste(fig,(0,0),fig)
            info['faces']=detect(g,'face_yolov8m.pt',0.3)
        json.dump(info,open(os.path.join(d,'_info.json'),'w'))
    if False:
        LAYER[0]='near'; lay=Image.new('RGBA',(W,H),(0,0,0,0))
        props=[c['near']]
        if c['kind']=='major': props.append({'lantern':"an ornate hanging brass steampunk lantern glowing amber on a chain",'cable':"hanging cables and wires with brass connectors and small neon lights",'pipe':"a cluster of brass steampunk pipes, valves and glowing neon gauges"}[c['prop']])
        left=rng.random()<0.5
        for i,p in enumerate(props):
            im=render(f"{p}, isolated object group, {GREY}, {STYLE}",NEG+", "+NOFIG,seed+51+i*5)
            pc=cut(sharpen(im)); pc=pc.crop(pc.getbbox())
            side=left if i==0 else not left; top=(i==1 and c['prop'] in('lantern','cable'))
            k=min(W*rng.uniform(0.26,0.34)/pc.width,H*0.24/pc.height); pc=pc.resize((int(pc.width*k),int(pc.height*k)),Image.LANCZOS)
            x=-int(pc.width*0.15) if side else W-int(pc.width*0.85); y=-int(pc.height*0.05) if top else H-int(pc.height*0.92)
            lay.alpha_composite(place(pc,x,y))
        S('near',lay)
    if want('energy'):
        LAYER[0]='energy'
        im=render(f"large swirling neon energy ribbons and luminous light streaks of {E}, flowing in from the edges around an empty center, glowing sparks, musical light waves and particles, on a pure black background, {STYLE}",NEG+", "+NOFIG+", objects, buildings, white background",seed+61)
        en=lumakey(fit(im,(W,H)))
        yy,xx=np.mgrid[0:H,0:W]; m=np.ones((H,W),np.float32)
        r=np.sqrt(((xx-W*.5)/(W*.30))**2+((yy-H*.45)/(H*.32))**2); m*=0.15+0.85*np.clip((r-0.55)/0.6,0,1)
        ip=os.path.join(d,'_info.json'); faces=json.load(open(ip)).get('faces',[]) if os.path.exists(ip) else []
        for (x1,y1,x2,y2) in faces:   # energy never crosses a face
            cx,cy=(x1+x2)/2,(y1+y2)/2; rx,ry=(x2-x1)*1.25,(y2-y1)*1.35
            rf=np.sqrt(((xx-cx)/rx)**2+((yy-cy)/ry)**2); m*=np.clip((rf-1)/0.6,0,1)
        fp=os.path.join(d,'_fig.png')
        if os.path.exists(fp):  # energy stays light over the body, strongest around it
            fa=np.asarray(Image.open(fp).getchannel('A').filter(ImageFilter.GaussianBlur(25))).astype(np.float32)/255
            m*=1-0.85*fa
        S('energy',mult_alpha(en,m))
    L_=lambda k: Image.open(os.path.join(d,k+'.png')).convert('RGBA')
    if want('bg'):      # bg = far sky + distant skyline, flattened
        im=L_('_sky'); im.alpha_composite(L_('_city')); im.convert('RGB').save(os.path.join(d,'bg.png'))
    if want('figure'):  # figure = ground band + character standing on it
        im=L_('_ground'); im.alpha_composite(L_('_fig')); im.save(os.path.join(d,'figure.png'))
    wp=os.path.join(d,'_workflows.json'); old=json.load(open(wp)) if os.path.exists(wp) else []
    done={e['layer'] for e in LOG}; json.dump([e for e in old if e['layer'] not in done]+LOG,open(wp,'w'),indent=1)
    comp=Image.new('RGBA',(W,H))
    for k in('bg','mid','figure','energy'):
        p=os.path.join(d,k+'.png')
        if os.path.exists(p): comp.alpha_composite(Image.open(p).convert('RGBA'))
    comp.convert('RGB').resize((W//2,H//2),Image.LANCZOS).save(os.path.join(d,'_composite.jpg'),quality=88)
if __name__=='__main__':
    cards=json.load(open(os.path.join(HERE,'cards_hq.json')))
    a,b=int(sys.argv[1]),int(sys.argv[2]); only=sys.argv[3].split(',') if len(sys.argv)>3 else None
    for c in cards[a:b+1]:
        t=time.time(); TEMPS.clear()
        try: do_card(c,only); log('OK',c['slug'],f'{time.time()-t:.0f}s','peakC',max(TEMPS or [0]))
        except TooHot as ex: log('STOP too hot',c['slug'],ex); sys.exit(3)
        except Exception as ex: log('FAIL',c['slug'],repr(ex)[:600])
        time.sleep(30)
