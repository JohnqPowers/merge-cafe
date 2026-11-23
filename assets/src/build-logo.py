import asyncio, math, sys, os
from playwright.async_api import async_playwright
D='/home/claude/logo/'
hero=open(D+'hero.svgfrag').read()
def wedges(cx,cy,R=1500,n=18,wdeg=10):
    out=[]
    for k in range(n):
        a0=math.radians(k*360/n-wdeg/2); a1=math.radians(k*360/n+wdeg/2)
        out.append(f'<polygon points="{cx},{cy} {cx+R*math.cos(a0):.1f},{cy+R*math.sin(a0):.1f} {cx+R*math.cos(a1):.1f},{cy+R*math.sin(a1):.1f}"/>')
    return ''.join(out)
BG=f'''<defs><radialGradient id="bg" cx=".5" cy=".42" r=".78"><stop offset="0" stop-color="#FFE08A"/><stop offset=".4" stop-color="#FF9A5A"/><stop offset="1" stop-color="#D2356B"/></radialGradient>
<radialGradient id="gl2" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFF3C4" stop-opacity=".62"/><stop offset=".6" stop-color="#FFF3C4" stop-opacity=".2"/><stop offset="1" stop-color="#FFF3C4" stop-opacity="0"/></radialGradient><radialGradient id="vg" cx=".5" cy=".5" r=".72"><stop offset=".6" stop-color="#7A0F3C" stop-opacity="0"/><stop offset="1" stop-color="#7A0F3C" stop-opacity=".38"/></radialGradient></defs>
<rect width="1024" height="1024" fill="url(#bg)"/><g fill="#fff" opacity=".14">{wedges(512,540)}</g><circle cx="512" cy="540" r="420" fill="url(#gl2)"/><rect width="1024" height="1024" fill="url(#vg)"/>'''
def hero_g(scale=1,dx=0,dy=0):
    return f'<g transform="translate({512+dx} {512+dy}) scale({scale}) translate(-554 -518)">{hero}</g>'
def svg(inner,bg=False):
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1024" height="1024" viewBox="0 0 1024 1024">{inner}</svg>'
VAR={
 'icon-background': svg(BG),
 'icon-foreground': svg(hero_g(.96)),
 'icon-only': svg(BG+hero_g(1.1,0,6)),
 'hero-only': svg(hero_g(1.0)),
}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1024,'height':1024},device_scale_factor=1)
        for name,s in VAR.items():
            await pg.set_content(f'<html><body style="margin:0;background:transparent">{s}</body></html>')
            await pg.wait_for_timeout(150)
            await pg.screenshot(path=D+name+'.png',omit_background=True)
            print('wrote',name)
        await b.close()
asyncio.run(main())
